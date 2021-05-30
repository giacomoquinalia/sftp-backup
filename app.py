import sys
import smtplib
import paramiko 

# Arquivo de log
paramiko.util.log_to_file("./backup_log.log")

# Variaveis
host = "test.rebex.net" # nome do host
port = 22 # porta
username = "demo" # user para logar
password = "password" # senha para logar

remote_path = [] # deixa assim
local_path = './' # Coloque o caminho onde vao ser baixados os arquivos


try:
    # Logando no host
    transport = paramiko.Transport((host, port))
    transport.connect(None, username, password)

    # Fazendo conexao sftp 
    sftp_client = paramiko.SFTPClient.from_transport(transport)

    # Pegando os arquivos do diretorio
    files = sftp_client.listdir(path="/bkp_synsuite/") # coloque o caminho todo ate onde estao os arquivos (somente ate a pasta pai dos arquivos)

    # Baixando os arquivos
    for file in files:
        local = local_path + file
        sftp_client.get(file, local)
    

    email_content = "SUCESSO ao fazer o backup!"
    subject_content = "Sucesso"
except:
    email_content = "FALHA ao fazer o backup!"
    subject_content = "Falha"


# Fachando conexao
try:
    sftp_client.close()
except NameError:
    pass


# Enviando email de resultado
with smtplib.SMTP('smtp.gmail.com', 587) as smtp:

    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login('email@gmail.com', 'password')

    subject = subject_content
    body = email_content
    msg = f'Subject: {subject}\n\n{body}'

    # coloque seu email no lugar de to@email.com
    smtp.sendmail('from@gmail.com', 'to@gmail.com', msg)


sys.exit()
