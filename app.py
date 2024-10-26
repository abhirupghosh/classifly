import streamlit as st
from ui_components import render_sidebar, render_main_content
from analysis import analyze_columns
from category_descriptions import render_category_descriptions

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
        /* Hide progress bar text */
        .stProgress > div > div > div > div {
            display: none !important;
        }
        /* Optionally, adjust the height of the progress bar */
        .stProgress > div > div > div {
            height: 10px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    render_sidebar()
    render_main_content()

    if st.session_state.get('rerun_analysis', False):
        analyze_columns()
        st.session_state.rerun_analysis = False

    # Add the new category descriptions section
    render_category_descriptions()

if __name__ == "__main__":
    main()
