import pandas as pd
import streamlit as st
from sidebar import showSidebar
from ordersDashboard import show_orders_dashboard
from showHomepage import show_homepage

def start_dashboard(engine):
    if 'pesquisou' not in st.session_state:
        show_homepage()

    showSidebar(engine)