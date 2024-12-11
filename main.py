import PyPDF2
from lxml import etree


def collect_pdf_pages(file_path):
    print("Collecting PDF pages...")
    with open(file_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_text = [page.extract_text() for page in pdf_reader.pages]

    return pdf_text


def prepare_fb2():
    print("Preparing empty FB2...")
    fb2 = etree.Element("FictionBook", xmlns="http://www.gribuser.ru/xml/fictionbook/2.0")

    description = etree.SubElement(fb2, "description")
    title_info = etree.SubElement(description, "title-info")
    etree.SubElement(title_info, "author").text = "Author Name"
    etree.SubElement(title_info, "book-title").text = "Converted Book"

    return fb2


def convert_pages(pdf_pages, fb2):
    print("Writing pages to fb2...")
    fb2_body = etree.SubElement(fb2, "body")

    for i, page_text in enumerate(pdf_pages, start=1):
        section = etree.SubElement(fb2_body, "section")
        title = etree.SubElement(section, "title")
        etree.SubElement(title, "p").text = f"Page {i}"
        etree.SubElement(section, "p").text = page_text.strip()

        if i % 10 == 0:
            print(f"Wrote {i} pages...")

    return fb2_body


def pdf_to_fb2(pdf_file_path, fb2_file_path):
    pdf_pages = collect_pdf_pages(pdf_file_path)

    fb2 = prepare_fb2()
    fb2_body = convert_pages(pdf_pages, fb2)

    print("Saving final fb2 file...")
    with open(fb2_file_path, 'wb') as fb2_file:
        fb2_file.write(etree.tostring(fb2, pretty_print=True, encoding="utf-8", xml_declaration=True))


if __name__ == '__main__':
    pdf_to_fb2("example.pdf", "example.fb2")
