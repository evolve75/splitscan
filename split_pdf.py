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


from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path
import io


def split_pdf_pages(input_pdf_path, output_pdf_path):
    """
    Splits each page of a PDF file, where each page contains two
    facing pages, into individual pages, and saves the result as a new
    PDF file.

    The input PDF is assumed to have scans of two facing pages on each
    page. This function splits the left and right halves of each
    scanned page into separate pages in the output PDF.

    Args:
        input_pdf_path (str): Path to the input PDF file.
        output_pdf_path (str): Path to save the output PDF with split pages.

    Returns:
        None

    """
    writer = PdfWriter()

    # Convert PDF to images
    images = convert_from_path(input_pdf_path)

    for img in images:
        width, height = img.size

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

    # Write all pages to the output PDF
    with open(output_pdf_path, 'wb') as output_pdf:
        writer.write(output_pdf)


if __name__ == "__main__":
    input_pdf = "input.pdf"  # Replace with your input file path
    output_pdf = "output.pdf"  # Replace with your desired output file path
    split_pdf_pages(input_pdf, output_pdf)
