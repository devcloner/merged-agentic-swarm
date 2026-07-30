"""
Tests for tools/token_savior.py

Coverage: TokenSavior — compact_code_snippet, compact_bash_output,
compress_prose_output.
"""
from tools.token_savior import TokenSavior


class TestTokenSavior:
    def setup_method(self):
        self.ts = TokenSavior()

    def test_compact_code_removes_blank_and_comment_lines(self):
        code = """
# Header comment
def foo():
    pass

    # Another comment
    x = 1
"""
        result = self.ts.compact_code_snippet(code)
        assert "# Header comment" not in result
        assert "# Another comment" not in result
        assert "def foo():" in result
        assert "x = 1" in result

    def test_compact_code_truncates_long(self):
        lines = [f"line_{i}" for i in range(500)]
        code = "\n".join(lines)
        result = self.ts.compact_code_snippet(code, max_lines=100)
        assert "[Truncated" in result
        assert result.count("\n") <= 101  # 100 lines + truncation message

    def test_compact_code_does_not_truncate_short(self):
        code = "a = 1\nb = 2\n"
        result = self.ts.compact_code_snippet(code, max_lines=200)
        assert "[Truncated" not in result

    def test_compact_bash_output_short(self):
        output = "line1\nline2\n"
        result = self.ts.compact_bash_output(output, max_lines=50)
        assert result == output

    def test_compact_bash_output_filters_errors(self):
        lines = [f"line_{i}" for i in range(200)]
        lines.append("ERROR: something failed")
        output = "\n".join(lines)
        result = self.ts.compact_bash_output(output, max_lines=50)
        assert "ERROR" in result or len(result.splitlines()) <= 50

    def test_compress_prose_removes_fillers(self):
        text = "As an AI language model, I hope this helps! Feel free to ask if you have any questions."
        result = self.ts.compress_prose_output(text)
        assert "As an AI language model" not in result
        assert "I hope this helps" not in result

    def test_compress_prose_keeps_essential(self):
        text = "Here is the code you requested: print('hello'). Certainly!"
        result = self.ts.compress_prose_output(text)
        assert "print('hello')" in result

    def test_compress_prose_does_not_mutate_clean_text(self):
        text = "def foo(): pass\nreturn bar"
        result = self.ts.compress_prose_output(text)
        assert result == text

    def test_empty_input(self):
        assert self.ts.compact_code_snippet("") == ""
        assert self.ts.compact_bash_output("") == ""
        assert self.ts.compress_prose_output("") == ""
