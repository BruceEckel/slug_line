#: slug_line.py
import argparse
from pathlib import Path
import re


def create_or_update_slug_line(file_path: Path) -> None:
    """
    Create or update the slug line in the Python file file_path.
    """
    # Read the contents of the file
    lines = file_path.read_text(encoding="utf-8").splitlines(True)

    # Check if the first line is a slug line
    if lines and re.match(r"^#\:\s\w+\.py\n$", lines[0]):
        # Slug line exists, verify and correct if necessary
        correct_slug_line = f"#: {file_path.name}\n"
        if lines[0] != correct_slug_line:
            lines[0] = correct_slug_line
            # Write the corrected contents back to the file
            file_path.write_text("".join(lines), encoding="utf-8")
    else:
        # Slug line doesn't exist, insert one at the beginning
        slug_line = f"#: {file_path.name}\n"
        lines.insert(0, slug_line)
        # Write the updated contents back to the file
        file_path.write_text("".join(lines), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create or update slug lines in Python files"
    )
    args = parser.parse_args()

    for file_path in Path(".").glob("*.py"):
        create_or_update_slug_line(file_path)
