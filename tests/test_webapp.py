"""
Tests for merged_agentic_swarm.webapp — the control-panel JSON API + dashboard.

Coverage: /api/status (key pools + backends, no secret values), /api/reports
list + detail (404 + path-traversal guard), GET/PUT /api/profiles round-trip
against a tmp registry, /api/models role mapping (litellm fetch monkeypatched)
+ PUT /api/models/{role} registry write, GET/PUT /api/chains overlay merge,
/api/latency-test with a mocked httpx streaming transport, /api/run-plan,
POST /api/run background workflow kick-off, and the HTML dashboard. No test
touches the network or a real API key, and neither PROVIDER_REGISTRY.json nor
fabric-routes.json is ever written from a test.
"""

import json
import os
from pathlib import Path
from unittest.mock import patch

import httpx
import pytest
from starlette.testclient import TestClient

import merged_agentic_swarm.services.model_routing as mr
from merged_agentic_swarm import webapp
from merged_agentic_swarm.services import swarm_profiles
from merged_agentic_swarm.tools.agentic_orchestrator import MultiLayeredAgenticOrchestrator


@pytest.fixture(autouse=True)
def _fresh_caches():
    """Start each test with empty disk caches so patches don't leak across tests."""
    swarm_profiles._profiles_cache = None
    mr._registry_cache = None
    yield
    swarm_profiles._profiles_cache = None
    mr._registry_cache = None


@pytest.fixture
def client():
    app = webapp.create_app()
    with TestClient(app) as c:
        yield c


@pytest.fixture
def tmp_profiles_file(tmp_path):
    """Point swarm_profiles at a throwaway registry seeded with the on-disk profiles."""
    profiles = json.loads(swarm_profiles._PROFILES_PATH.read_text(encoding="utf-8"))
    target = tmp_path / "swarm-profiles.json"
    target.write_text(json.dumps(profiles, indent=2) + "\n", encoding="utf-8")
    with patch.object(swarm_profiles, "_PROFILES_PATH", target):
        yield target


class TestStatus:
    def test_status_has_pools_backends_and_no_secrets(self, client):
        data = client.get("/api/status").json()
        assert "key_pools" in data
        assert "fabric_routes" in data
        assert "registry_backends" in data
        assert "latest_report" in data

        # Pools expose only active/total/key_ids — never secret values.
        for info in data["key_pools"].values():
            assert set(info) == {"active", "total", "key_ids"}
            assert isinstance(info["key_ids"], list)

        # Backends expose base_url + auth env NAME + status + primary.
        for backend in data["registry_backends"].values():
            assert set(backend) == {"base_url", "auth_env", "status", "primary"}
            name = backend["auth_env"]
            assert any(tok in name for tok in ("KEY", "TOKEN", "SECRET")) or "+" in name

        text = json.dumps(data)
        assert "secret_value" not in text
        assert "Bearer " not in text
        key = os.environ.get("LITELLM_PROXY_KEY")
        if key:
            assert key not in text


class TestReports:
    def test_reports_lists_json_files_newest_first(self, tmp_path, client):
        target = tmp_path / "reports"
        target.mkdir()
        a = target / "20260101T000000Z.json"
        b = target / "20260102T000000Z.json"
        a.write_text('{"generated_at_utc":"2026-01-01T00:00:00+00:00"}', encoding="utf-8")
        b.write_text('{"generated_at_utc":"2026-01-02T00:00:00+00:00"}', encoding="utf-8")
        os.utime(a, (100.0, 100.0))
        os.utime(b, (110.0, 110.0))
        with patch.object(webapp, "_REPORTS_DIR", target):
            data = client.get("/api/reports").json()
        names = [r["name"] for r in data["reports"]]
        assert names == ["20260102T000000Z", "20260101T000000Z"]
        for r in data["reports"]:
            assert set(r) == {"name", "mtime"}

    def test_report_detail_returns_content(self, tmp_path, client):
        target = tmp_path / "reports"
        target.mkdir()
        (target / "abc.json").write_text(
            '{"generated_at_utc":"2026-01-01T00:00:00+00:00","waves":{"0":{"status_counts":{"completed":1}}}}',
            encoding="utf-8",
        )
        with patch.object(webapp, "_REPORTS_DIR", target):
            data = client.get("/api/reports/abc").json()
        assert data["generated_at_utc"] == "2026-01-01T00:00:00+00:00"
        assert data["waves"]["0"]["status_counts"]["completed"] == 1

    def test_report_detail_tolerates_json_suffix(self, tmp_path, client):
        target = tmp_path / "reports"
        target.mkdir()
        (target / "abc.json").write_text('{"generated_at_utc":"2026-01-01T00:00:00+00:00"}', encoding="utf-8")
        with patch.object(webapp, "_REPORTS_DIR", target):
            data = client.get("/api/reports/abc.json").json()
        assert data["generated_at_utc"] == "2026-01-01T00:00:00+00:00"

    def test_report_detail_unknown_404(self, tmp_path, client):
        with patch.object(webapp, "_REPORTS_DIR", tmp_path):
            resp = client.get("/api/reports/nope")
        assert resp.status_code == 404

    def test_report_detail_blocks_path_traversal(self, tmp_path, client):
        with patch.object(webapp, "_REPORTS_DIR", tmp_path):
            resp = client.get("/api/reports/%2e%2e%2f%2e%2e%2fetc%2fpasswd")
        assert resp.status_code == 404


class TestProfiles:
    def test_profiles_round_trip_update(self, tmp_profiles_file, client):
        resp = client.put(
            "/api/profiles/build",
            json={"description": "Edited build profile", "waves": [2, 4, 8]},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True
        assert data["profile"]["description"] == "Edited build profile"
        assert data["profile"]["waves"] == [2, 4, 8]

        # GET reflects the update (write path invalidates the load cache).
        profiles = client.get("/api/profiles").json()
        assert profiles["build"]["description"] == "Edited build profile"
        assert profiles["build"]["waves"] == [2, 4, 8]

        # The on-disk registry stayed valid JSON.
        on_disk = json.loads(tmp_profiles_file.read_text(encoding="utf-8"))
        assert on_disk["build"]["description"] == "Edited build profile"

    def test_profiles_put_unknown_profile_404(self, tmp_profiles_file, client):
        assert client.put("/api/profiles/nope", json={"description": "x"}).status_code == 404

    def test_profiles_put_invalid_body_400(self, tmp_profiles_file, client):
        assert client.put("/api/profiles/build", json={"bogus_key": 1}).status_code == 400
        resp = client.put(
            "/api/profiles/build",
            content=b"not-json",
            headers={"content-type": "application/json"},
        )
        assert resp.status_code == 400


class TestModels:
    def test_models_role_mapping_and_aliases(self, client):
        async def fake_fetch(_client):
            return ["gemini-batch", "gemini-batch-lite", "fast-flash"], None

        with patch.object(webapp, "_fetch_litellm_aliases", fake_fetch):
            data = client.get("/api/models").json()
        assert data["aliases"] == ["gemini-batch", "gemini-batch-lite", "fast-flash"]
        assert data["error"] is None
        mapping = data["role_mapping"]
        assert mapping["deep"] == "gemini-batch"
        assert mapping["main"] == "gemini-batch-lite"
        assert mapping["fast"] == "fast-flash"
        assert "cc-orchestrator" in mapping  # a registered role
        assert all(isinstance(v, str) for v in mapping.values())

    def test_models_fetch_failure_returns_empty_plus_note(self, client):
        async def fake_fetch(_client):
            return [], "litellm unreachable: boom"

        with patch.object(webapp, "_fetch_litellm_aliases", fake_fetch):
            data = client.get("/api/models").json()
        assert data["aliases"] == []
        assert data["error"] == "litellm unreachable: boom"
        assert data["role_mapping"]["deep"] == "gemini-batch"


class _Stream(httpx.AsyncByteStream):
    """Async byte stream over fixed chunks for the mocked litellm SSE response."""

    def __init__(self, chunks):
        self._chunks = list(chunks)

    async def __aiter__(self):
        for chunk in self._chunks:
            yield chunk

    async def aclose(self):
        pass


def _sse_chunks():
    return [
        b'data: {"id":"x","choices":[{"delta":{"content":"Hel"}}]}\n\n',
        b'data: {"id":"x","choices":[{"delta":{"content":"lo"}}]}\n\n',
        b"data: [DONE]\n\n",
    ]


class TestLatencyTest:
    @staticmethod
    def _app(handler):
        return webapp.create_app(transport=httpx.MockTransport(handler))

    def test_latency_test_streaming_success(self):
        def handler(request):
            return httpx.Response(
                200,
                headers={"content-type": "text/event-stream"},
                stream=_Stream(_sse_chunks()),
                request=request,
            )

        with TestClient(self._app(handler)) as c:
            data = c.post("/api/latency-test", json={"model": "gemini-batch"}).json()
        assert data["model"] == "gemini-batch"
        assert data["ok"] is True
        assert data["status_code"] == 200
        assert isinstance(data["ttft_ms"], float) and data["ttft_ms"] >= 0
        assert isinstance(data["total_ms"], float) and data["total_ms"] > 0
        assert "error" not in data
        text = json.dumps(data)
        assert "Bearer " not in text
        key = os.environ.get("LITELLM_PROXY_KEY")
        if key:
            assert key not in text

    def test_latency_test_defaults_max_tokens_256(self):
        seen = {}

        def handler(request):
            seen["json"] = json.loads(request.content)
            return httpx.Response(
                200,
                headers={"content-type": "text/event-stream"},
                stream=_Stream(_sse_chunks()),
                request=request,
            )

        with TestClient(self._app(handler)) as c:
            c.post("/api/latency-test", json={"model": "gemini-batch"})
        assert seen["json"]["model"] == "gemini-batch"
        assert seen["json"]["stream"] is True
        assert seen["json"]["max_tokens"] == 256

    def test_latency_test_connection_error_returns_ok_false(self):
        def handler(request):
            raise httpx.ConnectError("upstream down")

        with TestClient(self._app(handler)) as c:
            data = c.post("/api/latency-test", json={"model": "gemini-batch"}).json()
        assert data["ok"] is False
        assert data["status_code"] is None
        assert "error" in data
        key = os.environ.get("LITELLM_PROXY_KEY")
        if key:
            assert key not in json.dumps(data)

    def test_latency_test_missing_model_400(self):
        with TestClient(self._app(lambda r: httpx.Response(200, content=b"", request=r))) as c:
            resp = c.post("/api/latency-test", json={})
        assert resp.status_code == 400


class TestRunPlan:
    def test_run_plan_resolves_profile(self, client):
        data = client.post("/api/run-plan", json={"profile": "build"}).json()
        assert data["profile"] == "build"
        assert data["waves"] == [4, 8, 16, 24, 40]
        assert data["ramp"] == [4, 8, 16, 24, 40]
        assert data["model_alias"] == "gemini-batch"
        assert data["default_tier"] == "deep"
        assert data["gates"] is True
        assert "master_architect" in data["worker_roles"]

    def test_run_plan_learning_profile_uses_default_ramp(self, client):
        data = client.post("/api/run-plan", json={"profile": "learning"}).json()
        assert data["waves"] == []
        assert data["ramp"] == [4, 8, 16, 24, 40]

    def test_run_plan_unknown_profile_404(self, client):
        assert client.post("/api/run-plan", json={"profile": "nope"}).status_code == 404

    def test_run_plan_missing_profile_400(self, client):
        assert client.post("/api/run-plan", json={}).status_code == 400


class TestModelRoleUpdate:
    def test_model_role_update_writes_registry_and_reloads(self, tmp_path, client):
        real_registry_before = mr._REGISTRY_PATH.read_text(encoding="utf-8")
        target = tmp_path / "PROVIDER_REGISTRY.json"
        target.write_text(real_registry_before, encoding="utf-8")
        with patch.object(mr, "_REGISTRY_PATH", target), patch.object(mr, "reload_registry") as spy:
            resp = client.put("/api/models/deep", json={"alias": "smart-auto"})
            assert resp.status_code == 200
            data = resp.json()
        assert data["ok"] is True
        assert data["role"] == "deep"
        assert data["role_mapping"]["deep"] == "smart-auto"
        # The write path persisted role_routing.roles atomically.
        on_disk = json.loads(target.read_text(encoding="utf-8"))
        assert on_disk["role_routing"]["roles"]["deep"] == "smart-auto"
        assert on_disk["tiers"]  # untouched top-level keys preserved
        spy.assert_called_once_with()
        # The real PROVIDER_REGISTRY.json was never modified.
        assert mr._REGISTRY_PATH.read_text(encoding="utf-8") == real_registry_before

    def test_model_role_update_allows_new_role(self, tmp_path, client):
        target = tmp_path / "PROVIDER_REGISTRY.json"
        target.write_text(mr._REGISTRY_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        with patch.object(mr, "_REGISTRY_PATH", target):
            resp = client.put("/api/models/brand-new-role", json={"alias": "fast-flash"})
        assert resp.status_code == 200
        assert resp.json()["role_mapping"]["brand-new-role"] == "fast-flash"

    def test_model_role_update_invalid_400(self, tmp_path, client):
        target = tmp_path / "PROVIDER_REGISTRY.json"
        target.write_text("{}", encoding="utf-8")
        with patch.object(mr, "_REGISTRY_PATH", target):
            # alias must match ^[A-Za-z][A-Za-z0-9._-]*$
            assert client.put("/api/models/deep", json={"alias": "bad alias!"}).status_code == 400
            assert client.put("/api/models/deep", json={"alias": "2fast"}).status_code == 400
            assert client.put("/api/models/deep", json={"alias": 123}).status_code == 400
            assert client.put("/api/models/deep", json={"alias": ""}).status_code == 400
            assert client.put("/api/models/deep", json={}).status_code == 400
            # role must be a non-empty string
            assert client.put("/api/models/%20%20", json={"alias": "ok-alias"}).status_code == 400
            assert (
                client.put(
                    "/api/models/deep", content=b"not-json", headers={"content-type": "application/json"}
                ).status_code
                == 400
            )
        # Nothing was written to the throwaway registry.
        assert json.loads(target.read_text(encoding="utf-8")) == {}


class TestChains:
    @pytest.fixture
    def overlay_path(self, tmp_path):
        """Point webapp at a throwaway fabric-routes.json (never the real file)."""
        target = tmp_path / "fabric-routes.json"
        target.write_text(json.dumps({"routes": {}}) + "\n", encoding="utf-8")
        with patch.object(webapp, "_FABRIC_ROUTES_PATH", target):
            yield target

    def test_chains_get_merges_defaults_and_overlay(self, overlay_path, client):
        # Seed the overlay: override one code alias + add a brand-new alias.
        overlay_path.write_text(
            json.dumps(
                {
                    "routes": {
                        "claude-3-7-sonnet": [
                            {"provider": "gemini", "model": "override-model", "url": "http://x", "timeout": 5}
                        ],
                        "my-custom-chain": [{"provider": "mistral", "model": "mistral-tiny"}],
                    }
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        chains = client.get("/api/chains").json()["chains"]
        # Code-default aliases still present with their route chain.
        assert "claude-3-5-haiku" in chains
        assert chains["claude-3-5-haiku"][0]["provider"] == "gemini"
        # Overlay wins per alias.
        assert chains["claude-3-7-sonnet"] == [
            {"provider": "gemini", "model": "override-model", "url": "http://x", "timeout": 5}
        ]
        # New aliases from the overlay are added.
        assert chains["my-custom-chain"] == [{"provider": "mistral", "model": "mistral-tiny"}]

    def test_chains_put_upserts_overlay_and_merges(self, tmp_path, client):
        real_path = Path(webapp.__file__).resolve().parents[2] / "docs" / "agentic" / "fabric-routes.json"
        real_before = real_path.read_text(encoding="utf-8")
        target = tmp_path / "fabric-routes.json"
        target.write_text(json.dumps({"routes": {}}) + "\n", encoding="utf-8")
        with patch.object(webapp, "_FABRIC_ROUTES_PATH", target):
            resp = client.put(
                "/api/chains/my-chain",
                json={
                    "routes": [{"provider": "gemini", "model": "gemini-2.5-flash", "url": "http://g", "timeout": 30}]
                },
            )
            assert resp.status_code == 200
            data = resp.json()
            assert data["ok"] is True
            assert data["alias"] == "my-chain"
            assert data["routes"][0]["model"] == "gemini-2.5-flash"
            # The merged GET reflects the upsert immediately.
            chains = client.get("/api/chains").json()["chains"]
            assert chains["my-chain"] == [
                {"provider": "gemini", "model": "gemini-2.5-flash", "url": "http://g", "timeout": 30}
            ]
        # The overlay file was persisted.
        on_disk = json.loads(target.read_text(encoding="utf-8"))
        assert on_disk["routes"]["my-chain"] == [
            {"provider": "gemini", "model": "gemini-2.5-flash", "url": "http://g", "timeout": 30}
        ]
        # The real docs/agentic/fabric-routes.json was never touched.
        assert real_path.read_text(encoding="utf-8") == real_before

    def test_chains_put_invalid_400(self, overlay_path, client):
        assert client.put("/api/chains/bad%20alias", json={"routes": []}).status_code == 400
        assert client.put("/api/chains/2cool", json={"routes": []}).status_code == 400
        assert client.put("/api/chains/my-chain", json={}).status_code == 400
        assert client.put("/api/chains/my-chain", json={"routes": []}).status_code == 400
        assert client.put("/api/chains/my-chain", json={"routes": "nope"}).status_code == 400
        assert client.put("/api/chains/my-chain", json={"routes": [{"model": "x"}]}).status_code == 400
        assert client.put("/api/chains/my-chain", json={"routes": [{"provider": "x"}]}).status_code == 400
        assert (
            client.put(
                "/api/chains/my-chain", json={"routes": [{"provider": "x", "model": "y", "timeout": "30"}]}
            ).status_code
            == 400
        )
        # Nothing was written to the overlay.
        assert json.loads(overlay_path.read_text(encoding="utf-8")) == {"routes": {}}


class TestRun:
    def test_run_starts_workflow_in_background(self, client):
        captured = {}

        def fake_run(self, **kwargs):
            captured.update(kwargs)
            return {"started": True}

        # Keep the patch active until the daemon thread has run — otherwise the
        # real workflow (which executes for real) would kick off once reverted.
        with patch.object(MultiLayeredAgenticOrchestrator, "run_full_agentic_workflow", fake_run):
            resp = client.post("/api/run", json={"profile": "patch", "prd": "# title\n\nbody"})
            thread = client.app.state.last_run_thread
            assert thread is not None and thread.daemon
            thread.join(timeout=10)
        assert resp.status_code == 200
        data = resp.json()
        assert data == {"started": True, "profile": "patch", "model_alias": "fast-flash"}
        assert captured["prd_content"] == "# title\n\nbody"
        assert captured["ramp_sequence"] == [4]
        assert captured["default_model"] == "fast-flash"
        assert captured["gates"] is False

    def test_run_learning_profile_forwards_none_ramp(self, client):
        captured = {}

        def fake_run(self, **kwargs):
            captured.update(kwargs)
            return {"started": True}

        with patch.object(MultiLayeredAgenticOrchestrator, "run_full_agentic_workflow", fake_run):
            resp = client.post("/api/run", json={"profile": "learning", "prd": "# title\n\nbody"})
            client.app.state.last_run_thread.join(timeout=10)
        assert resp.status_code == 200
        assert captured["ramp_sequence"] is None
        assert captured["gates"] is False

    def test_run_unknown_profile_404(self, client):
        assert client.post("/api/run", json={"profile": "nope", "prd": "x"}).status_code == 404

    def test_run_missing_prd_400(self, client):
        assert client.post("/api/run", json={"profile": "patch"}).status_code == 400

    def test_run_missing_profile_400(self, client):
        assert client.post("/api/run", json={"prd": "x"}).status_code == 400


def test_dashboard_html(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert "Agentic Swarm Control Panel" in resp.text
    assert "latency-test" in resp.text
    assert "run-plan" in resp.text
    # New forms: role alias editing, chain editing, and the real-run kicker.
    assert "role-form" in resp.text
    assert "chain-form" in resp.text
    assert "run-form" in resp.text
    assert "executes for real" in resp.text
