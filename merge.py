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


