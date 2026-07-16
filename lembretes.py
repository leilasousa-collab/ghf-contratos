"""
GHF - Lembretes para o DP
Envia e-mail de lembrete para fazer upload da planilha
"""

import os
import sys
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'dados', 'contratos.db')

# Configuracao
CONFIG = {
    'gmail_usuario': 'SEU_EMAIL@gmail.com',
    'gmail_senha': 'SUA_SENHA_DE_APP',
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email_dp': 'dp@grupohiperfarma.far.br'
}

def enviar_email(destinatario, assunto, corpo_html):
    """Envia e-mail"""
    if CONFIG['gmail_usuario'] == 'SEU_EMAIL@gmail.com':
        print(f"[SIMULADO] Email para {destinatario}: {assunto}")
        return True

    msg = MIMEMultipart('alternative')
    msg['From'] = CONFIG['gmail_usuario']
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo_html, 'html', 'utf-8'))

    try:
        server = smtplib.SMTP(CONFIG['smtp_server'], CONFIG['smtp_port'])
        server.starttls()
        server.login(CONFIG['gmail_usuario'], CONFIG['gmail_senha'])
        server.sendmail(CONFIG['gmail_usuario'], destinatario, msg.as_string())
        server.quit()
        print(f"Email enviado: {destinatario}")
        return True
    except Exception as e:
        print(f"Erro: {e}")
        return False

def verificar_e_enviar_lembrete():
    """Verifica se hoje e dia de lembrete e envia"""
    hoje = datetime.now()
    dia = hoje.day

    # Enviar lembrete nos dias 1 e 15
    if dia not in [1, 15]:
        print(f"Hoje e dia {dia}. Lembrete envia nos dias 1 e 15.")
        return False

    # Verificar se ja enviou hoje
    log_file = os.path.join(BASE_DIR, 'dados', 'log_lembretes.txt')
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            envios = f.readlines()
            for envio in envios:
                if f"{hoje.strftime('%Y-%m-%d')}" in envio:
                    print("Lembrete ja enviado hoje.")
                    return False

    # Buscar estatisticas
    conn = sqlite3.connect(DATABASE)
    stats = conn.execute('''
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN status_1 = 'pendente' OR status_2 = 'pendente' THEN 1 ELSE 0 END) as pendentes,
            SUM(CASE WHEN status_1 != 'pendente' AND status_2 != 'pendente' THEN 1 ELSE 0 END) as validados
        FROM colaboradores
    ''').fetchone()
    conn.close()

    total = stats[0] or 0
    pendentes = stats[1] or 0
    validados = stats[2] or 0

    # Montar mensagem
    periodo = "INICIO" if dia == 1 else "MEIO"
    assunto = f"GHF - Lembrete: Atualizar dados - Periodo {periodo} de {hoje.strftime('%B/%Y')}"

    corpo_html = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"></head>
    <body style="margin:0; padding:0; font-family: Arial, sans-serif; background-color: #f5f5f5;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5; padding: 20px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">

                        <!-- Cabecalho -->
                        <tr>
                            <td style="background-color: #1A1A1A; padding: 20px; text-align: center;">
                                <h1 style="color: #FFD700; margin: 0; font-size: 24px;">GHF</h1>
                                <p style="color: #999; margin: 5px 0 0 0;">Sistema de Controle de Experiencia</p>
                            </td>
                        </tr>

                        <!-- Titulo -->
                        <tr>
                            <td style="background-color: #CC0000; padding: 15px; text-align: center;">
                                <span style="color: white; font-size: 18px; font-weight: bold;">
                                    LEMBRETE - ATUALIZAR DADOS
                                </span>
                            </td>
                        </tr>

                        <!-- Conteudo -->
                        <tr>
                            <td style="padding: 30px;">
                                <p style="font-size: 16px; color: #333;">Prezado(a) Departamento Pessoal,</p>

                                <p style="font-size: 14px; color: #555;">
                                    Hoje e <strong>dia {hoje.strftime('%d/%m/%Y')}</strong> e chegou a hora de atualizar
                                    os dados dos colaboradores no sistema GHF.
                                </p>

                                <div style="background-color: #FFF8E1; border: 1px solid #FFD700; border-radius: 8px; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #333;">
                                        <strong>Periodo:</strong> {periodo} do mes<br>
                                        <strong>Acao necessaria:</strong> Upload da planilha do Alterdata
                                    </p>
                                </div>

                                <!-- Status Atual -->
                                <h3 style="color: #1A1A1A; border-bottom: 2px solid #FFD700; padding-bottom: 10px;">
                                    Status Atual
                                </h3>
                                <table width="100%" cellpadding="10" cellspacing="0" style="border-collapse: collapse;">
                                    <tr style="background-color: #f9f9f9;">
                                        <td style="border: 1px solid #ddd; font-weight: bold;">Total Colaboradores</td>
                                        <td style="border: 1px solid #ddd; text-align: center; font-size: 18px; font-weight: bold;">{total}</td>
                                    </tr>
                                    <tr>
                                        <td style="border: 1px solid #ddd; font-weight: bold;">Pendentes</td>
                                        <td style="border: 1px solid #ddd; text-align: center; font-size: 18px; font-weight: bold; color: #CC0000;">{pendentes}</td>
                                    </tr>
                                    <tr style="background-color: #f9f9f9;">
                                        <td style="border: 1px solid #ddd; font-weight: bold;">Validados</td>
                                        <td style="border: 1px solid #ddd; text-align: center; font-size: 18px; font-weight: bold; color: #1A1A1A;">{validados}</td>
                                    </tr>
                                </table>

                                <!-- Passo a passo -->
                                <h3 style="color: #1A1A1A; border-bottom: 2px solid #FFD700; padding-bottom: 10px; margin-top: 20px;">
                                    Como Atualizar
                                </h3>
                                <ol style="color: #555; line-height: 1.8;">
                                    <li>Acesse o sistema GHF</li>
                                    <li>Clique em <strong>"Atualizar"</strong> no menu</li>
                                    <li>Clique em <strong>"Selecionar Arquivo"</strong></li>
                                    <li>Escolha a planilha exportada do Alterdata</li>
                                    <li>Clique em <strong>"Atualizar Dados"</strong></li>
                                </ol>

                                <!-- Botao -->
                                <table width="100%" cellpadding="0" cellspacing="0">
                                    <tr>
                                        <td align="center" style="padding: 20px 0;">
                                            <a href="http://localhost:5000/atualizar"
                                               style="background-color: #FFD700; color: #1A1A1A; padding: 15px 40px;
                                                      text-decoration: none; border-radius: 5px; font-size: 16px;
                                                      font-weight: bold; display: inline-block;">
                                                Acessar Sistema e Atualizar
                                            </a>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>

                        <!-- Rodape -->
                        <tr>
                            <td style="background-color: #f5f5f5; padding: 15px; text-align: center; border-top: 1px solid #e0e0e0;">
                                <p style="color: #999; font-size: 12px; margin: 0;">
                                    GHF - Sistema de Controle de Experiencia<br>
                                    Lembrete automatico - Dia {hoje.strftime('%d/%m/%Y')}
                                </p>
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>"""

    # Enviar
    enviar_email(CONFIG['email_dp'], assunto, corpo_html)

    # Registrar envio
    with open(log_file, 'a') as f:
        f.write(f"{hoje.strftime('%Y-%m-%d %H:%M:%S')} - Lembrete enviado para {CONFIG['email_dp']}\n")

    print(f"Lembrete enviado para {CONFIG['email_dp']}")
    return True

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'forcar':
        # Forcar envio mesmo sem ser dia 1 ou 15
        print("Forcando envio de lembrete...")
        CONFIG['email_dp'] = sys.argv[2] if len(sys.argv) > 2 else CONFIG['email_dp']

        # Enviar direto
        from datetime import datetime
        hoje = datetime.now()

        conn = sqlite3.connect(DATABASE)
        stats = conn.execute('''
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN status_1 = 'pendente' OR status_2 = 'pendente' THEN 1 ELSE 0 END) as pendentes
            FROM colaboradores
        ''').fetchone()
        conn.close()

        print(f"Enviando lembrete para: {CONFIG['email_dp']}")
        print(f"Total: {stats[0]}, Pendentes: {stats[1]}")

        # Gerar e enviar email de teste
        assunto = "GHF - TESTE - Lembrete de Atualizacao"
        corpo = "<h1>Este e um teste do lembrete GHF</h1><p>Se voce recebeu, o sistema esta funcionando!</p>"
        enviar_email(CONFIG['email_dp'], assunto, corpo)
        print("Email de teste enviado!")
    else:
        verificar_e_enviar_lembrete()
