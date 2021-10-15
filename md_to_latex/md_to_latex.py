#!/usr/bin/env python3
"""Script for converting a Markdown file into a LaTeX one.

Usage:
    md_to_latex.py MD_FILENAME TEX_FILENAME
"""

import re
import sys

# Constants
ONE_LINER_MAPPING = {
    # Mathematical expressions
    r"\$(.*?)\$": r"$ \1 $",

    # Heading
    r"^# ((.)+)$": r"\\section{\1}",
    r"^## ((.)+)$": r"\\subsection{\1}",
    r"^### ((.)+)$": r"\\subsubsection{\1}",

    # Bold
    r"\*\*(.*?)\*\*": r"\\textbf{\1}",

    # Italic
    r"\*(.*?)\*": r"\\textit{\1}",

    # Inline code blocks
    r"`([^`]+)`": r"\\mintinline{text}{\1}",
    r"^\d\.": r"    \\item ",

    # Unordered lists
    r"^-": r"    \\item",

    # Links
    r"(?<!\!)\[(.*?)\]\((.*?)\)": r"\1\\footnote{\\href{\2}{\2}}"
}
MULTILINE_MAPPING = {
    # Images, with replaced URL (the link is protected and not accessible)
    r"!\[.*\]\((.*)\)\n\n^(.*)$":
    r"""\\vspace{0.3cm}
\\begin{center}
    \\includegraphics[width=10cm]{}
    \\label{fig:1}
    \\captionsetup{justification=centering,margin=1cm}
    \\captionof{figure}{\2}
\\end{center}
\\vspace{0.3cm}"""
}


def main():
    """Main function."""
    # Check number of arguments
    if len(sys.argv) != 3:
        print("[+] Usage: {} MD_FILENAME TEX_FILE".format(sys.argv[0]))
        exit(1)

    with open(sys.argv[1], "r") as md_file:
        content = ""
        in_ordered_list = False
        in_unordered_list = False
        for line in md_file.readlines():
            # Detect the beginning of a list
            if not in_ordered_list and not in_unordered_list:

                (line,
                 itemize_count) = re.subn(r"^-",
                                          r"\\begin{itemize}\n    \\item",
                                          line)
                if itemize_count > 0:
                    in_ordered_list = True

                (line,
                 enumerate_count) = re.subn(r"^\d\.",
                                            r"\\begin{enumerate}\n    \\item",
                                            line)
                if enumerate_count > 0:
                    in_unordered_list = True

            # Apply all one-line regexes
            for key, value in ONE_LINER_MAPPING.items():
                line = re.sub(key, value, line)

            # Detect the end of a list
            if in_ordered_list and line == "\n":
                line = "\\end{itemize}\n\n"
                in_ordered_list = False
            if in_unordered_list and line == "\n":
                line = "\\end{enumerate}\n\n"
                in_unordered_list = False

            # Prepare for next line
            content += line

        # Check if all lists are closed
        if in_ordered_list:
            content += "\n\\end{itemize}\n"
        if in_unordered_list:
            content += "\n\\end{enumerate}\n"

        # Apply all multiline regexes
        for key, value in MULTILINE_MAPPING.items():
            content = re.sub(key, value, content, flags=re.MULTILINE)

        # Dump the content
        with open(sys.argv[2], "w") as tex_file:
            tex_file.write(content)
            print("[+] Success in converting the Markdown content.")


if __name__ == "__main__":
    main()
