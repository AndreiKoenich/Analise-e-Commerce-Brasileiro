import pandas as pd
import streamlit as st
from sidebar import show_info
from ordersDashboard import show_orders_dashboard

def load_data_from_db(engine, table_name):
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)
    return df

def start_dashboard(engine):
    if 'pesquisou' not in st.session_state:
        st.markdown("<h1 style='text-align: center; white-space: nowrap;'>Análise de Tendências no E-commerce Brasileiro</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: left; font-size: 18px;'>Selecione uma consulta ao lado para iniciar.</p>", unsafe_allow_html=True)
        st.image('image.jpeg')
        
    show_info(engine)
    print("Dashboard inicializada com sucesso.")