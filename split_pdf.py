#!/usr/bin/env python
#
# split_pdf
#
# Author: Anupam Sengupta (anupamsg@gmail.com)
#
# Copyright (C) 2024

from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import io


def split_pdf_pages(input_pdf_path, output_pdf_path):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        # Extract the page as an image
        pdf_bytes = io.BytesIO()
        page_writer = PdfWriter()
        page_writer.add_page(page)
        page_writer.write(pdf_bytes)
        pdf_bytes.seek(0)

        # Open page as image using PIL
        img = Image.open(pdf_bytes)

        # Get page dimensions
        width, height = img.size

        # Split into left and right halves
        left_half = img.crop((0, 0, width // 2, height))
        right_half = img.crop((width // 2, 0, width, height))

        # Save left half as a new PDF page
        left_pdf_bytes = io.BytesIO()
        left_half.save(left_pdf_bytes, format="PDF")
        left_pdf_reader = PdfReader(left_pdf_bytes)
        writer.add_page(left_pdf_reader.pages[0])

        # Save right half as a new PDF page
        right_pdf_bytes = io.BytesIO()
        right_half.save(right_pdf_bytes, format="PDF")
        right_pdf_reader = PdfReader(right_pdf_bytes)
        writer.add_page(right_pdf_reader.pages[0])

    # Write all pages to the output PDF
    with open(output_pdf_path, 'wb') as output_pdf:
        writer.write(output_pdf)


if __name__ == "__main__":
    # Call the function with the input and output PDF paths
    split_pdf_pages("input.pdf", "output.pdf")
