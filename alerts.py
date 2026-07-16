"""
GHF - Sistema de Alertas
Envio de notificacoes por E-mail e WhatsApp
"""

import os
import sys
import sqlite3
import smtplib
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'dados', 'contratos.db')

# ==================== CONFIGURACAO ====================
# Configuracao para WhatsApp (sem e-mail)
CONFIG = {
    'dias_alerta': 7,
    'url_sistema': 'http://localhost:5000',  # Alterar para o IP da maquina
    'usar_whatsapp': True,
    'usar_email': False  # Alterar para True quando configurar e-mail
}

# ==================== FUNCOES DE EMAIL ====================
def enviar_email(destinatario, assunto, corpo_html):
    """Envia e-mail (quando configurado)"""
    if not CONFIG.get('usar_email', False):
        print(f"[EMAIL DESABILITADO] Para: {destinatario}")
        return False

    if CONFIG.get('gmail_usuario') == 'SEU_EMAIL@gmail.com':
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
        print(f"Erro email {destinatario}: {e}")
        return False

# ==================== FUNCOES WHATSAPP ====================
def gerar_link_whatsapp(telefone, mensagem):
    """Gera link para envio via WhatsApp Web"""
    tel = ''.join(filter(str.isdigit, str(telefone)))
    if len(tel) == 11:
        tel = '55' + tel
    elif len(tel) == 10:
        tel = '55' + tel
    elif not tel.startswith('55'):
        tel = '55' + tel

    msg_encoded = urllib.parse.quote(mensagem)
    return f"https://api.whatsapp.com/send?phone={tel}&text={msg_encoded}"

def gerar_mensagem_whatsapp(colaborador, periodo, dias_restantes, url_painel):
    """Gera texto da mensagem WhatsApp"""
    if periodo == 1:
        acao_necessaria = "RENOVAR ou solicitar DESLIGAMENTO"
        tipo_periodo = "1o periodo (45 dias)"
    else:
        acao_necessaria = "EFETIVAR ou solicitar DESLIGAMENTO"
        tipo_periodo = "2o periodo (45+45 dias)"

    return f"""GHF - ALERTA DE EXPERIENCIA

Colaborador: {colaborador['nome']}
Funcao: {colaborador['funcao']}
Loja: {colaborador['departamento']}

Tipo: {tipo_periodo}
Vencimento: {colaborador[f'vencimento_{periodo}']}
Dias restantes: {dias_restantes}

Acao necessaria: {acao_necessaria}

Acesse o painel para validar:
{url_painel}"""

# ==================== TEMPLATES DE EMAIL ====================
def template_email_alerta(colaborador, periodo, dias_restantes, url_painel):
    """Gera HTML do email de alerta"""
    if periodo == 1:
        cor_tema = '#1976D2'
        acao_necessaria = 'Renovar ou Solicitar Desligamento'
        tipo_periodo = '1o Periodo (45 dias)'
    else:
        cor_tema = '#7B1FA2'
        acao_necessaria = 'Efetivar ou Solicitar Desligamento'
        tipo_periodo = '2o Periodo (45+45 dias)'

    if dias_restantes <= 0:
        cor_urgencia = '#d32f2f'
        texto_urgencia = 'VENCIDO'
    elif dias_restantes <= 3:
        cor_urgencia = '#d32f2f'
        texto_urgencia = 'URGENTE'
    elif dias_restantes <= 7:
        cor_urgencia = '#f57c00'
        texto_urgencia = 'ATENCAO'
    else:
        cor_urgencia = '#388e3c'
        texto_urgencia = 'PROGRAMADO'

    return f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"></head>
    <body style="margin:0; padding:0; font-family: Arial, Helvetica, sans-serif; background-color: #f5f5f5;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5; padding: 20px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">

                        <!-- Cabecalho -->
                        <tr>
                            <td style="background-color: {cor_tema}; padding: 20px; text-align: center;">
                                <h1 style="color: white; margin: 0; font-size: 24px;">GHF - Controle de Experiencia</h1>
                                <p style="color: rgba(255,255,255,0.9); margin: 5px 0 0 0;">Sistema de Alertas Automaticos</p>
                            </td>
                        </tr>

                        <!-- Banner Urgencia -->
                        <tr>
                            <td style="background-color: {cor_urgencia}; padding: 10px; text-align: center;">
                                <span style="color: white; font-size: 16px; font-weight: bold;">{texto_urgencia} - {dias_restantes} DIAS</span>
                            </td>
                        </tr>

                        <!-- Conteudo -->
                        <tr>
                            <td style="padding: 30px;">
                                <p style="font-size: 16px; color: #333;">Prezado(a),</p>
                                <p style="font-size: 14px; color: #555;">
                                    O colaborador abaixo possui contrato de experiencia vencendo em <strong>{dias_restantes} dia(s)</strong>.
                                    Acao necessaria: <strong>{acao_necessaria}</strong>
                                </p>

                                <!-- Card Colaborador -->
                                <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #fafafa; border: 1px solid #e0e0e0; border-radius: 8px; margin: 20px 0;">
                                    <tr>
                                        <td style="padding: 20px;">
                                            <h3 style="color: {cor_tema}; margin: 0 0 15px 0;">Dados do Colaborador</h3>
                                            <table width="100%" cellpadding="5" cellspacing="0">
                                                <tr>
                                                    <td style="font-weight: bold; color: #333; width: 140px;">Nome:</td>
                                                    <td style="color: #555;">{colaborador['nome']}</td>
                                                </tr>
                                                <tr>
                                                    <td style="font-weight: bold; color: #333;">Matricula:</td>
                                                    <td style="color: #555;">{colaborador['matricula']}</td>
                                                </tr>
                                                <tr>
                                                    <td style="font-weight: bold; color: #333;">Funcao:</td>
                                                    <td style="color: #555;">{colaborador['funcao']}</td>
                                                </tr>
                                                <tr>
                                                    <td style="font-weight: bold; color: #333;">Loja:</td>
                                                    <td style="color: #555;">{colaborador['departamento']}</td>
                                                </tr>
                                                <tr>
                                                    <td style="font-weight: bold; color: #333;">Periodo:</td>
                                                    <td style="color: #555;">{tipo_periodo}</td>
                                                </tr>
                                                <tr>
                                                    <td style="font-weight: bold; color: #333;">Vencimento:</td>
                                                    <td style="color: {cor_urgencia}; font-weight: bold;">{colaborador[f'vencimento_{periodo}']}</td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>

                                <!-- Botao Acao -->
                                <table width="100%" cellpadding="0" cellspacing="0">
                                    <tr>
                                        <td align="center" style="padding: 20px 0;">
                                            <a href="{url_painel}/gestor"
                                               style="background-color: {cor_tema}; color: white; padding: 15px 40px;
                                                      text-decoration: none; border-radius: 5px; font-size: 16px;
                                                      font-weight: bold; display: inline-block;">
                                                Acessar Painel de Validacao
                                            </a>
                                        </td>
                                    </tr>
                                </table>

                                <!-- Link WhatsApp -->
                                <table width="100%" cellpadding="0" cellspacing="0">
                                    <tr>
                                        <td align="center" style="padding: 10px 0;">
                                            <a href="{gerar_link_whatsapp(colaborador['celular'], gerar_mensagem_whatsapp(colaborador, periodo, dias_restantes, url_painel))}"
                                               style="background-color: #25D366; color: white; padding: 10px 30px;
                                                      text-decoration: none; border-radius: 5px; font-size: 14px;
                                                      display: inline-block;">
                                                Enviar via WhatsApp
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
                                    Sistema GHF - Controle de Experiencia<br>
                                    Este e-mail foi enviado automaticamente. Nao responda.
                                </p>
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>"""

# ==================== VERIFICACAO DE ALERTAS ====================
def verificar_e_enviar_alertas():
    """Verifica quais colaboradores precisam de alerta e envia"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    hoje = datetime.now().date()
    limite_alerta = hoje + timedelta(days=CONFIG['dias_alerta'])

    print(f"\nVerificando alertas - Hoje: {hoje}, Limite: {limite_alerta}")

    # Buscar gestores para mapear lojas -> emails
    gestores = {}
    for g in cursor.execute('SELECT loja, regional, email, nome FROM usuarios WHERE ativo = 1 AND perfil != "dp"').fetchall():
        if g['loja']:
            gestores[g['loja']] = {'email': g['email'], 'nome': g['nome']}
        if g['regional']:
            gestores[g['regional']] = {'email': g['email'], 'nome': g['nome']}

    # Periodo 1 - todos pendentes com vencimento proximo
    colaboradores_p1 = cursor.execute('''
        SELECT * FROM colaboradores
        WHERE status_1 = 'pendente'
        AND vencimento_1 IS NOT NULL
        AND date(vencimento_1) <= date(?)
        AND date(vencimento_1) >= date(?)
    ''', (limite_alerta.isoformat(), hoje.isoformat())).fetchall()

    # Periodo 2 - pendentes apos primeiro periodo validado
    colaboradores_p2 = cursor.execute('''
        SELECT * FROM colaboradores
        WHERE status_2 = 'pendente'
        AND status_1 != 'pendente'
        AND vencimento_2 IS NOT NULL
        AND date(vencimento_2) <= date(?)
        AND date(vencimento_2) >= date(?)
    ''', (limite_alerta.isoformat(), hoje.isoformat())).fetchall()

    enviados = 0

    # Processar Periodo 1
    for col in colaboradores_p1:
        vencimento = datetime.strptime(col['vencimento_1'], '%Y-%m-%d').date()
        dias_restantes = (vencimento - hoje).days

        # Verificar se ja enviou hoje
        ja_enviou = cursor.execute('''
            SELECT COUNT(*) FROM alertas_log
            WHERE colaborador_id = ? AND periodo = 1
            AND date(data_envio) = date('now')
        ''', (col['id'],)).fetchone()[0]

        if ja_enviou > 0:
            continue

        # Enviar email para o gestor da loja
        gestor = gestores.get(col['departamento']) or gestores.get(col['setor'])
        if gestor and gestor['email']:
            assunto = f"GHF: {colaborador_alerta(col, 1, dias_restantes)}"
            html = template_email_alerta(col, 1, dias_restantes, CONFIG['url_sistema'])

            if enviar_email(gestor['email'], assunto, html):
                cursor.execute('''
                    INSERT INTO alertas_log (colaborador_id, tipo, periodo)
                    VALUES (?, 'email', 1)
                ''', (col['id'],))
                enviados += 1

    # Processar Periodo 2
    for col in colaboradores_p2:
        vencimento = datetime.strptime(col['vencimento_2'], '%Y-%m-%d').date()
        dias_restantes = (vencimento - hoje).days

        ja_enviou = cursor.execute('''
            SELECT COUNT(*) FROM alertas_log
            WHERE colaborador_id = ? AND periodo = 2
            AND date(data_envio) = date('now')
        ''', (col['id'],)).fetchone()[0]

        if ja_enviou > 0:
            continue

        gestor = gestores.get(col['departamento']) or gestores.get(col['setor'])
        if gestor and gestor['email']:
            assunto = f"GHF: {colaborador_alerta(col, 2, dias_restantes)}"
            html = template_email_alerta(col, 2, dias_restantes, CONFIG['url_sistema'])

            if enviar_email(gestor['email'], assunto, html):
                cursor.execute('''
                    INSERT INTO alertas_log (colaborador_id, tipo, periodo)
                    VALUES (?, 'email', 2)
                ''', (col['id'],))
                enviados += 1

    conn.commit()
    conn.close()

    print(f"Alertas enviados: {enviados}")
    return enviados

def colaborador_alerta(col, periodo, dias_restantes):
    """Gera texto resumo do alerta"""
    tipo = "1o periodo" if periodo == 1 else "2o periodo"
    if dias_restantes <= 0:
        urgencia = "VENCIDO"
    elif dias_restantes <= 3:
        urgencia = "URGENTE"
    else:
        urgencia = "ATENCAO"
    return f"[{urgencia}] {col['nome']} - {tipo} vence em {dias_restantes} dias ({col['departamento']})"

# ==================== RELATORIO DE ALERTAS ====================
def relatorio_alertas():
    """Mostra relatorio de alertas enviados"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    total = conn.execute('SELECT COUNT(*) as c FROM alertas_log').fetchone()['c']
    hoje = conn.execute("SELECT COUNT(*) as c FROM alertas_log WHERE date(data_envio) = date('now')").fetchone()['c']
    periodo_1 = conn.execute('SELECT COUNT(*) as c FROM alertas_log WHERE periodo = 1').fetchone()['c']
    periodo_2 = conn.execute('SELECT COUNT(*) as c FROM alertas_log WHERE periodo = 2').fetchone()[0]

    conn.close()

    print("\n" + "=" * 40)
    print("  RELATORIO DE ALERTAS")
    print("=" * 40)
    print(f"  Total de alertas:    {total}")
    print(f"  Enviados hoje:       {hoje}")
    print(f"  Periodo 1:           {periodo_1}")
    print(f"  Periodo 2:           {periodo_2}")
    print("=" * 40)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == 'enviar':
            verificar_e_enviar_alertas()

        elif cmd == 'relatorio':
            relatorio_alertas()

        elif cmd == 'config':
            print("\nConfiguracao atual:")
            for k, v in CONFIG.items():
                print(f"  {k}: {v}")

        elif cmd == 'teste_email':
            email_teste = sys.argv[2] if len(sys.argv) > 2 else 'teste@teste.com'
            print(f"Enviando email de teste para {email_teste}...")
            html = template_email_alerta({
                'nome': 'FUNCIONARIO TESTE',
                'matricula': '000000',
                'funcao': 'CARGO TESTE',
                'departamento': 'LOJA TESTE',
                'vencimento_1': '2026-07-21',
                'vencimento_2': '2026-09-04'
            }, 1, 7, CONFIG['url_sistema'])
            enviar_email(email_teste, 'GHF: Teste de Alerta', html)
            print("Verifique sua caixa de entrada!")

        else:
            print("Comandos: enviar, relatorio, config, teste_email <email>")
    else:
        print("Uso: python alerts.py <comando>")
        print("  enviar         - Envia alertas pendentes")
        print("  relatorio      - Mostra relatorio de alertas")
        print("  config         - Mostra configuracao")
        print("  teste_email    - Envia email de teste")
