import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configuração da página do Streamlit
st.set_page_config(page_title="Preditor de Caixa - Restaurante", layout="wide")

st.title("📊 Motor de Previsão de Fluxo de Caixa")
st.subheader("Restaurante - Lucro Real")

# --- 1. CONFIGURAÇÃO DE REGRAS DE TAXAS E PRAZOS ---
# Você poderá alterar esses valores aqui quando tiver os dados exatos da contabilidade!
REGRAS = {
    "Pix": {"prazo": 0, "tipo": "D+0", "taxa": 0.00},
    "RedeShop": {"prazo": 1, "tipo": "D+1", "taxa": 0.015},
    "Visa Electron": {"prazo": 1, "tipo": "D+1", "taxa": 0.015},
    "Elo Débito": {"prazo": 1, "tipo": "D+1", "taxa": 0.02},
    "Voucher PAT (15 dias)": {"prazo": 15, "tipo": "D+15", "taxa": 0.036},
    "Voucher Normal (30 dias)": {"prazo": 30, "tipo": "D+30", "taxa": 0.045},
    "Mastercard Crédito": {"prazo": 30, "tipo": "D+30", "taxa": 0.03},
    "Visa Crédito": {"prazo": 30, "tipo": "D+30", "taxa": 0.03},
}

# --- 2. FUNÇÃO MAESTRO: CALCULA A DATA REAL DE LIQUIDAÇÃO BANCO ---
def ajustar_data_liquidacao(data_venda, prazo, tipo_prazo):
    data_prevista = data_venda + timedelta(days=prazo)
    
    # Se for D+0 (Pix), entra na hora, inclusive fim de semana
    if tipo_prazo == "D+0":
        return data_prevista
        
    # Para cartões (D+1, D+15, D+30): se cair no sábado(5) ou domingo(6), joga para segunda
    if data_prevista.weekday() == 5:  # Sábado
        return data_prevista + timedelta(days=2)
    elif data_prevista.weekday() == 6:  # Domingo
        return data_prevista + timedelta(days=1)
        
    return data_prevista

def processar_dados(df_vendas):
    dados_futuros = []
    for _, linha in df_vendas.iterrows():
        meio = linha["Meio de Pagamento"]
        valor_bruto = linha["Valor Bruto"]
        data_venda = pd.to_datetime(linha["Data da Venda"])
        
        if meio in REGRAS:
            regra = REGRAS[meio]
            valor_liquido = valor_bruto * (1 - regra["taxa"])
            data_liberacao = ajustar_data_liquidacao(data_venda, regra["prazo"], regra["tipo"])
            
            dados_futuros.append({
                "Data de Entrada": data_liberacao.strftime("%Y-%m-%d"),
                "Meio de Pagamento": meio,
                "Valor Líquido": valor_liquido
            })
            
    return pd.DataFrame(dados_futuros)

# --- 3. INTERFACE DO USUÁRIO (ABAS) ---
aba_manual, aba_upload = st.tabs(["⌨️ Lançamento Manual Rápido", "📂 Upload de Relatório (CSV/Excel)"])

df_base = pd.DataFrame()

with aba_manual:
    st.markdown("### Digite as vendas do dia para simular as entradas")
    data_input = st.date_input("Data das Vendas:", datetime.now())
    
    col1, col2, col3 = st.columns(3)
    vendas_manuais = []
    
    with col1:
        v_pix = st.number_input("Pix (R$):", min_value=0.0, value=0.0, step=100.0)
        v_redeshop = st.number_input("RedeShop (R$):", min_value=0.0, value=0.0, step=100.0)
        v_visa_elec = st.number_input("Visa Electron (R$):", min_value=0.0, value=0.0, step=100.0)
    with col2:
        v_elo_deb = st.number_input("Elo Débito (R$):", min_value=0.0, value=0.0, step=100.0)
        v_pat = st.number_input("Voucher PAT (R$):", min_value=0.0, value=0.0, step=100.0)
        v_voucher_norm = st.number_input("Voucher Normal (R$):", min_value=0.0, value=0.0, step=100.0)
    with col3:
        v_master_cred = st.number_input("Mastercard Crédito (R$):", min_value=0.0, value=0.0, step=100.0)
        v_visa_cred = st.number_input("Visa Crédito (R$):", min_value=0.0, value=0.0, step=100.0)

    if st.button("🚀 Calcular Previsão Manual"):
        mapeamento_manual = [
            ("Pix", v_pix), ("RedeShop", v_redeshop), ("Visa Electron", v_visa_elec),
            ("Elo Débito", v_elo_deb), ("Voucher PAT (15 dias)", v_pat),
            ("Voucher Normal (30 dias)", v_voucher_norm), ("Mastercard Crédito", v_master_cred),
            ("Visa Crédito", v_visa_cred)
        ]
        vendas_manuais = [{"Data da Venda": data_input, "Meio de Pagamento": m, "Valor Bruto": v} for m, v in mapeamento_manual if v > 0]
        df_base = pd.DataFrame(vendas_manuais)

with aba_upload:
    st.markdown("### Importe o arquivo consolidado de vendas")
    arquivo = st.file_uploader("Escolha um arquivo CSV ou Excel", type=["csv", "xlsx"])
    st.caption("O arquivo deve conter as colunas: 'Data da Venda', 'Meio de Pagamento' e 'Valor Bruto'")
    
    if arquivo is not None:
        if arquivo.name.endswith(".csv"):
            df_base = pd.read_csv(arquivo)
        else:
            df_base = pd.read_excel(arquivo)
        st.success("Arquivo carregado com sucesso!")

# --- 4. EXIBIÇÃO DOS RESULTADOS E GRÁFICOS AZUIS ---
if not df_base.empty:
    st.divider()
    df_resultado = processar_dados(df_base)
    
    if not df_resultado.empty:
        # Agrupa os valores que caem no mesmo dia
        df_agrupado = df_resultado.groupby("Data de Entrada")["Valor Líquido"].sum().reset_index()
        df_agrupado = df_agrupado.sort_values("Data de Entrada")
        
        st.subheader("📅 Cronograma de Entradas Previstas no Banco")
        
        # Layout em colunas: Gráfico à esquerda, Tabela à direita
        g1, g2 = st.columns([2, 1])
        
        with g1:
            # Configura o gráfico de barras com a cor Azul solicitada
            st.bar_chart(
                data=df_agrupado, 
                x="Data de Entrada", 
                y="Valor Líquido", 
                color="#004AH7"  # Azul Royal Corporativo
            )
            
        with g2:
            df_visual = df_agrupado.copy()
            df_visual["Valor Líquido"] = df_visual["Valor Líquido"].apply(lambda x: f"R$ {x:,.2f}")
            st.dataframe(df_visual, use_container_width=True, hide_index=True)
            
        st.metric(label="Total de Entradas Futuras Previstas", value=f"R$ {df_resultado['Valor Líquido'].sum():,.2f}")
    else:
        st.warning("Nenhum dado correspondente às regras mapeadas foi encontrado.")