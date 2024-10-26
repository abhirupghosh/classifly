import streamlit as st
from ui_components import render_sidebar, render_main_content
from analysis import analyze_columns
from category_descriptions import render_category_descriptions
from testbench import add_testbench_to_app

def main():
    """
    Main function to set up and run the Streamlit application.
    
    This function configures the page, applies custom CSS, renders the sidebar and main content,
    handles the analysis rerun if needed, and adds the category descriptions and testbench sections.
    """
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

    # Add the category descriptions section
    render_category_descriptions()

    # Add the new testbench section
    add_testbench_to_app()

if __name__ == "__main__":
    main()
