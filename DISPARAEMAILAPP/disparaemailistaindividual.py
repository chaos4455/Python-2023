import os
import re
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# Configurações do servidor SMTP da Hostinger
smtp_host = 'smtp-relay.brevo.com'
smtp_port = 465
smtp_username = 'evolucaoit@gmail.com'
smtp_password = 'LHNftYvsPOjK6m9k'

# Configurações do e-mail
sender_email = 'elias.andrade@evolucaoit.com.br'
subject = 'Apresentação de serviços de T.I - Consultoria e Serviços relevantes para operação e continuidade dos negócios da sua empresa'

# Lê o corpo do e-mail a partir do arquivo HTML
with open('templateemailmkt.html', 'r', encoding='utf-8') as file:
    html_body = file.read()

def extract_emails_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
        return emails

def send_email(receiver_email):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['Subject'] = subject

    # Adiciona o HTML ao corpo do e-mail
    message.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_username, smtp_password)

            message['To'] = receiver_email
            server.sendmail(sender_email, receiver_email, message.as_string())
            print(f'E-mail enviado para: {receiver_email}')

            # Criar log JSON
            log_data = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'status': 'success',
                'sender_email': sender_email,
                'subject': subject,
                'body': html_body,
                'sent_email': receiver_email
            }

            with open(f'email_log_{datetime.now().strftime("%Y%m%d%H%M%S")}.json', 'w', encoding='utf-8') as log_file:
                json.dump(log_data, log_file, ensure_ascii=False)

    except Exception as e:
        print(f'Erro ao enviar e-mail para {receiver_email}: {e}')

        # Criar log JSON em caso de erro
        log_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'error',
            'error_message': str(e),
            'sender_email': sender_email,
            'subject': subject,
            'body': html_body,
            'failed_email': receiver_email
        }

        with open(f'email_log_{datetime.now().strftime("%Y%m%d%H%M%S")}.json', 'w', encoding='utf-8') as log_file:
            json.dump(log_data, log_file, ensure_ascii=False)

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
