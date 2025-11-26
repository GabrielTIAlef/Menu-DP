#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
import json
import os
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
from pathlib import Path

diretorio_log = r"C:\Users\Gabriel Alef\Projeto\dados"
os.makedirs(diretorio_log, exist_ok=True)
log_arquivo = os.path.join(diretorio_log, "processo_gestta.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_arquivo, encoding='utf-8'),
        logging.StreamHandler()
    ]
)


def enviar_mensagem_slack(mensagem):
    webhook_url = "https://hooks.slack.com/services/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"
    slack_data = {"text": mensagem}
    try:
        response = requests.post(
            webhook_url, data=json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            logging.error(f"Erro: {response.status_code}, {response.text}")
    except Exception as e:
        logging.error(f"Erro: {e}")

url = "https://api.gestta.com.br/core/customer/task/report"
TOKEN = Path(r"G:\Drives compartilhados\1. Departamentos - Análise de Dados\TokenGestta.txt").read_text(encoding="utf-8").strip()
headers = {
    "authorization": f"{TOKEN}",
    "Content-Type": "application/json"
}

json_arquivo = os.path.join(diretorio_log, "gestta_relatorios.json")
csv_arquivo = os.path.join(diretorio_log, "gestta_relatorios.csv")

# Montagem dos períodos desejados
ano_atual = datetime.now().year
ano_anterior = ano_atual - 1
ano_seguinte = ano_atual + 1
fuso = "-03:00"

periodos = [
    (f"{ano_anterior}-01-01", f"{ano_anterior}-06-30"),
    (f"{ano_anterior}-07-01", f"{ano_anterior}-12-31"),
    (f"{ano_atual}-01-01", f"{ano_atual}-06-30"),
    (f"{ano_atual}-07-01", f"{ano_atual}-12-31"),
    (f"{ano_seguinte}-01-01", f"{ano_seguinte}-06-30"),
    (f"{ano_seguinte}-07-01", f"{ano_seguinte}-12-31")
]

dados_gerais = []

# Loop sobre cada período de até 6 meses
for inicio, fim in periodos:
    start_date = f"{inicio}T00:00:00{fuso}"
    end_date = f"{fim}T23:59:59{fuso}"
    
    payload = {
        "type": "CUSTOMER_TASK",
        "filter": "CURRENT_MONTH",
        "dates": {
            "startDate": start_date,
            "endDate": end_date
        }
    }

    try:
        logging.info(f"Iniciando requisição {inicio} a {fim}...")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()

        # Coleta e normalização dos dados
        if isinstance(data, list):
            df = pd.json_normalize(data)
        else:
            df = pd.json_normalize(data.get("data", data))

        if not df.empty:
            dados_gerais.append(df)
            logging.info(f"Período {inicio} a {fim} processado")
        else:
            logging.warning(f"Nenhum dado para o período {inicio} a {fim}.")

    except requests.exceptions.RequestException as err:
        msg = f"Erro na requisição ({inicio} a {fim}): {err}"
        logging.error(msg)
        enviar_mensagem_slack(f"ERRO no script Gestta ({inicio} a {fim}): {err}")
    except Exception as e:
        msg = f"Erro ao processar período ({inicio} a {fim}): {e}"
        logging.error(msg)
        enviar_mensagem_slack(f"ERRO no processamento do script Gestta ({inicio} a {fim}): {e}")

# Salvando os dados consolidados
if dados_gerais:
    df_final = pd.concat(dados_gerais, ignore_index=True)
    df_final.to_csv(csv_arquivo, index=False, encoding="utf-8-sig")
    with open(json_arquivo, "w", encoding="utf-8") as f:
        json.dump(df_final.to_dict(orient="records"), f, ensure_ascii=False, indent=2)
    logging.info("Dados salvos")
else:
    logging.warning("Nenhum dado coletado")


# In[4]:


import subprocess

subprocess.run(['python', r'C:\Users\Gabriel Alef\Projeto\Script\PBI_OS.py'])


# In[3]:


import subprocess

subprocess.run(['python', r'C:\Users\Gabriel Alef\Projeto\Script\RPA\RPA_Gestao_Atividades.py'])


# In[4]:


import subprocess

subprocess.run(['python', r'C:\Users\Gabriel Alef\Projeto\Script\RPA\RPA_Gestao_Supervisores.py'])


# In[ ]:




