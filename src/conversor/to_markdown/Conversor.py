from __future__ import annotations
import os
from typing import Optional, TYPE_CHECKING
from conversor.to_markdown.ConversorBuilder import ConversorBuilder
from conversor.to_markdown.ConversorStrategy import ConversorStrategy

if TYPE_CHECKING:
    from conversor.to_markdown.ConversorStrategy import ConversorStrategy

class Conversor():
    @staticmethod
    def create_openai_conversor(
        builder: ConversorBuilder,
        model: str = "gpt-4o",
        pdf_path: Optional[str] = None,
        image_output_dir: str = "data/openai/image",
        markdown_output_dir: str = "data/openai/markdown"
    ) -> ConversorStrategy:
        if pdf_path is None:
            pdf_name = os.getenv("PDF_NAME")
            if not pdf_name:
                raise ValueError("PDF_NAME não está definido nas variáveis de ambiente")
            pdf_path = os.getenv("PDF_PATH", "data/pdf/") + pdf_name

        return (builder
                .build_conversor()
                .with_client()
                .with_model(model)
                .with_pdf_path(pdf_path)
                .with_image_output_dir(image_output_dir)
                .with_markdown_output_dir(markdown_output_dir)
                .get_conversor())
        