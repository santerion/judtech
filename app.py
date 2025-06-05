import streamlit as st
import pandas as pd
import json # Adicionado para carregar dados do JSON

st.set_page_config(layout="wide")

# Carregar dados do JSON
try:
    with open("summary_and_timeline.json", "r", encoding="utf-8") as f:
        dados_extracao_ia = json.load(f)
    summary_text = dados_extracao_ia.get("summary", "Resumo não disponível.")
    timeline_events = dados_extracao_ia.get("timeline", [])
    current_status = dados_extracao_ia.get("current_status", "Status atual não disponível.")
except FileNotFoundError:
    st.error("Arquivo 'summary_and_timeline.json' não encontrado. Certifique-se de que o arquivo está no mesmo diretório que app.py.")
    summary_text = "Erro ao carregar o resumo."
    timeline_events = []
except json.JSONDecodeError:
    st.error("Erro ao decodificar o arquivo JSON 'summary_and_timeline.json'. Verifique a formatação do arquivo.")
    summary_text = "Erro ao carregar o resumo."
    timeline_events = []

# --- Sidebar Navigation ---
# st.sidebar.title("Navegação") # Removed
# pagina_selecionada = st.sidebar.radio( # Removed
#     "Selecione uma página:", # Removed
#     ["Capa do Processo", "Resumo", "Linha do Tempo"] # Removed
# ) # Removed

# Dados do processo (substitua com os dados reais ou carregue de uma fonte)
dados_processo = {
    "numero_processo": "1008100-10.2021.8.26.0577",
    "tags": ["Extinto"],
    "classe": "Procedimento do Juizado Especial Cível",
    "assunto": "Interpretação / Revisão de Contrato",
    "foro": "Foro de São José dos Campos",
    "vara": "2ª Vara do Juizado Especial Cível",
    "juiz": "Fabricio Jose Pinto Dias",
    "partes": {
        "requerente": {
            "nome": "Jardel Fernandes da Silva",
            "advogado": "Oscar Berwanger Bohrer"
        },
        "requerida": {
            "nome": "FACEBOOK SERVIÇOS ONLINE DO BRASIL LTDA.",
            "advogados": [
                "Ciro Torres Freitas",
                "Priscila Oliveira Prado Faloppa",
                "Daniela Seadi Kessler"
            ]
        }
    },
    "movimentacoes": [
        {"data": "13/05/2024", "movimento": "Mudança de Magistrado", "detalhes": "Dr(a). Fabricio Jose Pinto Dias - (Vaga 2 - Juiz Titular II) para o(a) Dr(a). Fabricio Jose Pinto Dias - (Vaga 1 - Juiz Titular I) - Motivo: Alteração da vaga conforme CPA nº 2024/27952"},
        {"data": "26/07/2023", "movimento": "Arquivado Definitivamente", "detalhes": None},
        {"data": "26/07/2023", "movimento": "Certidão de Cartório Expedida", "detalhes": "Certifico que procedi ao cadastramento do incidente processual de cumprimento de sentença. Nada Mais."},
        {"data": "26/07/2023", "movimento": "Execução/Cumprimento de Sentença Iniciada (o)", "detalhes": "0011291-12.2023.8.26.0577 - Cumprimento de sentença"},
        {"data": "17/07/2023", "movimento": "Proferido Despacho de Mero Expediente", "detalhes": "Cadastre-se o incidente de cumprimento de sentença. Após, tornem os autos à conclusão."}
    ],
    "peticoes_diversas": [
        {"data": "25/05/2021", "tipo": "Contestação"},
        {"data": "02/06/2021", "tipo": "Contestação"},
        {"data": "15/06/2021", "tipo": "Manifestação Sobre a Contestação"},
        {"data": "09/07/2021", "tipo": "Indicação de Provas"},
        {"data": "13/07/2021", "tipo": "Petições Diversas"},
        {"data": "16/07/2021", "tipo": "Petições Diversas"},
        {"data": "26/09/2021", "tipo": "Petições Diversas"},
        {"data": "28/09/2021", "tipo": "Petições Diversas"},
        {"data": "20/10/2021", "tipo": "Petições Diversas"},
        {"data": "23/11/2021", "tipo": "Petições Diversas"},
        {"data": "24/11/2021", "tipo": "Pedido de Juntada de Procuração Substabelecimento"},
        {"data": "15/08/2022", "tipo": "Recurso Inominado"},
        {"data": "08/09/2022", "tipo": "Contrarrazões de Apelação"},
        {"data": "20/09/2022", "tipo": "Contrarrazões de Apelação"},
        {"data": "31/01/2023", "tipo": "Petição Intermediária"},
        {"data": "26/02/2023", "tipo": "Petições Diversas"},
        {"data": "08/03/2023", "tipo": "Petição Intermediária"},
        {"data": "08/06/2023", "tipo": "Petições Diversas"}
    ],
    "incidentes_etc": [
        {"recebido_em": "26/07/2023", "classe_incidente": "Cumprimento de sentença"} # Assumindo que o texto "0011291-12.2023.8.26.0577 - Cumprimento de sentença" se refere à classe
    ],
    "apensos_entranhados_unificados": "Não há processos apensados, entranhados e unificados a este processo.",
    "audiencias": [
        {"data": "25/11/2021", "audiencia_tipo": "Conciliação", "situacao": "Realizada", "qt_pessoas": 2}
    ]
}

# Cabeçalho com número do processo e tags
col1, col2, col3= st.columns([3, 1, 1])
with col1:
    st.header(f"Processo Nº: {dados_processo['numero_processo']}")
with col2:
    for tag in dados_processo['tags']:
        st.info(tag)

# --- Tab Navigation ---
tab1, tab2, tab3 = st.tabs(["Capa do Processo", "Resumo", "Linha do Tempo"])

# --- Exibição dos Dados ---

# if pagina_selecionada == "Resumo": # Changed to tab2
with tab2: # New
    st.subheader("Resumo do Processo")
    st.markdown(summary_text, unsafe_allow_html=True)

# elif pagina_selecionada == "Linha do Tempo": # Changed to tab3
with tab3: # New
    st.subheader("Linha do Tempo")
    with st.expander("Linha do tempo", expanded=True): # Expand by default for this page
        if timeline_events:
            df_timeline = pd.DataFrame(timeline_events)
            # Renomear colunas para melhor apresentação, se necessário
            df_timeline.columns = ["Data", "Evento", "Fls."]
            df_timeline = df_timeline.reset_index(drop=True) # Remove index
            styler_timeline = df_timeline.style.hide(axis="index")
            styler_timeline = styler_timeline.set_properties(**{'white-space': 'pre-wrap', 'text-align': 'left'})
            st.markdown(styler_timeline.to_html(), unsafe_allow_html=True)
        else:
            st.write("Linha do tempo não disponível ou vazia.")

    st.subheader("Status Atual do Processo")
    st.markdown(current_status, unsafe_allow_html=True)

# elif pagina_selecionada == "Capa do Processo": # Changed to tab1
with tab1: # New

    st.subheader("Sobre")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.write(f"**Classe:** {dados_processo['classe']}")
        st.write(f"**Assunto:** {dados_processo['assunto']}")
        st.write(f"**Juiz:** {dados_processo['juiz']}")
    with col2:
        st.write(f"**Foro:** {dados_processo['foro']}")
        st.write(f"**Vara:** {dados_processo['vara']}")

    

    st.subheader("Partes")
    partes_reqte, partes_reqda = st.columns(2)

    with partes_reqte:
        st.markdown("**Requerente**")
        st.write(f"**Nome:** {dados_processo['partes']['requerente']['nome']}")
        st.write(f"**Advogado:** {dados_processo['partes']['requerente']['advogado']}")

    with partes_reqda:
        st.markdown("**Requerida**")
        st.write(f"**Nome:** {dados_processo['partes']['requerida']['nome']}")
        st.write("**Advogados:**")
        for adv in dados_processo['partes']['requerida']['advogados']:
            st.write(f"- {adv}")

    st.subheader("Movimentações")
    with st.expander("Movimentações", expanded=False):
        # Convertendo lista de dicionários para DataFrame para melhor visualização em tabela
        df_movimentacoes = pd.DataFrame(dados_processo['movimentacoes'])
        df_movimentacoes = df_movimentacoes.reset_index(drop=True) # Remove index
        styler_movimentacoes = df_movimentacoes.style.hide(axis="index")
        styler_movimentacoes = styler_movimentacoes.set_properties(**{'white-space': 'pre-wrap'})
        st.markdown(styler_movimentacoes.to_html(), unsafe_allow_html=True)

    st.subheader("Petições Diversas")
    with st.expander("Petições Diversas"):
        df_peticoes = pd.DataFrame(dados_processo['peticoes_diversas'])
        df_peticoes = df_peticoes.reset_index(drop=True) # Remove index
        st.markdown(df_peticoes.style.hide(axis="index").to_html(), unsafe_allow_html=True)

    st.subheader("Incidentes, Ações Incidentais, Recursos e Execuções de Sentenças")
    with st.expander("Incidentes, Ações Incidentais, Recursos e Execuções de Sentenças"):
        if dados_processo['incidentes_etc']:
            df_incidentes = pd.DataFrame(dados_processo['incidentes_etc'])
            df_incidentes = df_incidentes.reset_index(drop=True) # Remove index
            st.markdown(df_incidentes.style.hide(axis="index").to_html(), unsafe_allow_html=True)
        else:
            st.write("Não há incidentes registrados.")

    st.subheader("Apensos, Entranhados e Unificados")
    with st.expander("Apensos, Entranhados e Unificados", expanded=False):
        st.write(dados_processo['apensos_entranhados_unificados'])

    st.subheader("Audiências")
    with st.expander("Audiências"):
        if dados_processo['audiencias']:
            df_audiencias = pd.DataFrame(dados_processo['audiencias'])
            df_audiencias = df_audiencias.reset_index(drop=True) # Remove index
            st.markdown(df_audiencias.style.hide(axis="index").to_html(), unsafe_allow_html=True)
        else:
            st.write("Não há audiências registradas.")