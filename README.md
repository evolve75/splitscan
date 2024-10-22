# PDF Page Splitter

This Python script is designed to split each page of a scanned PDF document, where each page contains two facing pages,
into individual pages. It converts the PDF to images, splits each image into left and right halves, and saves the result
as a new PDF file with separate pages. The script includes a progress bar when run interactively to provide feedback on
the process.

## Features

- Splits a PDF with scanned facing pages into individual pages.
- Converts each page into an image, splits it, and saves the result as a new PDF.
- Displays a progress bar in interactive terminal sessions.
- Provides detailed error messages for file issues (missing files, invalid formats, etc.).

## Requirements

This script requires the following Python libraries:

- `PyPDF2`
- `pdf2image`
- `Pillow` (PIL)
- `tqdm` (for the progress bar)

You can install these dependencies using `pip`:

```bash
pip install PyPDF2 pdf2image Pillow tqdm
```

Additionally, the `pdf2image` library requires the installation of `poppler`. You can install `poppler` as follows:

- **macOS**:
    ```bash
    brew install poppler
    ```
- **Ubuntu**:
    ```bash
    sudo apt-get install poppler-utils
    ```
- **Windows**: Download `poppler` binaries from [here](http://blog.alivate.com.au/poppler-windows/) and add the bin
    folder to your system PATH.

## Usage

### Command-line Arguments

The script accepts two arguments:

1. The path to the **input PDF file**.
2. The path to the **output PDF file**.

### Example

To run the script, use the following command:

```bash
python split_pdf.py input.pdf output.pdf
```

Where:

- `input.pdf` is the path to the PDF file that you want to split.
- `output.pdf` is the path where the resulting PDF will be saved.

### Progress Bar

If the script is run in an interactive terminal, it will display a progress bar that shows the number of pages being
processed. The progress bar will automatically adjust based on the interactivity of the terminal.

### Help

You can display the help message by running:

```bash
python split_pdf.py --help
```

This will display usage information, including the arguments accepted by the script:

```
usage: split_pdf.py [-h] input_pdf output_pdf

Split a PDF containing two scanned pages per page into individual pages.

positional arguments:
  input_pdf   Path to the input PDF file.
  output_pdf  Path to the output PDF file.

optional arguments:
  -h, --help  show this help message and exit
```

## Exit Codes

The script provides meaningful exit codes to indicate the outcome of the execution:

- `0`: Success.
- `1`: General error or unexpected issue.
- `2`: Input-related error (e.g., file not found, invalid format).
- `3`: Output-related error (e.g., unable to write output file or invalid output directory).

## Error Handling

The script will output appropriate error messages if:

- The input PDF file does not exist.
- The input file is not a PDF.
- There is an issue writing the output PDF.
- The script encounters unexpected issues during execution.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
