# MVP: Orçamento Estimado com Formulário Simples
# Linguagem: Python (Streamlit)

import streamlit as st

# Dados de custo médio por m² (valores aproximados baseados no SINAPI para Lavras/MG)
custos_por_padrao = {
    "Simples": 2200,
    "Médio": 2600,
    "Alto": 3200
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
    padrao = st.selectbox("Padrão de Acabamento", list(custos_por_padrao.keys()))
    local = st.text_input("Local da Obra (Cidade/UF)")
    submitted = st.form_submit_button("Calcular Orçamento")

# Cálculo do orçamento
if submitted:
    custo_m2 = custos_por_padrao.get(padrao, 2500)
    custo_total = custo_m2 * area

    st.subheader("Resumo do Orçamento")
    st.write(f"**Tipo de Obra:** {tipo_obra}")
    st.write(f"**Local:** {local}")
    st.write(f"**Área:** {area:.2f} m²")
    st.write(f"**Padrão:** {padrao}")
    st.write(f"**Custo estimado por m²:** R$ {custo_m2:,.2f}")
    st.write(f"**Custo Total Estimado:** R$ {custo_total:,.2f}")

    st.subheader("Distribuição por Etapas")
    for etapa, percentual in etapas.items():
        valor = custo_total * percentual
        st.write(f"{etapa}: R$ {valor:,.2f} ({percentual*100:.0f}%)")
