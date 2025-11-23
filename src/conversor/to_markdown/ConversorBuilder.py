from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from conversor.to_markdown.ConversorStrategy import ConversorStrategy


class ConversorBuilder(ABC):
    @abstractmethod
    def with_client(self) -> ConversorBuilder:
        pass

    @abstractmethod
    def with_model(self, model_name: str) -> ConversorBuilder:
        pass
    
    @abstractmethod
    def with_markdown_output_dir(self, output_dir: str) -> ConversorBuilder:
        pass
    
    @abstractmethod
    def with_pdf_path(self, pdf_path: str) -> ConversorBuilder:
        pass
    
    @abstractmethod
    def with_image_output_dir(self, image_output_dir: str) -> ConversorBuilder:
        pass

    @abstractmethod
    def get_conversor(self) -> ConversorStrategy:
        pass