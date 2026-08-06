"""
Token Savior & Context Compactor
Optimizes context window consumption via symbol-level extraction, log compaction, and prose compression.
"""

import logging
import re

logger = logging.getLogger("token_savior")


class TokenSavior:
    @staticmethod
    def compact_code_snippet(code: str, max_lines: int = 200) -> str:
        """Removes blank lines and excessive indentation spaces to save tokens."""
        lines = code.splitlines()
        compacted = []
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            compacted.append(line)
        if len(compacted) > max_lines:
            return (
                "\n".join(compacted[:max_lines])
                + f"\n... [Truncated {len(compacted) - max_lines} lines by Token Savior]"
            )
        return "\n".join(compacted)

    @staticmethod
    def compact_bash_output(output: str, max_lines: int = 50) -> str:
        """Filters noisy bash logs and retains error tracebacks + summary lines."""
        lines = output.splitlines()
        if len(lines) <= max_lines:
            return output

        error_lines = [
            l
            for l in lines
            if any(k in l.lower() for k in ("error", "fail", "exception", "traceback", "warning", "passed", "failed"))
        ]
        tail_lines = lines[-max_lines:]

        combined = list(dict.fromkeys(error_lines + tail_lines))
        return "\n".join(combined[:max_lines])

    @staticmethod
    def compress_prose_output(text: str) -> str:
        """Compresses assistant prose (Caveman mode) by removing pleasantries, hedging, and filler words."""
        fillers = [
            r"\bAs an AI language model,?\b",
            r"\bI hope this helps!?\b",
            r"\bFeel free to ask if you have any questions.?\b",
            r"\bCertainly!?\b",
            r"\bHere is the code you requested:?\b",
        ]
        res = text
        for filler in fillers:
            res = re.sub(filler, "", res, flags=re.IGNORECASE)
        return res.strip()


# Helper
default_token_savior = TokenSavior()
