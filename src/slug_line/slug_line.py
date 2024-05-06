#: slug_line.py
import argparse
from pathlib import Path
import re
from dataclasses import dataclass, field
from rich.console import Console

console = Console()


@dataclass
class Changed:
    file_name: str
    # Set to False and exclude field from constructor arguments
    modified: bool = field(default=False, init=False)

    def true(self) -> "Changed":
        self.modified = True
        return self

    def false(self) -> "Changed":
        self.modified = False
        return self

    def report(self) -> str:
        assert self.modified is not None, "Must call true() or false() for Changed"
        if self.modified:
            return f"[bold red]{self.file_name}"
        return f"[bold green]{self.file_name}"


def ensure_slug_line(file_path: Path) -> Changed:
    """
    Create or update the slug line in the Python file: file_path
    """
    changed = Changed(file_path.name)
    lines = file_path.read_text(encoding="utf-8").splitlines(True)

    # Check if the first line is a slug line
    if lines and re.match(r"^#\:\s\w+\.py\n$", lines[0]):
        # Slug line exists, verify and correct if necessary
        correct_slug_line = f"#: {file_path.name}\n"
        if lines[0] != correct_slug_line:
            lines[0] = correct_slug_line
            file_path.write_text("".join(lines), encoding="utf-8")
            return changed.true()
        return changed.false()
    else:
        # Slug line doesn't exist, insert one at the beginning
        slug_line = f"#: {file_path.name}\n"
        lines.insert(0, slug_line)
        file_path.write_text("".join(lines), encoding="utf-8")
        return changed.true()


def main():
    argparse.ArgumentParser(
        description="Create or update slug lines in Python files (v 0.1)"
    ).parse_args()  # Provide -h help flag

    if not (code_files := list(Path(".").glob("*.py"))):
        console.print("No Python files found")
        return
    results = [ensure_slug_line(listing) for listing in code_files]
    for r in results:
        console.print(r.report())
    console.print(f"Number of changes: {sum(r.modified for r in results)}")


if __name__ == "__main__":
    main()
