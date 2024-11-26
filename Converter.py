import fitz
import re
import csv

pdf_path = r'C:\Thalysson\VisualCodeScripts\Códigos\github\Pacto-Project\Pacto Financias\DESPESAS\4. Abril\1. Edilaine- Férias 2 R$ 2.592,56.pdf'

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

texto = extract_text_from_pdf(pdf_path)

valor_pattern = re.compile(r'Valor: R\$ ([\d.,]+)')
nome_destinatario_pattern = re.compile(r'Nome do destinatário: (.+)')
solicitante_pattern = re.compile(r'Solicitante: (.+)')

valor = valor_pattern.search(texto).group(1)
nome_destinatario = nome_destinatario_pattern.search(texto).group(1)
solicitante = solicitante_pattern.search(texto).group(1)

csv_path = r'C:\Thalysson\VisualCodeScripts\Códigos\github\Pacto-Project\dados.csv'

with open(csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Nome', 'Valor', 'Solicitante'])
    writer.writerow([nome_destinatario, valor, solicitante])

print("Arquivo CSV criado com sucesso!")