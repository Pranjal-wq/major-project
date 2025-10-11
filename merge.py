"""import ast
import sys
import os

# --- Your analyzers here ---
class DeadCodeDetector(ast.NodeVisitor):
    def visit_If(self, node):
        if isinstance(node.test, ast.Constant):
            if node.test.value is True:
                print(f"[Dead Code] Else branch is unreachable at line {node.lineno}")
            elif node.test.value is False:
                print(f"[Dead Code] If branch is unreachable at line {node.lineno}")
        self.generic_visit(node)

class InlineExpansionDetector(ast.NodeVisitor):
    def visit_BinOp(self, node):
        if isinstance(node.op, ast.Mult):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                print(f"[Inline Expansion] Constant multiplication at line {node.lineno}: {ast.unparse(node)}")

        if isinstance(node.op, ast.Add):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                print(f"[Inline Expansion] Constant addition at line {node.lineno}: {ast.unparse(node)}")

        if isinstance(node.op, ast.Pow):
            if isinstance(node.right, ast.Constant) and node.right.value == 2:
                print(f"[Inline Expansion] Squaring detected at line {node.lineno}: {ast.unparse(node)}")

        self.generic_visit(node)

class OpaquePredicateDetector(ast.NodeVisitor):
    def visit_If(self, node):
        if isinstance(node.test, ast.BoolOp):
            for value in node.test.values:
                if isinstance(value, ast.Compare):
                    if isinstance(value.left, ast.Constant):
                        print(f"[Opaque Predicate] Constant comparison at line {node.lineno}: {ast.unparse(value)}")

                    if isinstance(value.left, ast.BinOp) and all(
                        isinstance(child, ast.Constant) for child in [value.left.left, value.left.right]
                    ):
                        print(f"[Opaque Predicate] Arithmetic constant comparison at line {node.lineno}: {ast.unparse(value)}")
        self.generic_visit(node)


def analyze_code(code):
    try:
        tree = ast.parse(code)
        print("\n--- Analysis Results ---\n")
        DeadCodeDetector().visit(tree)
        InlineExpansionDetector().visit(tree)
        OpaquePredicateDetector().visit(tree)
        print("\n--- Analysis Completed ---")
    except Exception as e:
        print("Error while analyzing code:", e)


def main():
    if len(sys.argv) < 3:
        print("Usage: python analyzer.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, "r") as f:
        code = f.read()

    # Redirect stdout to output file
    original_stdout = sys.stdout
    with open(output_file, "w") as f:
        sys.stdout = f
        analyze_code(code)
        sys.stdout = original_stdout

    print(f"Analysis complete. Results saved to {output_file}")


if __name__ == "__main__":
    main()
"""





"""

import ast
import sys
import os

# ------------------- DEAD CODE DETECTOR -------------------
class DeadCodeDetector(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.assigned = set()
        self.used = set()

    def visit_If(self, node):
        if isinstance(node.test, ast.Constant):
            if node.test.value is True:
                print(f"[Dead Code] Else branch is unreachable at line {node.lineno}")
            elif node.test.value is False:
                print(f"[Dead Code] If branch is unreachable at line {node.lineno}")
        self.generic_visit(node)

    def visit_While(self, node):
        if isinstance(node.test, ast.Constant) and node.test.value is False:
            print(f"[Dead Code] While loop never executes at line {node.lineno}")
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        for i, stmt in enumerate(node.body):
            if isinstance(stmt, ast.Return):
                for later_stmt in node.body[i+1:]:
                    print(f"[Dead Code] Code after return at line {later_stmt.lineno} inside function '{node.name}'")
        self.generic_visit(node)

    def visit_For(self, node):
        for stmt in node.body:
            if isinstance(stmt, ast.Break):
                idx = node.body.index(stmt)
                for later in node.body[idx+1:]:
                    print(f"[Dead Code] Code after break at line {later.lineno} in for loop")
        self.generic_visit(node)

    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Name):
            self.assigned.add(node.targets[0].id)
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.used.add(node.id)
        self.generic_visit(node)

    def report_unused(self):
        unused = self.assigned - self.used
        for var in unused:
            print(f"[Dead Code] Variable '{var}' assigned but never used")

# ------------------- INLINE EXPANSION DETECTOR -------------------
class InlineExpansionDetector(ast.NodeVisitor):
    def visit_BinOp(self, node):
        if isinstance(node.op, ast.Mult):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                print(f"[Inline Expansion] Constant multiplication at line {node.lineno}: {ast.unparse(node)}")

        if isinstance(node.op, ast.Add):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                print(f"[Inline Expansion] Constant addition at line {node.lineno}: {ast.unparse(node)}")

        if isinstance(node.op, ast.Pow):
            if isinstance(node.right, ast.Constant) and node.right.value == 2:
                print(f"[Inline Expansion] Squaring detected at line {node.lineno}: {ast.unparse(node)}")

        self.generic_visit(node)

# ------------------- OPAQUE PREDICATE DETECTOR -------------------
class OpaquePredicateDetector(ast.NodeVisitor):
    def visit_If(self, node):
        if isinstance(node.test, ast.BoolOp):
            for value in node.test.values:
                if isinstance(value, ast.Compare):
                    if isinstance(value.left, ast.Constant):
                        print(f"[Opaque Predicate] Constant comparison at line {node.lineno}: {ast.unparse(value)}")

                    if isinstance(value.left, ast.BinOp) and all(
                        isinstance(child, ast.Constant) for child in [value.left.left, value.left.right]
                    ):
                        print(f"[Opaque Predicate] Arithmetic constant comparison at line {node.lineno}: {ast.unparse(value)}")
        self.generic_visit(node)

# ------------------- ANALYSIS FUNCTION -------------------
def analyze_code(code, filename):
    try:
        print(f"\n===== Analyzing File: {filename} =====\n")
        tree = ast.parse(code)

        dead_detector = DeadCodeDetector()
        dead_detector.visit(tree)
        dead_detector.report_unused()

        InlineExpansionDetector().visit(tree)
        OpaquePredicateDetector().visit(tree)

        print(f"\n===== Completed: {filename} =====\n")
    except Exception as e:
        print(f"Error analyzing {filename}: {e}")

# ------------------- MAIN -------------------
def main():
    input_folder = "input"
    output_file = "output/combined_results.out"

    if not os.path.exists("output"):
        os.makedirs("output")

    original_stdout = sys.stdout
    with open(output_file, "w") as f:
        sys.stdout = f

        for filename in os.listdir(input_folder):
            if filename.endswith(".py"):
                file_path = os.path.join(input_folder, filename)
                with open(file_path, "r") as infile:
                    code = infile.read()
                analyze_code(code, filename)

        sys.stdout = original_stdout

    print(f"✅ Combined analysis complete. Results saved in {output_file}")


if __name__ == "__main__":
    main()
"""

"""
import os
import sys
import re
import ast

# -------------------- PYTHON ANALYZER (AST) --------------------
class PythonAnalyzer:
    def analyze(self, code, filename):
        print(f"\n===== Analyzing Python File: {filename} =====\n")
        try:
            tree = ast.parse(code)

            dead = DeadCodeDetector()
            dead.visit(tree)
            dead.report_unused()

            InlineExpansionDetector().visit(tree)
            OpaquePredicateDetector().visit(tree)

        except Exception as e:
            print(f"Error analyzing Python file {filename}: {e}")


class DeadCodeDetector(ast.NodeVisitor):
    def __init__(self):
        self.assigned = set()
        self.used = set()

    def visit_If(self, node):
        if isinstance(node.test, ast.Constant):
            if node.test.value is True:
                print(f"[Dead Code] Else branch unreachable at line {node.lineno}")
            elif node.test.value is False:
                print(f"[Dead Code] If branch unreachable at line {node.lineno}")
        self.generic_visit(node)

    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Name):
            self.assigned.add(node.targets[0].id)
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.used.add(node.id)

    def report_unused(self):
        for var in self.assigned - self.used:
            print(f"[Dead Code] Variable '{var}' assigned but never used")


class InlineExpansionDetector(ast.NodeVisitor):
    def visit_BinOp(self, node):
        if isinstance(node.op, (ast.Add, ast.Mult, ast.Pow)):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                print(f"[Inline Expansion] Constant expression at line {node.lineno}: {ast.unparse(node)}")
        self.generic_visit(node)


class OpaquePredicateDetector(ast.NodeVisitor):
    def visit_If(self, node):
        if isinstance(node.test, ast.Compare) and isinstance(node.test.left, ast.Constant):
            print(f"[Opaque Predicate] Constant condition at line {node.lineno}: {ast.unparse(node)}")
        self.generic_visit(node)


# -------------------- REGEX ANALYZER (C, C++, JAVA, KOTLIN) --------------------
class RegexAnalyzer:
    def analyze(self, code, filename):
        print(f"\n===== Analyzing File: {filename} =====\n")

        lines = code.split("\n")
        for i, line in enumerate(lines, start=1):

            # Dead code detection
            if re.search(r"\bif\s*\(\s*false\s*\)", line) or re.search(r"\bwhile\s*\(\s*false\s*\)", line):
                print(f"[Dead Code] Unreachable branch at line {i}: {line.strip()}")
            if re.search(r"\breturn\b.*;", line) and i < len(lines) and lines[i].strip():
                print(f"[Dead Code] Possible code after return at line {i+1}: {lines[i].strip()}")

            # Inline expansion detection
            if re.search(r"\d+\s*[\+\-\*\/]\s*\d+", line):
                print(f"[Inline Expansion] Constant expression at line {i}: {line.strip()}")
            if re.search(r"\b(\w+)\s*\*\s*\1\b", line):  # x*x
                print(f"[Inline Expansion] Squaring detected at line {i}: {line.strip()}")

            # Opaque predicate detection
            if re.search(r"\bif\s*\(\s*\d+\s*(==|!=|>|<|>=|<=)\s*\d+\s*\)", line):
                print(f"[Opaque Predicate] Constant comparison at line {i}: {line.strip()}")

        print(f"\n===== Completed: {filename} =====\n")


# -------------------- HANDLER --------------------
def analyze_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    ext = os.path.splitext(filepath)[1]
    if ext == ".py":
        PythonAnalyzer().analyze(code, filepath)
    elif ext in [".c", ".cpp", ".java", ".kt"]:
        RegexAnalyzer().analyze(code, filepath)
    else:
        print(f"Skipping unsupported file: {filepath}")


def main():
    input_folder = "input"
    output_file = "output/combined_results.out"

    if not os.path.exists("output"):
        os.makedirs("output")

    original_stdout = sys.stdout
    with open(output_file, "w", encoding="utf-8") as f:
        sys.stdout = f
        for filename in os.listdir(input_folder):
            file_path = os.path.join(input_folder, filename)
            analyze_file(file_path)
        sys.stdout = original_stdout

    print(f"✅ Multi-language analysis complete. Results saved in {output_file}")


if __name__ == "__main__":
    main()


"""




"""
import os
import sys
import re
import ast
from io import StringIO

# -------------------- PDF EXPORT --------------------
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER


def save_pdf(results, pdf_path="output/combined_results.pdf"):
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name="TitleStyle",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontSize=16,
        spaceAfter=20
    )
    normal_style = ParagraphStyle(
        name="NormalStyle",
        parent=styles["Normal"],
        fontSize=11,
        leading=14,
    )

    content = []
    content.append(Paragraph("🔍 Code Analysis Results", title_style))
    content.append(Spacer(1, 12))

    for line in results.split("\n"):
        if line.strip().startswith("====="):  # Add section separator
            content.append(PageBreak())
            content.append(Paragraph(line.strip(), styles["Heading2"]))
            content.append(Spacer(1, 12))
        else:
            content.append(Paragraph(line.replace("→", "->"), normal_style))
            content.append(Spacer(1, 6))

    doc.build(content)
    print(f"📄 PDF saved at {pdf_path}")


# -------------------- PYTHON ANALYZER (AST) --------------------
class PythonAnalyzer:
    def analyze(self, code, filename):
        print(f"\n===== Analyzing Python File: {filename} =====\n")
        try:
            tree = ast.parse(code)

            dead = DeadCodeDetector()
            dead.visit(tree)
            dead.report_unused()

            InlineExpansionDetector().visit(tree)
            OpaquePredicateDetector().visit(tree)

        except Exception as e:
            print(f"Error analyzing Python file {filename}: {e}")


class DeadCodeDetector(ast.NodeVisitor):
    def __init__(self):
        self.assigned = set()
        self.used = set()

    def visit_If(self, node):
        if isinstance(node.test, ast.Constant):
            if node.test.value is True:
                print(f"[Dead Code] Else branch unreachable at line {node.lineno}")
            elif node.test.value is False:
                print(f"[Dead Code] If branch unreachable at line {node.lineno}")
        self.generic_visit(node)

    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Name):
            self.assigned.add(node.targets[0].id)
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.used.add(node.id)

    def report_unused(self):
        for var in self.assigned - self.used:
            print(f"[Dead Code] Variable '{var}' assigned but never used")


class InlineExpansionDetector(ast.NodeVisitor):
    def visit_BinOp(self, node):
        if isinstance(node.op, (ast.Add, ast.Mult, ast.Pow)):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                print(f"[Inline Expansion] Constant expression at line {node.lineno}: {ast.unparse(node)}")
        self.generic_visit(node)


class OpaquePredicateDetector(ast.NodeVisitor):
    def visit_If(self, node):
        if isinstance(node.test, ast.Compare) and isinstance(node.test.left, ast.Constant):
            print(f"[Opaque Predicate] Constant condition at line {node.lineno}: {ast.unparse(node)}")
        self.generic_visit(node)


# -------------------- REGEX ANALYZER (C, C++, JAVA, KOTLIN) --------------------
class RegexAnalyzer:
    def analyze(self, code, filename):
        print(f"\n===== Analyzing File: {filename} =====\n")

        lines = code.split("\n")
        for i, line in enumerate(lines, start=1):

            # Dead code detection
            if re.search(r"\bif\s*\(\s*false\s*\)", line) or re.search(r"\bwhile\s*\(\s*false\s*\)", line):
                print(f"[Dead Code] Unreachable branch at line {i}: {line.strip()}")
            if re.search(r"\breturn\b.*;", line) and i < len(lines) and lines[i].strip():
                print(f"[Dead Code] Possible code after return at line {i+1}: {lines[i].strip()}")

            # Inline expansion detection
            if re.search(r"\d+\s*[\+\-\*\/]\s*\d+", line):
                print(f"[Inline Expansion] Constant expression at line {i}: {line.strip()}")
            if re.search(r"\b(\w+)\s*\*\s*\1\b", line):  # x*x
                print(f"[Inline Expansion] Squaring detected at line {i}: {line.strip()}")

            # Opaque predicate detection
            if re.search(r"\bif\s*\(\s*\d+\s*(==|!=|>|<|>=|<=)\s*\d+\s*\)", line):
                print(f"[Opaque Predicate] Constant comparison at line {i}: {line.strip()}")

        print(f"\n===== Completed: {filename} =====\n")


# -------------------- HANDLER --------------------
def analyze_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    ext = os.path.splitext(filepath)[1]
    if ext == ".py":
        PythonAnalyzer().analyze(code, filepath)
    elif ext in [".c", ".cpp", ".java", ".kt"]:
        RegexAnalyzer().analyze(code, filepath)
    else:
        print(f"Skipping unsupported file: {filepath}")


def main():
    input_folder = "input"
    output_file = "output/combined_results.out"

    if not os.path.exists("output"):
        os.makedirs("output")

    # Capture output in memory
    buffer = StringIO()
    original_stdout = sys.stdout
    sys.stdout = buffer

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        analyze_file(file_path)

    sys.stdout = original_stdout
    results = buffer.getvalue()

    # Save TXT
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(results)

    # Save PDF
    save_pdf(results)

    print(f"✅ Multi-language analysis complete. Results saved in {output_file} and PDF.")


if __name__ == "__main__":
    main()
"""



"""

import os
import sys
import re
import ast
from io import StringIO

# Your custom modules
from input.nameIdentifier import IdentifierCleaner, detect_language
from input.controlFlow import FakeConditionCleaner
from input.stringEncryption import StringDecryptor

# -------------------- PDF EXPORT --------------------
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

def save_pdf(results, pdf_path="output/combined_results.pdf"):
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name="TitleStyle",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontSize=16,
        spaceAfter=20
    )
    normal_style = ParagraphStyle(
        name="NormalStyle",
        parent=styles["Normal"],
        fontSize=11,
        leading=14,
    )

    content = [Paragraph("🔍 Code Analysis Results", title_style), Spacer(1,12)]
    for line in results.split("\n"):
        if line.strip().startswith("====="):
            content.append(PageBreak())
            content.append(Paragraph(line.strip(), styles["Heading2"]))
            content.append(Spacer(1,12))
        else:
            content.append(Paragraph(line.replace("→","->"), normal_style))
            content.append(Spacer(1,6))

    doc.build(content)
    print(f"📄 PDF saved at {pdf_path}")

# -------------------- ANALYZERS --------------------
class DeadCodeDetector(ast.NodeVisitor):
    def __init__(self):
        self.assigned = set()
        self.used = set()
    def visit_If(self, node):
        if isinstance(node.test, ast.Constant):
            if node.test.value is True:
                print(f"[Dead Code] Else branch unreachable at line {node.lineno}")
            elif node.test.value is False:
                print(f"[Dead Code] If branch unreachable at line {node.lineno}")
        self.generic_visit(node)
    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Name):
            self.assigned.add(node.targets[0].id)
        self.generic_visit(node)
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.used.add(node.id)
    def report_unused(self):
        for var in self.assigned - self.used:
            print(f"[Dead Code] Variable '{var}' assigned but never used")

class InlineExpansionDetector(ast.NodeVisitor):
    def visit_BinOp(self, node):
        if isinstance(node.op, (ast.Add, ast.Mult, ast.Pow)):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                print(f"[Inline Expansion] Constant expression at line {node.lineno}: {ast.unparse(node)}")
        self.generic_visit(node)

class OpaquePredicateDetector(ast.NodeVisitor):
    def visit_If(self, node):
        if isinstance(node.test, ast.Compare) and isinstance(node.test.left, ast.Constant):
            print(f"[Opaque Predicate] Constant condition at line {node.lineno}: {ast.unparse(node)}")
        self.generic_visit(node)

class PythonAnalyzer:
    def analyze(self, code, filename):
        try:
            tree = ast.parse(code)
            DeadCodeDetector().visit(tree)
            InlineExpansionDetector().visit(tree)
            OpaquePredicateDetector().visit(tree)
        except Exception as e:
            print(f"[Python Analysis] Error in {filename}: {e}")

class RegexAnalyzer:
    def analyze(self, code, filename):
        lines = code.split("\n")
        for i, line in enumerate(lines, start=1):
            if re.search(r"\bif\s*\(\s*false\s*\)", line) or re.search(r"\bwhile\s*\(\s*false\s*\)", line):
                print(f"[Dead Code] Unreachable branch at line {i}: {line.strip()}")
            if re.search(r"\d+\s*[\+\-\*\/]\s*\d+", line):
                print(f"[Inline Expansion] Constant expression at line {i}: {line.strip()}")
            if re.search(r"\bif\s*\(\s*\d+\s*(==|!=|>|<|>=|<=)\s*\d+\s*\)", line):
                print(f"[Opaque Predicate] Constant comparison at line {i}: {line.strip()}")

# -------------------- FILE HANDLER --------------------
def analyze_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()
    lang = detect_language(os.path.basename(filepath))

    results = {"String Decryption": [], "Identifier Cleaner": [], "Control Flow": [], "Code Analysis": []}

    # ---------------- String Decryption ----------------
    str_cleaner = StringDecryptor()
    str_changes, code_after_strings = str_cleaner.detect_and_clean(code)
    if str_changes:
        for c in str_changes:
            results["String Decryption"].append(
                f"{filepath}: {c['original']} -> {c['decrypted']} ({c['reason']})"
            )

    # ---------------- Identifier Cleaner ----------------
    id_cleaner = IdentifierCleaner(language=lang)
    try:
        obf_changes, deobf_code = id_cleaner.detect_and_clean(code_after_strings)
    except SyntaxError as e:
        results["Identifier Cleaner"].append(f"{filepath}: Skipped due to syntax error: {e}")
        obf_changes = []
        deobf_code = code_after_strings
    for c in obf_changes:
        results["Identifier Cleaner"].append(
            f"{filepath}: {c['original']} -> {c['cleaned']} ({c['reason']})"
        )

    # ---------------- Control Flow ----------------
    cf_cleaner = FakeConditionCleaner()
    cf_changes = cf_cleaner.clean_code(deobf_code)
    for c in cf_changes:
        results["Control Flow"].append(
            f"{filepath}: {c['original']} -> {c['cleaned']} ({c['reason']})"
        )

    # ---------------- Code Analysis ----------------
    final_code = deobf_code
    for c in cf_changes:
        final_code = final_code.replace(c['original'], c['cleaned'])
    if lang == "python":
        buffer = StringIO()
        sys.stdout = buffer
        PythonAnalyzer().analyze(final_code, filepath)
        sys.stdout = sys.__stdout__
        analysis_output = buffer.getvalue().strip()
        if analysis_output:
            results["Code Analysis"].append(analysis_output)
    elif lang in ["c", "cpp", "java", "kotlin"]:
        buffer = StringIO()
        sys.stdout = buffer
        RegexAnalyzer().analyze(final_code, filepath)
        sys.stdout = sys.__stdout__
        analysis_output = buffer.getvalue().strip()
        if analysis_output:
            results["Code Analysis"].append(analysis_output)

    return results

# -------------------- MAIN --------------------
def main():
    input_folder = "input"
    output_file = "output/combined_results.out"
    os.makedirs("output", exist_ok=True)

    # Dictionary to store aggregated results
    all_results = {"String Decryption": [], "Identifier Cleaner": [], "Control Flow": [], "Code Analysis": []}

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if os.path.isdir(file_path):
            continue
        file_results = analyze_file(file_path)
        for key in all_results:
            all_results[key].extend(file_results[key])

    # Prepare final uniform report
    report_lines = []
    for technique, cases in all_results.items():
        report_lines.append(f"\n===== {technique} =====\n")
        if cases:
            report_lines.extend(cases)
        else:
            report_lines.append("No cases detected.")
        report_lines.append("\n")

    final_report = "\n".join(report_lines)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_report)

    save_pdf(final_report)
    print(f"✅ Multi-language analysis complete. Results saved in {output_file} and PDF.")

if __name__ == "__main__":
    main()

    """

"""

import os
import sys
from io import StringIO

# -------------------- Import all detection modules --------------------
from input.stringEncryption import StringDecryptor
from input.nameIdentifier import IdentifierCleaner, detect_language
from input.controlFlow import FakeConditionCleaner
from input.deadCode import DeadCodeCleaner
from input.inlineExpansion import InlineExpansionCleaner
from input.opaquePredicate import OpaquePredicateCleaner
from input.instructionSubstitution import InstructionSubstitutionCleaner
from input.dynamicLoading import DynamicCodeLoaderCleaner
from input.junkCode import JunkCodeCleaner
from input.apiRedirection import ApiRedirectionCleaner
from input.mixedLanguage import MixedLanguageCleaner
from input.codeFlattening import CodeFlatteningCleaner

# -------------------- PDF EXPORT --------------------
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER


def save_pdf(results, pdf_path="output/combined_results.pdf"):
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name="TitleStyle", parent=styles["Heading1"], alignment=TA_CENTER, fontSize=16, spaceAfter=20
    )
    normal_style = ParagraphStyle(name="NormalStyle", parent=styles["Normal"], fontSize=11, leading=14)

    content = [Paragraph("🔍 Code Analysis Results", title_style), Spacer(1, 12)]
    for line in results.split("\n"):
        if line.strip().startswith("====="):
            content.append(PageBreak())
            content.append(Paragraph(line.strip(), styles["Heading2"]))
            content.append(Spacer(1, 12))
        else:
            content.append(Paragraph(line.replace("→", "->"), normal_style))
            content.append(Spacer(1, 6))
    doc.build(content)
    print(f"📄 PDF saved at {pdf_path}")


# -------------------- FILE ANALYSIS --------------------
def analyze_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()
    lang = detect_language(os.path.basename(filepath))

    # Unified result dictionary for all techniques
    results = {
        "String Encryption": [],
        "Identifier Cleaner": [],
        "Control Flow Flattening": [],
        "Dead Code": [],
        "Inline Expansion": [],
        "Opaque Predicates": [],
        "Instruction Substitution": [],
        "Dynamic Code Loading": [],
        "Junk Code": [],
        "API Redirection": [],
        "Mixed Language Obfuscation": [],
        "Code Flattening": [],
    }

    # Store all transformations in order
    transformations = [
        ("String Encryption", StringDecryptor()),
        ("Identifier Cleaner", IdentifierCleaner(language=lang)),
        ("Control Flow Flattening", FakeConditionCleaner()),
        ("Dead Code", DeadCodeCleaner()),
        ("Inline Expansion", InlineExpansionCleaner()),
        ("Opaque Predicates", OpaquePredicateCleaner()),
        ("Instruction Substitution", InstructionSubstitutionCleaner()),
        ("Dynamic Code Loading", DynamicCodeLoaderCleaner()),
        ("Junk Code", JunkCodeCleaner()),
        ("API Redirection", ApiRedirectionCleaner()),
        ("Mixed Language Obfuscation", MixedLanguageCleaner()),
        ("Code Flattening", CodeFlatteningCleaner()),
    ]

    current_code = code
    for technique, cleaner in transformations:
        try:
            changes = cleaner.clean_code(current_code)
            for c in changes:
                results[technique].append(
                    f"{filepath}: {c['original']} -> {c['cleaned']} ({c['reason']})"
                )
                current_code = current_code.replace(c['original'], c['cleaned'])
        except Exception as e:
            results[technique].append(f"{filepath}: Error while processing {technique}: {e}")

    return results


# -------------------- MAIN --------------------
def main():
    input_folder = "input"
    output_file = "output/combined_results.txt"
    os.makedirs("output", exist_ok=True)

    # Combine results for all files
    all_results = {
        "String Encryption": [],
        "Identifier Cleaner": [],
        "Control Flow Flattening": [],
        "Dead Code": [],
        "Inline Expansion": [],
        "Opaque Predicates": [],
        "Instruction Substitution": [],
        "Dynamic Code Loading": [],
        "Junk Code": [],
        "API Redirection": [],
        "Mixed Language Obfuscation": [],
        "Code Flattening": [],
    }

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if os.path.isdir(file_path):
            continue
        file_results = analyze_file(file_path)
        for key in all_results:
            all_results[key].extend(file_results[key])

    # Prepare final text report
    report_lines = []
    for technique, logs in all_results.items():
        report_lines.append(f"\n===== {technique} =====\n")
        if logs:
            report_lines.extend(logs)
        else:
            report_lines.append("No cases detected.\n")

    final_report = "\n".join(report_lines)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_report)

    save_pdf(final_report)
    print(f"✅ Analysis complete! Results saved in {output_file} and combined_results.pdf.")


if __name__ == "__main__":
    main()

    """




import os
import sys
import re
import ast
from io import StringIO

# ---------------- Custom modules ----------------
from input.nameIdentifier import IdentifierCleaner, detect_language
from input.controlFlow import FakeConditionCleaner
from input.stringEncryption import StringDecryptor
from input.deadCode import clean_deadcode_python, clean_deadcode_clike
from input.inlineExpansion import clean_inline_expansion_python, clean_inline_expansion_clike
from input.opaque_predicate import clean_opaque_predicate_python, clean_opaque_predicate_clike
from input.controlflow_flattening import clean_controlflow_flattening_python, clean_controlflow_flattening_clike
from input.instruction_substitution import clean_instruction_substitution_python, clean_instruction_substitution_clike
from input.dynamic_loading import clean_dynamic_code_loading_python, clean_dynamic_code_loading_clike
from input.junkcode import clean_junk_code_python, clean_junk_code_clike
from input.api_redirection import clean_api_redirection_python, clean_api_redirection_clike
from input.mixed_language import clean_mixed_language_python, clean_mixed_language_clike

# -------------------- PDF EXPORT --------------------
"""from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

def save_pdf(results, pdf_path="output/combined_results.pdf"):
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name="TitleStyle",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontSize=16,
        spaceAfter=20
    )
    normal_style = ParagraphStyle(
        name="NormalStyle",
        parent=styles["Normal"],
        fontSize=11,
        leading=14,
    )

    content = [Paragraph("🔍 Code Analysis Results", title_style), Spacer(1,12)]
    for line in results.split("\n"):
        if line.strip().startswith("====="):
            content.append(PageBreak())
            content.append(Paragraph(line.strip(), styles["Heading2"]))
            content.append(Spacer(1,12))
        else:
            content.append(Paragraph(line.replace("→","->"), normal_style))
            content.append(Spacer(1,6))

    doc.build(content)
    print(f"📄 PDF saved at {pdf_path}")
"""


# -------------------- PDF EXPORT --------------------
def save_pdf(results, pdf_path="output/combined_results.pdf"):
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER

    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name="TitleStyle",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontSize=16,
        spaceAfter=20
    )
    normal_style = ParagraphStyle(
        name="NormalStyle",
        parent=styles["Normal"],
        fontSize=11,
        leading=14,
    )

    content = [Paragraph("🔍 Code Analysis Results", title_style), Spacer(1,12)]

    for line in results.split("\n"):
        line = line.strip()
        if not line:
            continue  # skip empty lines
        if line.startswith("====="):
            content.append(PageBreak())
            content.append(Paragraph(line, styles["Heading2"]))
            content.append(Spacer(1,12))
        else:
            # Only include result lines, ignore full code blocks
            if "->" in line or "No cases detected." in line or "Error" in line:
                content.append(Paragraph(line.replace("→","->"), normal_style))
                content.append(Spacer(1,6))

    doc.build(content)
    print(f"📄 PDF saved at {pdf_path}")

# -------------------- FILE HANDLER --------------------
def analyze_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()
    lang = detect_language(os.path.basename(filepath))

    results = {
        "String Encryption": [],
        "Identifier Cleaner": [],
        "Control Flow": [],
        "Dead Code": [],
        "Inline Expansion": [],
        "Opaque Predicates": [],
        "Control Flow Flattening": [],
        "Instruction Substitution": [],
        "Dynamic Code Loading": [],
        "Junk Code": [],
        "API Redirection": [],
        "Mixed Language Obfuscation": [],
    }

    # ---------------- String Encryption ----------------
    str_cleaner = StringDecryptor()
    str_changes, code = str_cleaner.detect_and_clean(code)
    for c in str_changes:
        results["String Encryption"].append(f"{filepath}: {c['original']} -> {c['decrypted']} ({c['reason']})")

    # ---------------- Identifier Cleaner ----------------
    id_cleaner = IdentifierCleaner(language=lang)
    try:
        id_changes, code = id_cleaner.detect_and_clean(code)
    except SyntaxError as e:
        results["Identifier Cleaner"].append(f"{filepath}: Skipped due to syntax error: {e}")
        id_changes = []
    for c in id_changes:
        results["Identifier Cleaner"].append(f"{filepath}: {c['original']} -> {c['cleaned']} ({c['reason']})")

    # ---------------- Control Flow ----------------
    cf_cleaner = FakeConditionCleaner()
    cf_changes = cf_cleaner.clean_code(code)
    for c in cf_changes:
        results["Control Flow"].append(f"{filepath}: {c['original']} -> {c['cleaned']} ({c['reason']})")
        code = code.replace(c['original'], c['cleaned'])

    # ---------------- Other Techniques ----------------
    tech_map = {
        "Dead Code": (clean_deadcode_python, clean_deadcode_clike),
        "Inline Expansion": (clean_inline_expansion_python, clean_inline_expansion_clike),
        "Opaque Predicates": (clean_opaque_predicate_python, clean_opaque_predicate_clike),
        "Control Flow Flattening": (clean_controlflow_flattening_python, clean_controlflow_flattening_clike),
        "Instruction Substitution": (clean_instruction_substitution_python, clean_instruction_substitution_clike),
        "Dynamic Code Loading": (clean_dynamic_code_loading_python, clean_dynamic_code_loading_clike),
        "Junk Code": (clean_junk_code_python, clean_junk_code_clike),
        "API Redirection": (clean_api_redirection_python, clean_api_redirection_clike),
        "Mixed Language Obfuscation": (clean_mixed_language_python, clean_mixed_language_clike),
    }

    for name, (py_func, clike_func) in tech_map.items():
        try:
            if lang == "python":
                changes = py_func(code)
            else:
                changes = clike_func(code)
            for ch in changes:
                results[name].append(f"{filepath}: {ch['original']} -> {ch['cleaned']} ({ch['reason']})")
                code = code.replace(ch['original'], ch['cleaned'])
        except Exception as e:
            results[name].append(f"{filepath}: Error - {e}")

    return results

# -------------------- MAIN --------------------
def main():
    input_folder = "input"
    output_file = "output/combined_results.txt"
    os.makedirs("output", exist_ok=True)

    all_results = {
        "String Encryption": [],
        "Identifier Cleaner": [],
        "Control Flow": [],
        "Dead Code": [],
        "Inline Expansion": [],
        "Opaque Predicates": [],
        "Control Flow Flattening": [],
        "Instruction Substitution": [],
        "Dynamic Code Loading": [],
        "Junk Code": [],
        "API Redirection": [],
        "Mixed Language Obfuscation": [],
    }

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if os.path.isdir(file_path):
            continue
        file_results = analyze_file(file_path)
        for key in all_results:
            all_results[key].extend(file_results[key])

    # Prepare final uniform report
    report_lines = []
    for technique, cases in all_results.items():
        report_lines.append(f"\n===== {technique} =====\n")
        if cases:
            report_lines.extend(cases)
        else:
            report_lines.append("No cases detected.")
        report_lines.append("\n")

    final_report = "\n".join(report_lines)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_report)

    save_pdf(final_report)
    print(f"✅ Multi-language analysis complete. Results saved in {output_file} and PDF.")

if __name__ == "__main__":
    main()
