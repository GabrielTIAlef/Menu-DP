#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from sqlalchemy import create_engine, text
from sqlalchemy.types import String, Text, Integer, Boolean
from datetime import datetime
import os
import requests
import json
from pathlib import Path
import pandas as pd

DB_CONFIG = {
    "usuario": "postgres",
    "senha": "...",
    "host": "localhost",
    "porta": "5432",
    "banco": "ProjetoImport"
}

checklist = [
    "2.1. Organização da Entrada do Cliente",
    "2.1. Cadastro de Cliente | Gestta | Fiscal",
    "2.1. Cadastro de Cliente | Gestta | Contábil",
    "2.1. Cadastro de Cliente | Gestta | Folha",
    "2.1. Atualizar Cadastro do Cliente na Domínio",
    "2.1. Conferir Documentação - Contabilidade Anterior",
    "2.1. Mover Pasta do Cliente para Clientes Ativos (Dropbox)",
    "2.1. Transferir contador responsável",
    "2.1. Organizar Documentação Inicial do Cliente",
    "2.1. Mapeamento do Cliente",
    "2.1. Passagem de Bastão do Cliente | Folha",
    "2.1. Passagem de Bastão do Cliente | Fiscal"
]

TOKEN = Path(r"G:\Drives compartilhados\1. Departamentos - Análise de Dados\TokenGestta.txt").read_text(encoding="utf-8").strip()

def conectar_banco():
    url = f"postgresql+psycopg2://{DB_CONFIG['usuario']}:{DB_CONFIG['senha']}@{DB_CONFIG['host']}:{DB_CONFIG['porta']}/{DB_CONFIG['banco']}"
    engine = create_engine(url)
    try:
        with engine.connect() as conn:
            print("Conexão feita")
        return engine
    except Exception as e:
        print(f"Erro: {e}")
        raise
        
def coluna_banco(engine):
    with engine.connect() as conn:
        df_banco = pd.read_sql(
            text("""SELECT tarefa__nome, tarefa__id FROM public.worflow_cs;"""), 
            conn 
        )
    return df_banco
        
def api(engine):
    headers = {
        "authorization": f"{TOKEN}",
        "Accept": "application/json",
    }

    df_banco = coluna_banco(engine)
    print(f"Linhas no banco: {len(df_banco)} IDs únicos: {df_banco['tarefa__id'].nunique()}")

    mask = df_banco["tarefa__nome"].isin(checklist)
    print(f"Linhas que batem com checklist: {mask.sum()}")

    ids_alvos = (
        df_banco.loc[mask, "tarefa__id"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
    )
    print(f"IDs únicos para consultar na API: {len(ids_alvos)}")
    if not ids_alvos:
        print("Nenhum ID a consultar")
        return pd.DataFrame(columns=["id","name","order","done"])
        
    linhas = []
    sem_lista = 0

    for idx, task_id in enumerate(ids_alvos, 1):
        url = f"https://api.gestta.com.br/core/customer/task/{task_id}"
        try:
            resp = requests.get(url, headers=headers, timeout=60)
            resp.raise_for_status()
            payload = resp.json()
        except requests.RequestException as e:
            print(f"ERRO {task_id}: {e}")
            continue

        passos = payload.get("customer_task_steps") or payload.get("data", {}).get("customer_task_steps", [])
        if not isinstance(passos, list) or len(passos) == 0:
            sem_lista += 1
            print(f"task {task_id} sem customer_task_step' ou lista vazia")
            continue
        
        for p in passos:
            linhas.append({
                "id": task_id,
                "name": p.get("name"),
                "order": p.get("order"),
                "done": bool(p.get("done")),
            })

    df_api = ( 
        pd.DataFrame(linhas, columns=["id", "name", "order", "done"])
          .sort_values(["id", "order"], na_position="last")
          .reset_index(drop=True)
    )

    df_db = df_api.rename(columns={"order": "step_order"}) 
    df_db.to_sql(
    "cs_check",
    con=engine,
    schema="public",
    if_exists="replace",
    index=False,
    method="multi",
    dtype={
        "id": String(24),
        "name": Text(),
        "step_order": Integer(),
        "done": Boolean(),
    },
    )
    
    print(f"Tasks consultadas: {len(ids_alvos)} sem steps: {sem_lista}")
    print(f"Linhas coletadas: {len(df_api)} tasks únicas no DF: {df_api['id'].nunique()}")

    return df_api

def main():
    engine = conectar_banco()
    df_banco = coluna_banco(engine)
    df_api = api(engine)

if __name__ == "__main__":
    main()

