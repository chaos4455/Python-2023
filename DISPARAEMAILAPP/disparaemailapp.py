import os
import re
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import sqlite3

# Configurações do servidor SMTP da Hostinger
smtp_host = 'smtp-relay.brevo.com'
smtp_port = 465
smtp_username = 'evolucaoit@gmail.com'
smtp_password = 'LHNftYvsPOjK6m9k'

# Configurações do e-mail
sender_email = 'elias.andrade@evolucaoit.com.br'
#subject = 'Apresentação de serviços de T.I - Consultoria e Serviços relevantes para operação e continuidade dos negócios da sua empresa'
subject = 'Desenvolvimento de website corporativo por 199 R$ entregue em até 7 dias - Apresentação de serviço e proposta comercial'

# Lê o corpo do e-mail a partir do arquivo HTML
with open('templates//templatevendasitev3.html', 'r', encoding='utf-8') as file:
    html_body = file.read()

def extract_emails_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
        return emails

def is_email_contacted_recently(email, days=7):
    conn = sqlite3.connect('controledeenvios.db')
    cursor = conn.cursor()

    # Verificar se o e-mail foi contactado nos últimos 'days' dias
    cursor.execute('''
        SELECT COUNT(*) FROM envios
        WHERE email = ? AND data_envio >= ?
    ''', (email, (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")))

    count = cursor.fetchone()[0]

    conn.close()

    return count > 0

import sqlite3

def log_email_enviado(email):
    try:
        conn = sqlite3.connect('controledeenvios.db')
        cursor = conn.cursor()

        # Inserir o email enviado no banco de dados
        cursor.execute('''
            INSERT INTO envios (email, data_envio, nome_lista)
            VALUES (?, ?, ?)
        ''', (email, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'nome_da_sua_lista'))

        conn.commit()
        print(f'E-mail registrado no banco de dados: {email}')

    except Exception as e:
        print(f'Erro ao registrar e-mail no banco de dados: {e}')

    finally:
        conn.close()

def send_email(receiver_email, template_name='templatevendasitev3.html'):
    if is_email_contacted_recently(receiver_email):
        print(f'E-mail já foi contactado nos últimos 7 dias: {receiver_email}')
        return

    message = MIMEMultipart()
    message['From'] = sender_email
    message['Subject'] = subject

    # Lê o corpo do e-mail a partir do arquivo HTML
    with open(f'templates/{template_name}', 'r', encoding='utf-8') as file:
        html_body = file.read()

    # Adiciona o HTML ao corpo do e-mail
    message.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_username, smtp_password)

            message['To'] = receiver_email
            server.sendmail(sender_email, receiver_email, message.as_string())
            print(f'E-mail enviado para: {receiver_email}')

            # Registra o envio no banco de dados
            log_email_enviado(receiver_email, template_name)

    except Exception as e:
        print(f'Erro ao enviar e-mail para {receiver_email}: {e}')

        # Registra o erro no banco de dados
        log_email_enviado(receiver_email, template_name, status='error', error_message=str(e))

# Restante do código...

def log_email_enviado(email, template_name, status='success', error_message=None):
    try:
        # Criar log JSON
        log_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': status,
            'error_message': error_message,
            'sender_email': sender_email,
            'subject': subject,
            'template_name': template_name,
            'receiver_email': email,
        }

        # Escolha o diretório de log com base no status
        log_directory = 'log_json' if status == 'success' else 'log_json_errors'

        # Garanta que o diretório exista
        os.makedirs(log_directory, exist_ok=True)

        # Grave o JSON verticalmente
        log_file_path = os.path.join(log_directory, f'email_log_{datetime.now().strftime("%Y%m%d%H%M%S")}.json')
        with open(log_file_path, 'w', encoding='utf-8') as log_file:
            json.dump(log_data, log_file, indent=4, ensure_ascii=False)

        print(f'E-mail registrado no banco de dados: {email}')

    except Exception as e:
        print(f'Erro ao registrar e-mail no banco de dados: {e}')

# Restante do código...

def log_email_enviado(email, template_name, status='success', error_message=None):
    try:
        # Criar log JSON
        log_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': status,
            'error_message': error_message,
            'sender_email': sender_email,
            'subject': subject,
            'template_name': template_name,
            'receiver_email': email,
        }

        # Escolha o diretório de log com base no status
        log_directory = 'log_json' if status == 'success' else 'log_json_errors'

        # Garanta que o diretório exista
        os.makedirs(log_directory, exist_ok=True)

        # Grave o JSON verticalmente
        log_file_path = os.path.join(log_directory, f'email_log_{datetime.now().strftime("%Y%m%d%H%M%S")}.json')
        with open(log_file_path, 'w', encoding='utf-8') as log_file:
            json.dump(log_data, log_file, indent=4, ensure_ascii=False)

        print(f'E-mail registrado no banco de dados: {email}')

    except Exception as e:
        print(f'Erro ao registrar e-mail no banco de dados: {e}')


def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                emails = extract_emails_from_file(file_path)

                for email in emails:
                    # Envia o e-mail para cada destinatário
                    send_email(email)

# Diretório a ser processado
directory_to_process = 'listaenderecos'
process_directory(directory_to_process)
