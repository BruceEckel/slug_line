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
    # Init to False and exclude field from constructor arguments
    modified: bool = field(default=False, init=False)

    def true(self) -> "Changed":
        self.modified = True
        return self

    def false(self) -> "Changed":
        self.modified = False
        return self

    def report(self) -> str:
        if self.modified:
            return f"[bold red]{self.file_name}"
        return f"[bold green]{self.file_name}"


def ensure_slug_line(file_path: Path, full_path=False) -> Changed:
    """
    Create or update the slug line in the Python file: file_path
    """
    #print(file_path)
    changed = Changed(file_path.name)
    lines = file_path.read_text(encoding="utf-8").splitlines(True)
    filename = file_path if full_path else file_path.name
    correct_slug_line = f"#: {filename}\n"

    # Check if the first line is a slug line
    if lines and re.match(r"^#\:\s\w+\.py\n$", lines[0]):
        # Slug line exists, verify and correct if necessary
        if lines[0] != correct_slug_line:
            lines[0] = correct_slug_line
            file_path.write_text("".join(lines), encoding="utf-8")
            return changed.true()
        return changed.false()
    else:
        # Slug line doesn't exist, insert at top of file
        lines.insert(0, correct_slug_line)
        file_path.write_text("".join(lines), encoding="utf-8")
        return changed.true()


def main():
    parser = argparse.ArgumentParser(
        description="Create or update slug lines (commented file name at top) in Python files"
    )
    parser.add_argument('-r', '--recursive', action='store_true', help='recursively search for python files')
    parser.add_argument('-f', '--full-path', action='store_true', help='include full path in slug line')
    args = parser.parse_args()

    mask = "**/*.py" if args.recursive else "*.py"
    if not (code_files := list(Path(".").glob(mask))):
        console.print("No Python files found")
        return
    results = [ensure_slug_line(listing, args.full_path) for listing in code_files]
    for r in results:
        console.print(r.report())
    console.print(f"Number of changes: {sum(r.modified for r in results)}")


if __name__ == "__main__":
    main()
