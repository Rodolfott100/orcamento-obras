# MVP: Orçamento Estimado com Formulário Simples
# Linguagem: Python (Streamlit)

import streamlit as st
import re

# Custo por m² por estado (UF) e padrão de acabamento (valores simulados, base SINAPI)
custos_por_estado = {
    "AC": {"Simples": 1900, "Médio": 2300, "Alto": 2900},
    "AL": {"Simples": 1950, "Médio": 2350, "Alto": 2950},
    "AP": {"Simples": 1920, "Médio": 2320, "Alto": 2920},
    "AM": {"Simples": 2000, "Médio": 2400, "Alto": 3000},
    "BA": {"Simples": 2000, "Médio": 2400, "Alto": 3000},
    "CE": {"Simples": 1980, "Médio": 2380, "Alto": 2980},
    "DF": {"Simples": 2150, "Médio": 2550, "Alto": 3150},
    "ES": {"Simples": 2120, "Médio": 2520, "Alto": 3120},
    "GO": {"Simples": 2100, "Médio": 2500, "Alto": 3100},
    "MA": {"Simples": 1930, "Médio": 2330, "Alto": 2930},
    "MT": {"Simples": 2070, "Médio": 2470, "Alto": 3070},
    "MS": {"Simples": 2080, "Médio": 2480, "Alto": 3080},
    "MG": {"Simples": 2100, "Médio": 2500, "Alto": 3100},
    "PA": {"Simples": 2020, "Médio": 2420, "Alto": 3020},
    "PB": {"Simples": 1960, "Médio": 2360, "Alto": 2960},
    "PR": {"Simples": 2200, "Médio": 2600, "Alto": 3200},
    "PE": {"Simples": 1990, "Médio": 2390, "Alto": 2990},
    "PI": {"Simples": 1940, "Médio": 2340, "Alto": 2940},
    "RJ": {"Simples": 2250, "Médio": 2650, "Alto": 3300},
    "RN": {"Simples": 1970, "Médio": 2370, "Alto": 2970},
    "RS": {"Simples": 2180, "Médio": 2580, "Alto": 3180},
    "RO": {"Simples": 2050, "Médio": 2450, "Alto": 3050},
    "RR": {"Simples": 1910, "Médio": 2310, "Alto": 2910},
    "SC": {"Simples": 2170, "Médio": 2570, "Alto": 3170},
    "SP": {"Simples": 2300, "Médio": 2700, "Alto": 3400},
    "SE": {"Simples": 1950, "Médio": 2350, "Alto": 2950},
    "TO": {"Simples": 2060, "Médio": 2460, "Alto": 3060},
    "DEFAULT": {"Simples": 2200, "Médio": 2600, "Alto": 3200}
}

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
    local = st.text_input("Local da Obra (Cidade/UF)")
    submitted = st.form_submit_button("Calcular Orçamento")

# Função para extrair a sigla do estado (UF)
def extrair_uf(texto):
    match = re.search(r"\b([A-Z]{2})\b", texto.upper())
    return match.group(1) if match else None

# Cálculo do orçamento
if submitted:
    uf = extrair_uf(local)
    custos_estado = custos_por_estado.get(uf, custos_por_estado["DEFAULT"])
    custo_m2 = custos_estado.get(padrao, 2600)
    custo_total = custo_m2 * area

    st.subheader("Resumo do Orçamento")
    st.write(f"**Tipo de Obra:** {tipo_obra}")
    st.write(f"**Local:** {local} ({uf if uf else 'UF não reconhecida'})")
    st.write(f"**Área:** {area:.2f} m²")
    st.write(f"**Padrão:** {padrao}")
    st.write(f"**Custo estimado por m²:** R$ {custo_m2:,.2f}")
    st.write(f"**Custo Total Estimado:** R$ {custo_total:,.2f}")

    st.subheader("Distribuição por Etapas")
    for etapa, percentual in etapas.items():
        valor = custo_total * percentual
        st.write(f"{etapa}: R$ {valor:,.2f} ({percentual*100:.0f}%)")
