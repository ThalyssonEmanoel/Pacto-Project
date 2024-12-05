import fitz
import re
import csv
import os
import matplotlib.pyplot as plt
import openpyxl
from openpyxl.drawing.image import Image

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    text = re.sub(r'\s+', ' ', text)
    return text

def process_pdfs_in_folder(folder_path, csv_path, excel_path):
    data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            texto = extract_text_from_pdf(pdf_path)

            valor_pattern = re.compile(r'Valor:?\s*R\$ ([\d.,]+)')
            nome_destinatario_pattern = re.compile(r'Nome do destinatário:?\s*(.+?)\s*(?:CPF|CNPJ|Valor|$)')

            valor_pago_pattern = re.compile(r'Valor Pago \(R\$ \):?\s*R\$ ([\d.,]+)')
            nome_pagador_pattern = re.compile(r'Nome do Pagador:?\s*(.+?)\s*(?:CPF|CNPJ|Valor|$)')

            match_valor = valor_pattern.search(texto)
            match_nome = nome_destinatario_pattern.search(texto)

            if match_valor and match_nome:
                valor = float(match_valor.group(1).replace('.', '').replace(',', '.'))
                nome = match_nome.group(1)
                if nome in data:
                    data[nome] += valor
                else:
                    data[nome] = valor

    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['Nome', 'Valor']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for nome, valor in data.items():
            writer.writerow({'Nome': nome, 'Valor': valor})

    nomes = list(data.keys())
    valores = list(data.values())
    plt.bar(nomes, valores)
    plt.xlabel('Nome')
    plt.ylabel('Valor')
    plt.title('Valores por Nome')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('src/images/grafico.png')

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    img = Image('src/images/grafico.png')
    sheet.add_image(img, 'A1')
    workbook.save(excel_path)

folder_path = r'DESPESAS\4. Abril'  
csv_path = r'src\data\dados.csv'
excel_path = r'src\data\graph.xlsx'
process_pdfs_in_folder(folder_path, csv_path, excel_path)