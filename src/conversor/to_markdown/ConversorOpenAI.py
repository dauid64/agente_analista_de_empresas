import base64
import logging
import os
from typing import Optional

from pathlib import Path
from openai import OpenAI
import pymupdf

from conversor.to_markdown.ConversorStrategy import ConversorStrategy


class ConversorOpenAI(ConversorStrategy):
    def __init__(self):
        super().__init__()
        self.client : Optional[OpenAI] = None
        self.model: Optional[str] = None
        self.output_dir: Optional[str] = None
        self.pdf_path: Optional[str] = None
        self.image_output_dir: Optional[str] = None
    
    def convert(self):
        """Converte PDF para imagens e depois para Markdown."""
        if self.pdf_path is None:
            raise ValueError("PDF path não foi configurado")
        if self.image_output_dir is None:
            raise ValueError("Image output directory não foi configurado")
        if self.output_dir is None:
            raise ValueError("Output directory não foi configurado")
        
        logging.info("Iniciando conversão de PDF para Markdown...")
        self._convert_pdf_to_images()
        self._convert_images_to_markdown()
        # self._clear_temp_files()
        logging.info("Conversão concluída com sucesso!")
        return
    
    def _convert_pdf_to_images(self):
        """Converte cada página do PDF em uma imagem PNG."""
        logging.info(f"Transformando PDF em imagens: {self.pdf_path}")
        doc = pymupdf.open(self.pdf_path)
        for page in doc:
            pix = page.get_pixmap()
            output_path = f"{self.image_output_dir}/page-{page.number}.png"
            pix.save(output_path)
            logging.debug(f"Imagem salva em: {output_path}")
        doc.close()
        logging.info("PDF transformado em imagens com sucesso!")
        return

    def _convert_images_to_markdown(self):
        """Converte todas as imagens do diretório em arquivos Markdown."""
        if self.image_output_dir is None:
            raise ValueError("Image output directory não foi configurado")
        
        path = Path(self.image_output_dir)
        logging.info(f"Convertendo imagens para Markdown: {self.image_output_dir}")
        
        for file in sorted(path.iterdir()):
            if file.is_file() and file.suffix.lower() in ['.png', '.jpg', '.jpeg']:  
                logging.debug(f"Processando imagem: {file.name}")
                encoded_image = self._encode_image_to_base64(file.read_bytes())
                markdown_content = self._transcribe_image_to_markdown(encoded_image)
                markdown_name = file.stem
                output_path = f"{self.output_dir}/{markdown_name}.md"
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(markdown_content)
                    logging.debug(f"Markdown salvo em: {output_path}")
        logging.info("Imagens convertidas para Markdown com sucesso!")
        return
    
    def _clear_temp_files(self):
        """Remove arquivos temporários de imagens."""
        if self.image_output_dir is None:
            return
        
        path = Path(self.image_output_dir)
        for file in path.iterdir():
            if file.is_file():
                file.unlink()
                logging.debug(f"Arquivo temporário removido: {file}")
        logging.info("Arquivos temporários limpos.")
        return

    def _transcribe_image_to_markdown(self, encoded_image: str) -> str:
        if self.client is None:
            raise ValueError("client não foi inicializado")
        if self.model is None:
            raise ValueError("model não foi inicializado")
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful assistant that converts images to Markdown format.
The images contain data about appraisal reports of companies.
Extract all relevant information from the images and format it in Markdown,
including any text, tables, graphics or other elements present in the images."""
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Convert the following image to Markdown format."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ]
        )
        return response.choices[0].message.content or ""

    @staticmethod
    def _encode_image_to_base64(image: bytes) -> str:
        encoded_string = base64.b64encode(image).decode('utf-8')
        return encoded_string

