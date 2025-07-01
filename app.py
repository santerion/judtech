import streamlit as st
import pandas as pd
import json # Adicionado para carregar dados do JSON
from processo_inventario.dados_do_processo import dados_processo
from processo_inventario.summary_and_timeline import summary_and_timeline

st.set_page_config(layout="wide")

dados_extracao_ia = summary_and_timeline

summary_text = dados_extracao_ia.get("summary", "Resumo não disponível.")
timeline_events = dados_extracao_ia.get("timeline", [])
current_status = dados_extracao_ia.get("current_status", "Status atual não disponível.")

# --- Sidebar Navigation ---
# st.sidebar.title("Navegação") # Removed
# pagina_selecionada = st.sidebar.radio( # Removed
#     "Selecione uma página:", # Removed
#     ["Capa do Processo", "Resumo", "Linha do Tempo"] # Removed
# ) # Removed

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
        st.write(f"**Fonte:** {dados_processo['fonte']}")
        st.write(f"**Classe:** {dados_processo['classe']}")
        st.write(f"**Assunto:** {dados_processo['assunto']}")
        st.write(f"**Foro:** {dados_processo['foro']}")
        st.write(f"**Vara:** {dados_processo['vara']}")
    with col2:
        st.write(f"**Juiz:** {dados_processo['juiz']}")
        st.write(f"**Distribuição:** {dados_processo['distribuicao']}")
        st.write(f"**Controle:** {dados_processo['controle']}")
        st.write(f"**Área:** {dados_processo['area']}")
        st.write(f"**Valor da Ação:** {dados_processo['valor_da_acao']}")

    

    st.subheader("Partes")
    partes_reqte, partes_reqda = st.columns(2)

    partes = dados_processo['partes']
    
    with partes_reqte:
        for parte in partes[::2]:  # Even indexed items (0, 2, 4, ...)
            st.markdown(f"**{parte['tipo']}**")
            st.write(f"**Nome:** {parte['nome']}")
            if len(parte['advogados']) > 0:
                st.write(f"Advogados:")
                for adv in parte['advogados']:
                    st.write(f"- {adv}")

    with partes_reqda:
        for parte in partes[1::2]:  # Odd indexed items (1, 3, 5, ...)
            st.markdown(f"**{parte['tipo']}**")
            st.write(f"**Nome:** {parte['nome']}")
            if len(parte['advogados']) > 0:
                st.write(f"Advogados:")
                for adv in parte['advogados']:
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