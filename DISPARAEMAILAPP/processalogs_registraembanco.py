#esse arquivo processa jsons na pasta log e alimenta o banco de controle de envio na tabela logs json e tabela envios para que o disparador nao envie spam no caso por padrão 7 dias, etc.
#Este arquivo deve ser processado diariamente toda vez que for feito envios para que atualize os bancos - 


import os
import json
import sqlite3
from datetime import datetime
import hashlib

# Conectar ao banco de dados
conn = sqlite3.connect('controledeenvios.db')
cursor = conn.cursor()

# Criar tabela 'envios' se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS envios (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        data_envio TEXT,
        nome_lista TEXT
    )
''')
conn.commit()

# Criar tabela 'log_json' se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS log_json (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        hashjson TEXT UNIQUE,
        nome_arquivo TEXT
    )
''')
conn.commit()

# Diretório onde os logs JSON estão localizados
logs_directory = 'log_json'

# Inicializa contador de e-mails enviados
total_emails_enviados = 0

# Pega a data atual
data_atual = datetime.now().strftime("%Y-%m-%d")

# Abre o arquivo de relatório para escrita
relatorio_file_path = f'relatorio_envios_{data_atual}.txt'
with open(relatorio_file_path, 'w', encoding='utf-8') as relatorio_file:
    # Percorre os arquivos no diretório de logs
    for file_name in os.listdir(logs_directory):
        if file_name.endswith('.json'):
            file_path = os.path.join(logs_directory, file_name)

            # Calcula a hash do arquivo
            hashjson = hashlib.md5(file_name.encode()).hexdigest()

            # Tenta inserir na tabela 'log_json'
            try:
                cursor.execute('''
                    INSERT INTO log_json (hashjson, nome_arquivo)
                    VALUES (?, ?)
                ''', (hashjson, file_name))
                conn.commit()
            except sqlite3.IntegrityError:
                # Se já existir, ignora
                pass

            # Lê o conteúdo do arquivo JSON
            with open(file_path, 'r', encoding='utf-8') as log_file:
                log_data = json.load(log_file)

                # Puxa o valor de 'template_name' ou define como 'nao_existe'
                nome_lista = log_data.get('template_name', 'nao_existe')

                # Verifica se o e-mail e a data existem no log
                if 'receiver_email' in log_data and 'timestamp' in log_data:
                    receiver_email = log_data['receiver_email']
                    timestamp = log_data['timestamp']

                    # Verifica se o e-mail e a data correspondem ao critério
                    if timestamp.startswith(data_atual):
                        # Verifica se o registro já existe na tabela 'envios'
                        check_query = f"SELECT COUNT(*) FROM envios WHERE email = '{receiver_email}' AND data_envio = '{timestamp}'"
                        cursor.execute(check_query)
                        count = cursor.fetchone()[0]

                        if count == 0:
                            # Se não existir, insere na tabela 'envios'
                            cursor.execute('''
                                INSERT INTO envios (email, data_envio, nome_lista)
                                VALUES (?, ?, ?)
                            ''', (receiver_email, timestamp, nome_lista))
                            conn.commit()

                            total_emails_enviados += 1

    # Escreve no relatório
    relatorio_file.write(f'Hoje, {data_atual}, foram enviados {total_emails_enviados} e-mails.\n')
    relatorio_file.write(f'Os e-mails foram registrados no banco de dados.\n')

# Fecha a conexão com o banco de dados
conn.close()
