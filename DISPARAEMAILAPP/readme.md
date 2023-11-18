# Disparador de E-mails em Massa

Bem-vindo ao projeto de Disparador de E-mails em Massa! Este aplicativo Python foi desenvolvido originalmente por mim  para processar listas de e-mails e realizar envios em larga escala de forma eficiente.

![:-)](https://raw.githubusercontent.com/chaos4455/Python-2023/main/DISPARAEMAILAPP/art.jpeg)


## Sobre o Projeto

Este projeto consiste em vários scripts Python que desempenham funções específicas para o disparo de e-mails em massa.

### 1. Criar Banco de Dados

- **Arquivo:** `criabancodecontroleenvio.py`
  
  Este script cria o banco de dados de controle de envios (`controledeenvios.db`) para armazenar informações sobre os e-mails enviados.

### 2. Processar Listas de Envios

- **Arquivo:** `disparalistaenvios.py`

  Este script processa listas de e-mails brutos, extrai os e-mails válidos e os salva no banco de dados, evitando envios duplicados.

### 3. Processar Listas de E-mails Extras

- **Arquivo:** `processalistaemailextra.py`

  Este script processa listas de e-mails extraídas de planilhas do site `listaempresas.com.br` em formato TXT. Ele identifica e exporta apenas os e-mails válidos.

### 4. Backup do Projeto

- **Arquivo:** `criabackupprojeto.py`

  Este script faz backup da pasta raiz do projeto, garantindo a integridade e possibilidade de restauração.

## Como Usar

1. **Criar Banco de Dados:**

   python criabancodecontroleenvio.py
Processar Listas de Envios:


python disparalistaenvios.py
Processar Listas de E-mails Extras:



python processalistaemailextra.py
Fazer Backup do Projeto:



python criabackupprojeto.py
Lembre-se de configurar suas chaves SMTP no arquivo chaves_smtp_brevo.txt para garantir o correto funcionamento do envio de e-mails.

Contato
Se você tiver alguma dúvida ou sugestão, entre em contato:

LinkedIn: Elias Andrade
E-mail: elias.andrade@evolucaoit.com.br
Obrigado por explorar o Disparador de E-mails em Massa! Este projeto faz parte do meu portfólio profissional e está em constante evolução.
