from startDatabase import import_data
from queries import best_products
from dashboard import start_dashboard
import streamlit as st

def main():
    if 'engine' not in st.session_state:
        st.session_state.engine = import_data() 
    start_dashboard(engine=st.session_state.engine)

main()