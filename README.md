# Pacto-Project

## Descrição
O Pacto-Project é uma ferramenta para extração e processamento de dados de arquivos PDF para fins de cálculo financeiro.

## Funcionalidades
- Extração de texto de arquivos PDF
- Processamento de múltiplos PDFs em uma pasta
- Armazenamento dos dados extraídos em um arquivo CSV
- Visualização de dados com gráficos

## Passo-a-Passo
1. Tenha o [Python3](https://www.python.org/downloads/) instalado na máquina.
2. Clone este projeto em uma pasta do seu computador:
    ```bash
    git clone <URL_DO_REPOSITORIO>
    ```
3. Crie um ambiente virtual na pasta raiz do projeto. Veja a documentação oficial do [Python](https://docs.python.org/pt-br/3/library/venv.html):
    ```bash
    python -m venv venv
    ```
4. Ative o ambiente virtual:
    - Windows:
        ```bash
        venv\Scripts\activate
        ```
    - macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
5. Baixe as dependências:
    ```bash
    pip install -r requirements.txt
    ```
6. Crie uma pasta chamada "DESPESAS" e coloque os arquivos PDF nela.
7. Os arquivos PDF devem conter os atributos "Valor" e "Nome do destinatário", exatamente como está escrito.
8. Execute o script para processar os PDFs e gerar o arquivo CSV:
    ```bash
    python Converter.py
    ```

## Mudanças pendentes
1. Encontrar uma maneira de executar o script sem precisar instalar as bibliotecas, ou substituí-las por bibliotecas nativas do Python.
2. Implementar novos atributos que poderão ser lidos, além de "Valor" e "Nome do destinatário".
3. Melhorar o gráfico.
4. Conseguir executar o script clicando em apenas 2 botões (arquivos .reg).

## Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.