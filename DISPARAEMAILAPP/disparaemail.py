import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import json

# Configurações do servidor SMTP da Hostinger
smtp_host = 'smtp.hostinger.com'
smtp_port = 465
smtp_username = 'login'
smtp_password = 'Senha'

# Configurações do e-mail
sender_email = 'elias.andrade@evolucaoit.com.br'
receiver_email = 'elias.andrade@evolucaoit.com.br'
# subject = 'Apresentação da Evolução IT - Consultoria e Serviços em Tecnologia da Informação'
subject = 'Apresentação de serviços de T.I - Consultoria e Serviços relevantes para operação e contunidade dos negócios da sua empresa'

# Lê o corpo do e-mail a partir do arquivo HTML
with open('templatefinalpronto.html', 'r', encoding='utf-8') as file:
    html_body = file.read()

def send_email():
    # Configuração da mensagem
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Adiciona o HTML ao corpo do email
    message.attach(MIMEText(html_body, 'html'))

    try:
        # Conexão com o servidor SMTP usando SSL/TLS
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print('E-mail enviado com sucesso!')

        # Criar log JSON
        log_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'success',
            'sender_email': sender_email,
            'receiver_email': receiver_email,
            'subject': subject,
            'body': html_body
        }

        with open('email_log.json', 'a', encoding='utf-8') as log_file:
            json.dump(log_data, log_file, ensure_ascii=False)
            log_file.write('\n')

    except Exception as e:
        print(f'Erro ao enviar e-mail: {e}')

        # Criar log JSON em caso de erro
        log_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'error',
            'error_message': str(e),
            'sender_email': sender_email,
            'receiver_email': receiver_email,
            'subject': subject,
            'body': html_body
        }

        with open('email_log.json', 'a', encoding='utf-8') as log_file:
            json.dump(log_data, log_file, ensure_ascii=False)
            log_file.write('\n')

# Chamada da função para enviar o e-mail
send_email()
