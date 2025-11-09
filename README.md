# Agente Analista de Empresa

Projeto tem como objetivo criar um agente capaz de estruturar uma analise de empresas a partir de dados de laudos que estao disponiveis na CVM. O Agente em questao ira estruturar as informacoes relevantes do laudo em uma tabela excel.

## Objetivos

- [x] Configurar ambiente e modulos da aplicacao.
- [x] Decidir bibliotecas que irei utilizar.
- [x] Analisar melhor forma de tratar a informacao do laudo para o agente de forma mais entendivel, utilizando por exemplo o formato Markdown e RAG para evitar informacoes que promova alucinacoes.
- [ ] Elaborar algoritmo para o agente acessar as informacoes tratadas e responder de forma mais clara possivel.
- [ ] Criar testes automatizados para garantir a eficiencia do Agente.
- [ ] Criar interface para possibilitar usuario anexar os laudos e receber a analise da empresa.

## Bibliotecas

* PyMuPDF - Converter PDF para imagem.
* openai - Transcrever Imagens em Markdown.

## Configuracao do projeto

* Python 3.14.0

## Como rodar

`python src/main.py`

