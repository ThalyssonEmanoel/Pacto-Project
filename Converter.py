import fitz
import re
import csv
import os
import matplotlib.pyplot as plt
import sys

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

def process_pdfs_in_folder(folder_path, csv_path):
    data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            texto = extract_text_from_pdf(pdf_path)

            valor_pattern = re.compile(r'Valor: R\$ ([\d.,]+)')
            valor_pago_pattern = re.compile(r'Valor Pago \(R\$ \): ([\d.,]+)')
            nome_destinatario_pattern = re.compile(r'Nome do destinatário: (.+)')
            nome_pagador_pattern = re.compile(r'Nome do Pagador: (.+)')
            solicitante_pattern = re.compile(r'Solicitante: (.+)')

            valor_match = valor_pattern.search(texto)
            if not valor_match:
                valor_match = valor_pago_pattern.search(texto)

            nome_destinatario_match = nome_destinatario_pattern.search(texto)
            if not nome_destinatario_match:
                nome_destinatario_match = nome_pagador_pattern.search(texto)

            solicitante_match = solicitante_pattern.search(texto)

            if valor_match and nome_destinatario_match and solicitante_match:
                valor = float(valor_match.group(1).replace('.', '').replace(',', '.'))
                nome_destinatario = nome_destinatario_match.group(1)
                solicitante = solicitante_match.group(1)
                
                if nome_destinatario in data:
                    data[nome_destinatario]['valor'] += valor
                else:
                    data[nome_destinatario] = {'valor': valor, 'solicitante': solicitante}

    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Valor', 'Solicitante'])
        for nome, info in data.items():
            writer.writerow([nome, f"{info['valor']:.2f}".replace('.', ','), info['solicitante']])

    print("Arquivo CSV criado com sucesso!")

def create_pie_chart_from_csv(csv_path):
    with open(csv_path, mode='r') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    
    if 'Valor' in data[0] and 'Nome' in data[0]:
        valor_key = 'Valor'
        nome_key = 'Nome'
    elif 'Valor Pago' in data[0] and 'Nome do Pagador' in data[0]:
        valor_key = 'Valor Pago'
        nome_key = 'Nome do Pagador'
    else:
        raise ValueError("CSV does not contain the required columns.")
    
    valores = [float(row[valor_key].replace('.', '').replace(',', '.')) for row in data]
    nomes = [f"{row[nome_key]} - R$ {row[valor_key]}" for row in data]

    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(valores, autopct='%1.1f%%', startangle=140)

    ax.legend(wedges, nomes, title="Nomes", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.setp(autotexts, size=10, weight="bold")
    ax.set_title('Distribuição de Valores')

    plt.show()
if len(sys.argv) > 1:
    folder_path = sys.argv[1]
else:
    folder_path = r'DESPESAS\4. Abril'

csv_path = r'../../dados.csv'

process_pdfs_in_folder(folder_path, csv_path)

create_pie_chart_from_csv(csv_path)