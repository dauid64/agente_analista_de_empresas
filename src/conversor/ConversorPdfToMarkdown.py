import logging
import os
import pymupdf

from conversor.ConversorImageToMarkDown import ConversorImageToMarkDownBase  # type: ignore


class ConversorPdfToMarkdown:
    def __init__(self, conversor_image_to_markdown: ConversorImageToMarkDownBase):
        self.pdf_name = os.getenv("PDF_NAME")
        if not self.pdf_name:
            raise ValueError(
                "A variável de ambiente PDF_NAME não está definida. Defina PDF_NAME com o nome do arquivo PDF (ex.: 'document.pdf').")

        self.pdf_path = os.getenv("PDF_PATH", "data/pdf/") + self.pdf_name
        self.image_output = os.getenv("IMAGE_OUTPUT_PATH", "data/image/")
        self.markdown_output = os.getenv(
            "MARKDOWN_OUTPUT_PATH", "data/markdown/")
        self.conversor_image_to_markdown = conversor_image_to_markdown

        logging.info(f"""
                    -------------
                     ConversorPdfToMarkdown inicializado com \n
                     PDF_NAME: {self.pdf_name} \n
                     PDF_PATH: {self.pdf_path} \n
                     IMAGE_OUTPUT_PATH: {self.image_output} \n
                     MARKDOWN_OUTPUT_PATH: {self.markdown_output}
                    -------------
        """)

    def convert_pdf_to_markdown(self):
        self._transform_pdf_to_image()
        self.conversor_image_to_markdown.convert_image_to_markdown(
            self.image_output)
        # self._clear_temp_files()
        return

    def _transform_pdf_to_image(self):
        logging.info("Transformando PDF em imagens...")
        doc = pymupdf.open(self.pdf_path)
        for page in doc:
            pix = page.get_pixmap()
            pix.save(f"{self.image_output}/page-{page.number}.png")
            logging.debug(
                f"Imagem salva em: {self.image_output}/page-{page.number}.png")
        logging.info("PDF transformado em imagens com sucesso!")
        return

    def _clear_temp_files(self):
        files = os.listdir(self.image_output)
        for file in files:
            os.remove(os.path.join(self.image_output, file))
