#Este arquivo na verdade cria o banco de controle de envios
#Confirmar se esse arquivo não é uma duplicata de versão desatualizada. 


import sqlite3
import os
import re
from datetime import datetime

def create_database():
    conn = sqlite3.connect('controledeenvios.db')
    cursor = conn.cursor()

    # Criar tabela se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS envios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            data_envio TEXT NOT NULL,
            nome_lista TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def insert_emails_to_database(emails, lista_nome):
    conn = sqlite3.connect('controledeenvios.db')
    cursor = conn.cursor()

    # Inserir e-mails no banco de dados
    for email in emails:
        cursor.execute('''
            INSERT INTO envios (email, data_envio, nome_lista)
            VALUES (?, ?, ?)
        ''', (email, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), lista_nome))

    conn.commit()
    conn.close()

def extract_emails_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
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
                    insert_emails_to_database(emails, file_name)

# Criar ou atualizar o banco de dados
create_database()

# Processar o diretório "enviados"
directory_to_process = 'enviados'
process_directory(directory_to_process)
