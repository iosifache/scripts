# `csv_to_latex`

## Description 🖼️

`csv_to_latex` is a script for converting a CSV table into a LaTeX one.

## Setup 🔧

1. Install Python 3.
2. Install the required libraries: `pip3 install -r requirements.txt`.

## Usage 🧰

By default, the script writes its output on the standard output. However, in the command below, which converts the CSV file identified by the name `INPUT_CSV` into the LaTeX representation and attaches the description `DESCRIPTION` and the label `LABEL`, writes the generated output into the file `OUTPUT_TEX`. This command was used for the test files (`input.csv` and `output.tex`) too.

1. Convert a CSV file: `csv_to_latex.py INPUT_CSV DESCRIPTION LABEL > OUTPUT_TEX`.