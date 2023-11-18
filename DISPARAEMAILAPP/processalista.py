#esse arquivo processa ums lista de email extraida das planilhas do site listaempresas.com.br em formato txt e consegue identificar emails e exportar só os emails

import os
import re

def extract_emails_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
        return emails

def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                emails = extract_emails_from_file(file_path)
                if emails:
                    # Nome do arquivo de origem sem a extensão
                    original_file_name = os.path.splitext(file_name)[0]

                    # Nome do arquivo exportado
                    output_filename = f'listaemailprocessada_{original_file_name}.txt'

                    print(f'E-mails encontrados no arquivo {file_name}:')
                    for email in emails:
                        print(email)

                    # Salva todos os e-mails em um arquivo com o nome do arquivo de origem
                    with open(output_filename, 'w', encoding='utf-8') as output_file:
                        for email in emails:
                            output_file.write(f'{email}\n')

                    print(f'Lista de e-mails processada e salva em: {output_filename}')

if __name__ == "__main__":
    directory_to_process = 'listaemailbruta'
    process_directory(directory_to_process)
