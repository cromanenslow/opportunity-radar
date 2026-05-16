"""测试 Algora 扫描质量修复

验证：
1. _clean_description() 能正确去除 HTML 标签和噪声
2. _parse_bounty_amount() 能鲁棒解析各种金额格式
3. _extract_amount() 能处理更多金额模式
"""

from __future__ import annotations

import unittest
from scanner.platforms import (
    _clean_description,
    _extract_amount,
    _parse_bounty_amount,
)


class TestCleanDescription(unittest.TestCase):
    """测试 Description 净化函数"""

    def test_removes_html_tags(self):
        raw = "<p>This is a bug report</p><div>Please fix it</div>"
        cleaned = _clean_description(raw)
        self.assertNotIn("<p>", cleaned)
        self.assertNotIn("</div>", cleaned)
        self.assertIn("This is a bug report", cleaned)
        self.assertIn("Please fix it", cleaned)

    def test_removes_html_with_attributes(self):
        raw = '<a href="https://example.com">Click here</a> to reproduce'
        cleaned = _clean_description(raw)
        self.assertNotIn("<a", cleaned)
        self.assertNotIn("</a>", cleaned)
        self.assertIn("Click here", cleaned)
        self.assertIn("to reproduce", cleaned)

    def test_removes_urls(self):
        raw = "See https://github.com/user/repo/issues/1 for details"
        cleaned = _clean_description(raw)
        self.assertNotIn("https://github.com", cleaned)
        self.assertIn("See", cleaned)
        self.assertIn("for details", cleaned)

    def test_removes_markdown_image(self):
        raw = "![screenshot](https://example.com/img.png) The bug is here"
        cleaned = _clean_description(raw)
        self.assertNotIn("![screenshot]", cleaned)
        self.assertNotIn("https://example.com/img.png", cleaned)
        self.assertIn("The bug is here", cleaned)

    def test_removes_markdown_link(self):
        raw = "See [the issue](https://github.com/org/repo) for context"
        cleaned = _clean_description(raw)
        self.assertNotIn("[the issue]", cleaned)
        self.assertNotIn("https://github.com/org/repo", cleaned)
        self.assertIn("See", cleaned)
        self.assertIn("for context", cleaned)

    def test_truncates_long_code_blocks(self):
        code = "x" * 500
        raw = f"Report:\n```python\n{code}\n```\nEnd"
        cleaned = _clean_description(raw, max_len=500)
        # Should not contain the full 500-char code block
        self.assertLess(len(cleaned), 400)
        self.assertIn("Report:", cleaned)
        self.assertIn("```", cleaned)
        self.assertIn("End", cleaned)

    def test_normalizes_whitespace(self):
        raw = "  Too    many   spaces   \n\n\n  and\nnewlines  "
        cleaned = _clean_description(raw)
        self.assertNotIn("  ", cleaned)  # no double spaces
        self.assertNotIn("\n\n", cleaned)
        # Should have single spaces between words
        self.assertEqual(cleaned, "Too many spaces and newlines")

    def test_truncation_at_word_boundary(self):
        long_text = "word " * 200
        cleaned = _clean_description(long_text, max_len=100)
        self.assertLessEqual(len(cleaned), 104)  # 100 + "..." max
        self.assertTrue(cleaned.endswith("..."))

    def test_handles_none_or_empty(self):
        self.assertEqual(_clean_description(None), "")
        self.assertEqual(_clean_description(""), "")
        self.assertEqual(_clean_description("  "), "")

    def test_strips_script_tags(self):
        raw = "Normal text. <script>alert('xss')</script> More text."
        cleaned = _clean_description(raw)
        self.assertNotIn("<script>", cleaned)
        self.assertNotIn("</script>", cleaned)
        self.assertIn("alert('xss')", cleaned)  # content preserved, only tags removed
        self.assertIn("Normal text.", cleaned)
        self.assertIn("More text.", cleaned)

    def test_keeps_meaningful_content(self):
        raw = "## Steps to reproduce\n1. Click button\n2. See error\n\n**Expected:** Works\n**Actual:** Broken"
        cleaned = _clean_description(raw)
        self.assertIn("Steps to reproduce", cleaned)
        self.assertIn("Click button", cleaned)
        self.assertIn("See error", cleaned)
        self.assertIn("Expected:", cleaned)
        self.assertIn("Actual:", cleaned)
        self.assertIn("Broken", cleaned)


class TestParseBountyAmount(unittest.TestCase):
    """测试 Bounty 金额解析鲁棒性"""

    def test_parses_numeric_int(self):
        self.assertEqual(_parse_bounty_amount(100), 100.0)
        self.assertEqual(_parse_bounty_amount(0), 0.0)
        self.assertEqual(_parse_bounty_amount(-50), 0.0)  # negative → 0

    def test_parses_numeric_float(self):
        self.assertEqual(_parse_bounty_amount(50.5), 50.5)
        self.assertEqual(_parse_bounty_amount(0.0), 0.0)

    def test_parses_dollar_string(self):
        self.assertEqual(_parse_bounty_amount("$100"), 100.0)
        self.assertEqual(_parse_bounty_amount("$ 50"), 50.0)
        self.assertEqual(_parse_bounty_amount("$1,000"), 1000.0)
        self.assertEqual(_parse_bounty_amount("$ 1,234.56"), 1234.56)

    def test_parses_usd_suffix(self):
        self.assertEqual(_parse_bounty_amount("100 USD"), 100.0)
        self.assertEqual(_parse_bounty_amount("50 usd"), 50.0)
        self.assertEqual(_parse_bounty_amount("1,000 USD"), 1000.0)

    def test_parses_usdc_suffix(self):
        self.assertEqual(_parse_bounty_amount("100 USDC"), 100.0)
        self.assertEqual(_parse_bounty_amount("50 usdc"), 50.0)

    def test_parses_plain_number_string(self):
        self.assertEqual(_parse_bounty_amount("100"), 100.0)
        self.assertEqual(_parse_bounty_amount("50.50"), 50.5)
        self.assertEqual(_parse_bounty_amount("0"), 0.0)

    def test_parses_range_takes_max(self):
        self.assertEqual(_parse_bounty_amount("$100-$200"), 200.0)
        self.assertEqual(_parse_bounty_amount("$50 - $100"), 100.0)
        self.assertEqual(_parse_bounty_amount("$1,000 - $5,000"), 5000.0)

    def test_handles_none(self):
        self.assertEqual(_parse_bounty_amount(None), 0.0)

    def test_handles_empty_string(self):
        self.assertEqual(_parse_bounty_amount(""), 0.0)
        self.assertEqual(_parse_bounty_amount("  "), 0.0)

    def test_handles_garbage_string(self):
        self.assertEqual(_parse_bounty_amount("not-a-number"), 0.0)
        self.assertEqual(_parse_bounty_amount("abc"), 0.0)
        self.assertEqual(_parse_bounty_amount("TODO"), 0.0)

    def test_handles_string_with_leading_text(self):
        """Fallback: extract numbers from text"""
        self.assertEqual(_parse_bounty_amount("Bounty: $100"), 100.0)
        self.assertEqual(_parse_bounty_amount("Reward: 50 USD"), 50.0)
        self.assertEqual(_parse_bounty_amount("Prize: $ 75.50"), 75.5)

    def test_handles_currency_value_in_sentence(self):
        """Fallback regex picks up amounts in natural language"""
        self.assertEqual(_parse_bounty_amount("Up to $250 reward"), 250.0)
        self.assertEqual(_parse_bounty_amount("$500 bounty available"), 500.0)

    def test_handles_invalid_type(self):
        self.assertEqual(_parse_bounty_amount([]), 0.0)
        self.assertEqual(_parse_bounty_amount({}), 0.0)


class TestExtractAmount(unittest.TestCase):
    """测试 _extract_amount 增强"""

    def test_dollar_prefix(self):
        self.assertEqual(_extract_amount("$100 reward"), 100.0)
        self.assertEqual(_extract_amount("bounty: $1,000"), 1000.0)
        self.assertEqual(_extract_amount("fixed $50.50"), 50.5)

    def test_usd_suffix(self):
        self.assertEqual(_extract_amount("100 USD reward"), 100.0)
        self.assertEqual(_extract_amount("Bounty: 500 USD"), 500.0)
        self.assertEqual(_extract_amount("Prize: 1,000 USD"), 1000.0)

    def test_usdc_suffix(self):
        self.assertEqual(_extract_amount("100 USDC"), 100.0)
        self.assertEqual(_extract_amount("Bounty: 500 USDC"), 500.0)

    def test_range_takes_max(self):
        self.assertEqual(_extract_amount("$100-$200"), 200.0)
        self.assertEqual(_extract_amount("$50 - $100"), 100.0)
        self.assertEqual(_extract_amount("$100 - $200"), 200.0)

    def test_no_match_returns_zero(self):
        self.assertEqual(_extract_amount(""), 0.0)
        self.assertEqual(_extract_amount("no numbers here"), 0.0)
        self.assertEqual(_extract_amount("Free work"), 0.0)

    def test_combination_text(self):
        """Extract from realistic issue body"""
        body = (
            "## Bounty\n"
            "This issue has a $250 bounty.\n"
            "Please fix the bug and earn 250 USD.\n"
        )
        self.assertEqual(_extract_amount(body), 250.0)

    def test_multiple_amounts_takes_max(self):
        self.assertEqual(_extract_amount("$50 or $100 or $75"), 100.0)
        self.assertEqual(_extract_amount("$100 and $200 and $50"), 200.0)


if __name__ == "__main__":
    unittest.main()
