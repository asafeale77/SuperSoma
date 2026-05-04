import streamlit as st

st.title("🧮 Calculadora de Soma")

if "numeros" not in st.session_state:
    st.session_state.numeros = []

entrada = st.number_input("Digite um número:", step=1.0, format="%.2f")

col1, col2 = st.columns(2)
if col1.button("➕ Adicionar"):
    st.session_state.numeros.append(entrada)

if col2.button("🔄 Limpar"):
    st.session_state.numeros = []

if st.session_state.numeros:
    st.write("**Números adicionados:**", st.session_state.numeros)
    st.success(f"**Resultado: {sum(st.session_state.numeros):.2f}**")