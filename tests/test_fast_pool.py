import httpx

from merged_agentic_swarm.fast_pool import FastPoolConfig, dispatch


class _FakeClient:
    """Records the per-request timeout passed to post() without network I/O."""

    def __init__(self) -> None:
        self.last_timeout: httpx.Timeout | None = None
        self.closed = False

    @property
    def is_closed(self) -> bool:
        return self.closed

    def post(self, url: str, content: bytes, headers: dict, timeout: httpx.Timeout) -> httpx.Response:
        self.last_timeout = timeout
        return httpx.Response(200, content=b"{}", request=httpx.Request("POST", url))

    def close(self) -> None:
        self.closed = True


def _install_fake(monkeypatch) -> _FakeClient:
    fake = _FakeClient()
    monkeypatch.setattr("merged_agentic_swarm.fast_pool.get_client", lambda config=None: fake)
    return fake


def test_dispatch_localhost_uses_local_connect_timeout(monkeypatch):
    fake = _install_fake(monkeypatch)
    cfg = FastPoolConfig(connect_timeout=5.0, local_connect_timeout=2.0)
    dispatch("http://localhost:4000/v1/messages", b"{}", {}, 30.0, cfg)
    assert fake.last_timeout is not None
    assert fake.last_timeout.connect == 2.0
    assert fake.last_timeout.read == 30.0


def test_dispatch_remote_keeps_configured_connect_timeout(monkeypatch):
    fake = _install_fake(monkeypatch)
    cfg = FastPoolConfig(connect_timeout=5.0, local_connect_timeout=2.0)
    # Localhost first, then remote: the remote must keep 5.0, not inherit 2.0.
    dispatch("http://localhost:4000/v1/messages", b"{}", {}, 30.0, cfg)
    assert fake.last_timeout.connect == 2.0
    dispatch("https://api.example.com/v1/messages", b"{}", {}, 30.0, cfg)
    assert fake.last_timeout.connect == 5.0
    assert fake.last_timeout.read == 30.0
