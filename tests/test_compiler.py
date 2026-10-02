# tests/test_compiler.py
import os
from pathlib import Path
import tempfile
import unittest

from main import extract_latex, rename_pdf, count_pdf_pages


class TestOverleafCVCompiler(unittest.TestCase):

    def test_extract_latex_raw(self):
        code = r"\documentclass{article}\begin{document}Hello\end{document}"
        self.assertEqual(extract_latex(code), code)

    def test_extract_latex_markdown_fence(self):
        raw = "```latex\n\\documentclass{article}\n\\begin{document}Hello\\end{document}\n```"
        expected = "\\documentclass{article}\n\\begin{document}Hello\\end{document}"
        self.assertEqual(extract_latex(raw), expected)

    def test_extract_latex_with_conversational_text(self):
        raw = (
            "Sure! Here is your tailored resume:\n\n"
            "```latex\n"
            "\\documentclass{article}\n"
            "\\begin{document}\n"
            "Senior Engineer\n"
            "\\end{document}\n"
            "```\n"
            "Let me know if you need any adjustments!"
        )
        extracted = extract_latex(raw)
        self.assertTrue(extracted.startswith("\\documentclass{article}"))
        self.assertTrue(extracted.endswith("\\end{document}"))
        self.assertNotIn("Sure!", extracted)
        self.assertNotIn("Let me know", extracted)

    def test_rename_pdf_template(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(b"%PDF-1.4 ...")
            tmp_path = f.name

        try:
            renamed = rename_pdf(
                tmp_path=tmp_path,
                role="Senior AI Engineer / Lead",
                candidate_name="Alex Developer"
            )
            self.assertTrue(renamed.endswith("Alex_Developer_Your_Next_Senior_AI_Engineer_Lead.pdf"))
            self.assertTrue(os.path.exists(renamed))
            os.remove(renamed)
        except Exception:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            raise


if __name__ == "__main__":
    unittest.main()
