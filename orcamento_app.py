# MVP: Orçamento Estimado com Formulário Simples
# Linguagem: Python (Streamlit)

import streamlit as st
import re
import pandas as pd
import requests

@st.cache_data(ttl=86400)
def carregar_custos_sinapi():
    # Este CSV é gerado com base em dados reais da tabela SINAPI
    url = "https://raw.githubusercontent.com/datasets-br/custos-sinapi/main/custos-m2-simplificado.csv"
    df = pd.read_csv(url, sep=",")
    custos = {}
    for _, row in df.iterrows():
        uf = row["UF"].strip().upper()
        custos[uf] = {
            "Simples": row.get("Simples", 2200),
            "Médio": row.get("Medio", 2600),
            "Alto": row.get("Alto", 3200)
        }
    return custos

# Carrega os custos do SINAPI automaticamente
custos_por_estado = carregar_custos_sinapi()

# Banco de dados simplificado de cidades (IBGE ou outro CSV pode ser usado no futuro)
@st.cache_data
def carregar_cidades():
    url = "https://raw.githubusercontent.com/chandez/Estados-Cidades-IBGE/master/Cidades.json"
    cidades = requests.get(url).json()
    cidade_para_uf = {}
    for estado in cidades:
        uf = estado["sigla"]
        for cidade in estado["cidades"]:
            cidade_para_uf[cidade.strip().lower()] = uf
    return cidade_para_uf

cidade_para_uf = carregar_cidades()

# Percentual aproximado de cada etapa da obra
etapas = {
    "Fundação": 0.10,
    "Estrutura": 0.20,
    "Alvenaria": 0.15,
    "Cobertura": 0.10,
    "Instalações": 0.15,
    "Acabamentos": 0.30
}

st.title("Orçamento Estimado de Obra")

# Formulário de entrada
with st.form("formulario_orcamento"):
    tipo_obra = st.selectbox("Tipo de Obra", ["Casa Térrea", "Sobrado", "Comercial"])
    area = st.number_input("Área Construída (m²)", min_value=10.0, step=1.0)
    pavimentos = st.selectbox("Número de Pavimentos", [1, 2, 3])
    padrao = st.selectbox("Padrão de Acabamento", ["Simples", "Médio", "Alto"])
    local = st.text_input("Local da Obra (Cidade)")
    submitted = st.form_submit_button("Calcular Orçamento")

# Função para extrair a UF da cidade digitada
def extrair_uf(texto):
    texto = texto.strip().lower()
    return cidade_para_uf.get(texto, None)

# Cálculo do orçamento
if submitted:
    uf = extrair_uf(local)
    custos_estado = custos_por_estado.get(uf, custos_por_estado.get("DEFAULT", {"Simples": 2200, "Médio": 2600, "Alto": 3200}))
    custo_m2 = custos_estado.get(padrao, 2600)
    custo_total = custo_m2 * area

    st.subheader("Resumo do Orçamento")
    st.write(f"**Tipo de Obra:** {tipo_obra}")
    st.write(f"**Local:** {local.title()} ({uf if uf else 'UF não reconhecida'})")
    st.write(f"**Área:** {area:.2f} m²")
    st.write(f"**Padrão:** {padrao}")
    st.write(f"**Custo estimado por m²:** R$ {custo_m2:,.2f}")
    st.write(f"**Custo Total Estimado:** R$ {custo_total:,.2f}")

    st.subheader("Distribuição por Etapas")
    for etapa, percentual in etapas.items():
        valor = custo_total * percentual
        st.write(f"{etapa}: R$ {valor:,.2f} ({percentual*100:.0f}%)")
