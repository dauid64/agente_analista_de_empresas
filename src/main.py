import logging
import os
from conversor.to_markdown.ConversorOpenAIBuilder import ConversorOpenAIBuilder
from conversor.to_markdown.Conversor import Conversor
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

    conversor = Conversor()
    builder = ConversorOpenAIBuilder()

    conversor_openai = conversor.create_openai_conversor(builder)

    conversor_openai.convert()

if __name__ == "__main__":
    main()