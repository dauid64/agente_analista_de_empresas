import logging
import os
import base64

from pathlib import Path
from abc import ABC, abstractmethod
from typing import Any
from openai import OpenAI


class ConversorImageToMarkDownBase(ABC):
    def __init__(self, client: Any, model: str):
        self.client = client
        self.model = model

    @abstractmethod
    def convert_image_to_markdown(self, image_path: str):
        pass


class ConversorImageToMarkDownOpenAI(ConversorImageToMarkDownBase):
    def __init__(self):
        super().__init__(
            client=OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            ),
            model="gpt-4.1",
        )

    def convert_image_to_markdown(self, image_path: str):
        path = Path(image_path)

        for file in path.iterdir():
            if file.is_file():  
                logging.debug(f"Processando imagem: {file.name}")
                encoded_image = self._encode_image_to_base64(file.read_bytes())
                markdown_content = self._transcribe_image_to_markdown(
                    encoded_image)
                markdown_name = file.name.split(".")[0]
                with open(f"data/markdown/{markdown_name}.md", "w", encoding="utf-8") as f:
                    f.write(markdown_content)
                    logging.debug(f"Markdown salvo em: data/markdown/{markdown_name}.md")
        return

    def _transcribe_image_to_markdown(self, encoded_image: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": """
                        You are a helpful assistant that converts images to Markdown format.
                        The images contains data about appraisal reports of companies.
                        Extract all relevant information from the images and format it in Markdown,
                        including any text, tables, graphics or other elements present in the images.
                    """,
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text", "text": "Convert the following image to Markdown format."
                        },
                        {
                            "type": "input_image",
                            "image_url": f"data:image/png;base64,{encoded_image}"
                        }
                    ]
                }
            ]
        )
        return response.output_text

    @staticmethod
    def _encode_image_to_base64(image: bytes) -> str:
        encoded_string = base64.b64encode(image).decode('utf-8')
        return encoded_string
