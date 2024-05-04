#: slug_line.py
import argparse
from pathlib import Path
import re


def create_or_update_slug_line(file_path: Path) -> bool:
    """
    Create or update the slug line in the Python file: file_path.
    """
    print(f"Checking {file_path.name}", end=" ... ")
    lines = file_path.read_text(encoding="utf-8").splitlines(True)

    # Check if the first line is a slug line
    if lines and re.match(r"^#\:\s\w+\.py\n$", lines[0]):
        # Slug line exists, verify and correct if necessary
        correct_slug_line = f"#: {file_path.name}\n"
        if lines[0] != correct_slug_line:
            lines[0] = correct_slug_line
            file_path.write_text("".join(lines), encoding="utf-8")
            print("fixed")
            return True  # Update happened
        print("no change")
        return False  # No update
    else:
        # Slug line doesn't exist, insert one at the beginning
        slug_line = f"#: {file_path.name}\n"
        lines.insert(0, slug_line)
        file_path.write_text("".join(lines), encoding="utf-8")
        print("fixed")
        return True  # Slug line inserted

    print("no change")
    return False  # No update


def main():
    parser = argparse.ArgumentParser(
        description="Create or update slug lines in Python files"
    )
    parser.parse_args()

    code_files = list(Path(".").glob("*.py"))
    if not code_files:
        print("No Python files found")
        return
    results = [create_or_update_slug_line(code_file) for code_file in code_files]
    print(f"Number of changes: {results.count(True)}")


if __name__ == "__main__":
    main()
