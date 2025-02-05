import streamlit as st
import multipage_streamlit as mt
from PagesData import UploadPage, ProfilingScript


def init_state():
    # create session state
    if "df" not in st.session_state:
        st.session_state.df = None
    if "selected_columns" not in st.session_state:
        st.session_state.selected_columns = []
    if "complex_analysis_selected_columns_widget" not in st.session_state:
        st.session_state.complex_analysis_selected_columns_widget = []

def main():
    init_state()
    app = mt.MultiPage()
    app.add("Upload ", UploadPage.upload_page)
    if st.session_state.df is not None:
        app.add("Complex analise 📊", ProfilingScript.complex_analysis)
        app.add("Dynamic  analise 🎛️", ProfilingScript.dynamic_analysis)
    app.run_radio()

main()