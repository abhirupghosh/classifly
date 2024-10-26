import streamlit as st
from ui_components import render_sidebar, render_main_content
from analysis import analyze_columns

def main():
    st.set_page_config(page_title="Auto Classifier", layout="wide")

    # Apply custom CSS
    st.markdown("""
        <style>
        .streamlit-expanderHeader {
            font-size: 1.2rem !important;
            font-weight: 600 !important;
        }
        .streamlit-expanderContent {
            font-size: 1rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    render_sidebar()
    render_main_content()

    if st.session_state.get('rerun_analysis', False):
        analyze_columns()
        st.session_state.rerun_analysis = False

if __name__ == "__main__":
    main()
