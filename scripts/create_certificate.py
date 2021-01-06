from PyPDF2 import PdfFileWriter, PdfFileReader
import io
import os

from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Adding custom fonts. 1st parm is the name of the font and 2nd is the path to the ttf font file.
path = os.path.join(settings.BASE_DIR, 'scripts/RobotoMono-Medium.ttf')
pdfmetrics.registerFont(TTFont('Roboto', path))
path = os.path.join(settings.BASE_DIR, 'scripts/RobotoMono-Light.ttf')
pdfmetrics.registerFont(TTFont('RobotoL', path))


# Function to return a pdf page with the parameters added into it.
def create_page(name, affiliation):
    name = name.title()
    packet = io.BytesIO()
    can = canvas.Canvas(packet)

    # can.setFont('Roboto', 17)
    # can.drawString(345, 265, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    # =======================================================================================================
    # Code to centre a string between a starting and ending coordinates.
    font_size = 15
    can.setFont('Roboto', font_size)

    # You'll have to determine the following values with the help of the helper file, get_pdf_coordinates.py
    start = 500
    end = 720
    length_of_one_letter = 10  # Use some 'monospaced' font so that each letter will have the same length.
    y = 295

    mid = start + (end - start) / 2
    half_string_size = (len(name) / 2) * length_of_one_letter
    x = mid - half_string_size
    can.drawString(x, y, name)
    # =======================================================================================================

    # =======================================================================================================
    # Code to centre a string between a starting and ending coordinates.
    font_size = 17
    can.setFont('Roboto', font_size)

    # You'll have to determine the following values with the help of the helper file, get_pdf_coordinates.py
    start = 345
    end = 600
    length_of_one_letter = 10  # Use some 'monospaced' font so that each letter will have the same length.
    y = 265

    mid = start + (end - start) / 2
    half_string_size = (len(name) / 2) * length_of_one_letter
    x = mid - half_string_size
    can.drawString(x, y, affiliation)
    # =======================================================================================================

    can.save()  # Save the canvas

    packet.seek(0)
    # Creating a pdf with just the canvas we just created.
    new_pdf = PdfFileReader(packet)

    # Read your existing PDF (ticket.pdf)
    path = os.path.join(settings.BASE_DIR, 'scripts/participation_base.pdf')
    existing_pdf = PdfFileReader(open(path, "rb"))
    # Add the canvas on the existing page
    page = existing_pdf.getPage(0)
    page2 = new_pdf.getPage(0)
    page.mergePage(page2)

    return page


if __name__ == "__main__":
    output = PdfFileWriter()

    page = create_page("JERIN", "ticket.pdf")
    output.addPage(page)  # Adding that page to the pdf.

    # Writing it to a file.
    outputStream = open("certificate.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
