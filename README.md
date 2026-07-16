# GHF - Sistema de Controle de Contratos de Experiencia

## Descricao
Sistema web para controle de contratos de experiencia de funcionarios, com envio automatico de alertas por e-mail e WhatsApp.

## Funcionalidades
- **Painel DP:** Visao geral de todos os contratos no Brasil
- **Painel Gestor:** Validacao de contratos da sua loja
- **Alertas Automaticos:** E-mail 7 dias antes do vencimento
- **Exportacao:** Planilha Excel com filtros
- **Controle por Acesso:** DP, Gestores e Regionais

## Instalacao

### Requisitos
- Python 3.8 ou superior
- Conexao com a internet (para dependencias)

### Passo a passo

1. **Copie a pasta do projeto** para o computador desejado

2. **Copie a planilha Excel** para a pasta `dados`:
   - Nome: `CONTRATO DE EXPERIENCIA.xlsx`
   - Ou `CONTRATO DE EXPERIENCIA 14.07.xls`

3. **Execute o instalador:**
   ```
   instalar.bat
   ```

4. **Inicie o sistema:**
   ```
   iniciar.bat
   ```

5. **Acesse no navegador:**
   ```
   http://localhost:5000
   ```

## Login Padrao
- **E-mail:** dp@ghf.com
- **Senha:** 123456

## Para Outros Computadores na Rede

### Na maquina que roda o sistema:
1. Execute `iniciar.bat`
2. Anote o IP exibido (ex: 192.168.1.100)

### Nos computadores dos colegas:
1. Abra o navegador
2. Acesse: `http://192.168.1.100:5000` (use o IP da maquina)

## Atualizar Dados
Quando a planilha Excel for atualizada pelo DP:
1. Copie a nova planilha para a pasta `dados`
2. Execute: `atualizar_dados.bat`

## Configurar Alertas por E-mail
1. Acesse: https://myaccount.google.com/apppasswords
2. Gere uma senha de app
3. Edite o arquivo `alerts.py`:
   ```python
   CONFIG = {
       'gmail_usuario': 'seu-email@gmail.com',
       'gmail_senha': 'sua-senha-de-app',
       ...
   }
   ```

## Estrutura de Pastas
```
projeto-ghf/
├── app.py                 # Backend principal
├── database.py            # Banco de dados
├── alerts.py              # Sistema de alertas
├── requirements.txt       # Dependencias
├── instalar.bat           # Instalador
├── iniciar.bat            # Iniciar sistema
├── atualizar_dados.bat    # Atualizar planilha
├── configurar_alertas.bat # Configurar e-mail
├── dados/                 # Planilha e banco
│   └── contratos.db       # Banco SQLite
├── templates/             # Paginas HTML
│   ├── base.html
│   ├── login.html
│   ├── dp_dashboard.html
│   ├── gestor_dashboard.html
│   └── usuarios.html
└── static/                # CSS e JS
    ├── css/
    └── js/
```

## Permissoes de Acesso

| Perfil | Acesso |
|--------|--------|
| **DP** | Visualiza e gerencia todos os colaboradores do Brasil |
| **Gestor** | Visualiza e valida apenas colaboradores da sua loja |
| **Regional** | Visualiza e valida colaboradores da sua regional |

## Suporte
Em caso de problemas, verifique:
1. Python esta instalado? `python --version`
2. Dependencias instaladas? Execute `instalar.bat` novamente
3. Planilha na pasta correta? Verifique a pasta `dados`
