import logging
import os
from conversor.ConversorImageToMarkDown import ConversorImageToMarkDownOpenAI
from conversor.ConversorPdfToMarkdown import ConversorPdfToMarkdown
from dotenv import load_dotenv

def main():
    load_dotenv()

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    numeric_level = getattr(logging, log_level, logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

    logging.getLogger().setLevel(numeric_level)

    logging.info("Iniciando Agente Analisador de Empresas...")

    conversor_image_to_markdown = ConversorImageToMarkDownOpenAI()
    conversorPdfToMarkdown = ConversorPdfToMarkdown(conversor_image_to_markdown)

    conversorPdfToMarkdown.convert_pdf_to_markdown()

if __name__ == "__main__":
    main()