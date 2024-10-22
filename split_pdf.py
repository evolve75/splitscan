#!/usr/bin/env python
#
# split_pdf:
#
# Splits a PDF file containing two scanned physical pages in a single
# PDF, and generates a new PDF with a single physical page per PDF
# page. The pages are collated in the correct order.
#
# Author: Anupam Sengupta (anupamsg@gmail.com)
#
# Copyright (C) 2024

import os
import sys
import argparse
from PyPDF2 import PdfWriter, PdfReader
from pdf2image import convert_from_path, exceptions as pdf2image_exceptions
from PIL import UnidentifiedImageError
import io


def split_pdf_pages(input_pdf_path, output_pdf_path):
    """
    Splits each page of a PDF file, where each page contains two facing pages,
    into individual pages, and saves the result as a new PDF file.

    Args:
        input_pdf_path (str): Path to the input PDF file.
        output_pdf_path (str): Path to save the output PDF with split pages.

    Returns:
        None
    """
    writer = PdfWriter()

    try:
        # Convert PDF to images (handle potential PDF conversion issues)
        images = convert_from_path(input_pdf_path)

        for img in images:
            width, height = img.size

            # Defensive programming: Check if image is not empty
            if width == 0 or height == 0:
                print("Error: Image from page is empty or invalid.")
                sys.exit(1)

            # Split into left and right halves
            left_half = img.crop((0, 0, width // 2, height))
            right_half = img.crop((width // 2, 0, width, height))

            # Save left half as a new PDF page
            left_pdf_bytes = io.BytesIO()
            left_half.save(left_pdf_bytes, format="PDF")
            writer.add_page(PdfReader(left_pdf_bytes).pages[0])

            # Save right half as a new PDF page
            right_pdf_bytes = io.BytesIO()
            right_half.save(right_pdf_bytes, format="PDF")
            writer.add_page(PdfReader(right_pdf_bytes).pages[0])

    except pdf2image_exceptions.PDFPageCountError:
        print(f"Error: The file '{input_pdf_path}' could not be processed as a valid PDF.")
        sys.exit(2)

    except UnidentifiedImageError as e:
        print(f"Error: An error occurred while converting the PDF pages to images: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        sys.exit(1)

    try:
        # Write all pages to the output PDF
        with open(output_pdf_path, 'wb') as output_pdf:
            writer.write(output_pdf)
    except Exception as e:
        print(f"Error: Failed to write the output file '{output_pdf_path}': {e}")
        sys.exit(3)

    # If everything goes well, return 0 (success)
    print(f"Successfully split the pages and saved to '{output_pdf_path}'")
    sys.exit(0)


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Split a PDF containing two scanned pages per page into individual pages."
    )
    parser.add_argument(
        "input_pdf",
        help="Path to the input PDF file."
    )
    parser.add_argument(
        "output_pdf",
        help="Path to the output PDF file."
    )

    # Parse the arguments
    args = parser.parse_args()

    input_pdf = args.input_pdf
    output_pdf = args.output_pdf

    # Check if input file exists
    if not os.path.isfile(input_pdf):
        print(f"Error: The input file '{input_pdf}' was not found.")
        sys.exit(2)

    # Check if input file is a PDF
    if not input_pdf.lower().endswith('.pdf'):
        print("Error: The input file must be a PDF.")
        sys.exit(2)

    # Defensive programming: Check if the output file directory is valid
    output_dir = os.path.dirname(output_pdf)
    if output_dir and not os.path.isdir(output_dir):
        print(f"Error: The directory for the output file '{output_pdf}' does not exist.")
        sys.exit(3)

    # Call the function to split the PDF pages
    try:
        split_pdf_pages(input_pdf, output_pdf)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
