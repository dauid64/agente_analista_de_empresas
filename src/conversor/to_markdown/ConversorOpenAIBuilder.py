import os
from openai import OpenAI
from typing import Optional

from conversor.to_markdown.ConversorBuilder import ConversorBuilder
from conversor.to_markdown.ConversorOpenAI import ConversorOpenAI


class ConversorOpenAIBuilder(ConversorBuilder):
    def __init__(self):
        super().__init__()
        self._current_conversor: Optional[ConversorOpenAI] = None

    def build_conversor(self):
        self._current_conversor = ConversorOpenAI()
        return self

    def with_client(self):
        if self._current_conversor is None:
            raise ValueError("Chame build_conversor() primeiro")
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API key não fornecida")
        
        self._current_conversor.client = OpenAI(api_key=api_key)
        return self

    def with_model(self, model_name: str):
        if self._current_conversor is None:
            raise ValueError("Chame build_conversor() primeiro")
        self._current_conversor.model = model_name
        return self

    def with_markdown_output_dir(self, output_dir: str):
        if self._current_conversor is None:
            raise ValueError("Chame build_conversor() primeiro")
        self._current_conversor.output_dir = output_dir
        return self
    
    def with_pdf_path(self, pdf_path: str):
        if self._current_conversor is None:
            raise ValueError("Chame build_conversor() primeiro")
        self._current_conversor.pdf_path = pdf_path
        return self
    
    def with_image_output_dir(self, image_output_dir: str):
        if self._current_conversor is None:
            raise ValueError("Chame build_conversor() primeiro")
        self._current_conversor.image_output_dir = image_output_dir
        return self

    def get_conversor(self) -> ConversorOpenAI:
        if self._current_conversor is None:
            raise ValueError("Chame build_conversor() primeiro")
        if self._current_conversor.client is None:
            raise ValueError("Client não foi configurado")
        if self._current_conversor.model is None:
            raise ValueError("Model não foi configurado")
        if self._current_conversor.output_dir is None:
            raise ValueError("Output directory não foi configurado")
        if self._current_conversor.pdf_path is None:
            raise ValueError("PDF path não foi configurado")
        if self._current_conversor.image_output_dir is None:
            raise ValueError("Image output directory não foi configurado")
        return self._current_conversor
