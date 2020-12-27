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
def create_page(name, file_name):
    packet = io.BytesIO()
    can = canvas.Canvas(packet)

    can.setFont('Roboto', 70)  # Setting the font and size of text.
    can.drawString(1000, 925, name)  # Drawing a string onto the page. (x, y, string)

    can.setFont('RobotoL', 48)
    can.drawString(2110, 925, name)


    # =======================================================================================================
    # Code to centre a string between a starting and ending coordinates.

    can.setFont('Roboto', 17)

    # You'll have to determine the following values with the help of the helper file, get_pdf_coordinates.py
    start = 210
    end = 646
    length_of_one_letter = 10  # Use some 'monospaced' font so that each letter will have the same length.
    y = 280

    mid = start + (end - start) / 2
    half_string_size = (len(name) / 2) * length_of_one_letter
    x = mid - half_string_size
    can.drawString(x, y, name)
    # =======================================================================================================

    can.save()  # Save the canvas

    packet.seek(0)
    # Creating a pdf with just the canvas we just created.
    new_pdf = PdfFileReader(packet)

    # Read your existing PDF (ticket.pdf)
    path = os.path.join(settings.BASE_DIR, f'scripts/{file_name}')
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
