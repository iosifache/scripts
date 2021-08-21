"""Script for converting a CSV table into a LaTeX one.

Usage:
    csv_to_latex.py CSV_FILENAME DESCRIPTION LABEL
"""
#!/usr/bin/env python3

import re
import sys

import pandas

# Constants
LATEX_ESCAPE_MAPPING = {
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\^{}",
    "\\": r"\textbackslash{}",
    "<": r"\textless{}",
    ">": r"\textgreater{}",
}
TABLE_FORMAT = """\\vspace{{0.3cm}}
\\begin{{table}}[h]
    \\centering
    \\begin{{tabular}}{{ | {} | }}
        \\hline
        {}\t\\hline
    \\end{{tabular}}
    \\caption{{{}}}
    \\label{{tab:{}}}
\\end{{table}}
\\vspace{{0.3cm}}"""
HEADING_FORMAT = "{} \\\\\n\t\\hline\n"
COLUMN_FORMAT = "p{{{}\\linewidth}}"
LINE_FORMAT = "\t{} \\\\\n"
YES_NO_REPLACEMENTS = ["✅", "❌"]


def tex_escape(text: str) -> str:
    """Escapes the characters of a text to respect the LaTeX encoding.

    This function and LATEX_ESCAPE_MAPPING are taken from Stack Overflow [1].

    [1] https://stackoverflow.com/a/25875504

    Args:
        text (str): Text to escape

    Returns:
        str: Escaped text
    """
    regex = re.compile("|".join(
        re.escape(str(key)) for key in sorted(LATEX_ESCAPE_MAPPING.keys(),
                                              key=lambda item: -len(item))))

    return regex.sub(lambda match: LATEX_ESCAPE_MAPPING[match.group()], text)


def preprocess_cells(cell: str) -> str:
    """Process a cell before using it to populate the LaTeX table.

    Args:
        cell (str): Cell content

    Returns:
        str: Processed cell content
    """
    if cell == "Yes":
        return YES_NO_REPLACEMENTS[0]
    elif cell == "No":
        return YES_NO_REPLACEMENTS[1]
    else:
        return tex_escape(cell)


def main():
    """Main function."""
    # Check number of arguments
    if len(sys.argv) != 4:
        print("[+] Usage: {} CSV_FILENAME DESCRIPTION LABEL".format(
            sys.argv[0]))
        exit(1)
    csv_filename = sys.argv[1]
    description = sys.argv[2]
    label = sys.argv[3]

    # Read the CSV file
    table_df = pandas.read_csv(csv_filename)

    # Create the column definition
    columns_count = len(table_df.columns)
    columns_width = round(1 / columns_count, 2)
    columns_definition = " | ".join(columns_count
                                    * [COLUMN_FORMAT.format(columns_width)])

    # Create the table body
    table_body = HEADING_FORMAT.format(" & ".join(table_df.columns))
    for entry in table_df.values:
        entry = [preprocess_cells(str(cell)) for cell in entry]
        table_body += LINE_FORMAT.format(" & ".join(entry))

    # Create and output the table
    table = TABLE_FORMAT.format(columns_definition, table_body, description,
                                label)
    print(table)


if __name__ == "__main__":
    main()
