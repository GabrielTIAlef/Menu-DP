# Menu DP automatizado – Projeto IZZI Contabilidade

> 🔹 *Automação completa entre Gestta, Notion, PostgreSQL e Power BI, integrando dados de clientes, tarefas e equipes em tempo real, com RPA e alertas via Slack.*

## 🚀 **Contexto e Objetivo**

Este projeto foi desenvolvido para resolver um dos principais desafios da gestão contábil moderna:  
**acompanhar a operação em tempo real** sem depender de atualizações manuais e planilhas.

A ideia nasceu da necessidade da equipe da **IZZI Contabilidade** de centralizar, automatizar e visualizar todos os fluxos de tarefas, clientes e times, com base em dados vindos de ferramentas que **não possuem APIs públicas completas**, como o **Gestta**.

## 🎯 **Solução Desenvolvida**

Foi construída uma **arquitetura completa de dados** que coleta, trata e integra informações automaticamente, com custo zero de licenças adicionais e taxa de atualização quase instantânea.

| Etapa | Ferramenta | Função |
|-------|-------------|--------|
| Coleta | **Python + API Gestta / API Notion** | Extrai dados brutos e transforma em DataFrames normalizados |
| Banco de Dados | **PostgreSQL** | Centraliza todas as tabelas e views relacionais |
| Automação | **Selenium (RPA Headless)** | Atualiza datasets do Power BI automaticamente |
| Comunicação | **Slack Webhook** | Envia alertas de erro e status das rotinas |
| Visualização | **Power BI** | Exibe painéis operacionais e estratégicos em tempo real |

## 🧩 Componentes Técnicos

🟩 gestta_relat.py

* Coleta relatórios de tarefas via API do Gestta para períodos semestrais.

* Faz logging, consolidação e alertas via Slack.

* Gera arquivos CSV e JSON padronizados.

🟦 base_not.py

* Conecta-se à API oficial do Notion, extrai propriedades dinâmicas (relation, people, date, etc).

* Converte os dados em formato relacional e insere no PostgreSQL.

* Automatiza a criação de colunas e mantém compatibilidade entre tabelas.

🟨 Operacional_BD.py

* Faz o ETL completo entre os dados de Gestta e Notion.

* Cria views SQL (bi_final e "Workflow_CS") para o Power BI.

* Exporta bases tratadas para Excel, mantendo rastreabilidade.

🟧 CS.py

* Consulta as tarefas de entrada de novos clientes (checklist 2.1) no Gestta.

* Valida a execução de cada etapa via API e grava status no banco.

* Permite análise de eficiência e gargalos no onboarding.

🟥 rpa.py

* Automatiza a atualização de datasets no Power BI Web, via Selenium Headless.

* Simula o clique em “Atualizar agora” nos relatórios necessários.

* Envia alertas no Slack em caso de timeout, erro ou sucesso.

## 💡 Resultados Concretos

| Métrica                               | Antes      | Depois da Automação         |
| ------------------------------------- | ---------- | --------------------------- |
| Tempo de atualização dos painéis      | 2h–3h      | ⏱️ < 5 minutos              |
| Dependência de planilhas manuais      | Alta       | Zero                        |
| Atualizações com erros                | Frequentes | Controladas via Slack       |
| Acesso entre equipes                  | Limitado   | Centralizado e automatizado |
| Custo mensal com ferramentas externas | 💰 +R$400  | 💸 R$0                      |

## 🧰 Stack Utilizada

* Python → pandas, requests, sqlalchemy, selenium, python-dotenv, logging

* Banco de dados → PostgreSQL

* APIs integradas → Gestta (não pública) e Notion (oficial)

* Visualização → Power BI

* Comunicação → Slack (webhook)

* Infraestrutura → Windows + Task Scheduler (execuções automáticas)

## 📈 Impacto Estratégico

Este projeto passou a ser a espinha dorsal dos painéis operacionais da IZZI,
permitindo que gestores e analistas acompanhem:

* Tempo médio de conclusão de tarefas;

* Eficiência por colaborador e setor;

* Gargalos entre departamentos (Contábil, Fiscal, Folha);

* Fluxo de entrada de clientes e desempenho de onboarding.

Além disso:

* Padronizou a comunicação entre áreas da empresa;

* Trouxe visão em tempo real da operação;

* Reduziu retrabalho e dependência de atualizações manuais;

* Criou uma base escalável para novos dashboards e automações.
