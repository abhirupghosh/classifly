import streamlit as st
import concurrent.futures
from inference.prompts.GetTargetDescription import get_target_description
from rag.create_index import create_index
import pandas as pd

def create_faiss_indices(df, predictor_columns):
    indices = {}
    model = st.session_state.sentence_transformer_model
    # Ensure the model is on CPU
    model = model.cpu()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_column = {executor.submit(create_index, df, column, model=model): column for column in predictor_columns}
        for future in concurrent.futures.as_completed(future_to_column):
            column = future_to_column[future]
            index, _ = future.result()
            indices[column] = index
    return indices

def process_and_display_categories():
    """
    Process and display category descriptions using concurrent execution.
    
    This function checks for the presence of category data, creates expanders for each category,
    and concurrently generates descriptions for all categories. It updates the UI with progress
    and stores the generated descriptions in the session state.
    """
    if 'category_predictor_dict' not in st.session_state:
        st.warning("Please run the analysis first to generate category data.")
        return

    category_predictor_dict = st.session_state.category_predictor_dict

    st.header("Category Descriptions")
    st.markdown("""
    <style>
    .stProgress .st-bo {
        background-color: green;
    }
    </style>
    """, unsafe_allow_html=True)
    progress_bar = st.progress(0, text="Generating category descriptions...")

    def update_progress(progress, text):
        progress_bar.progress(progress, text=text)

    # Create FAISS indices for each predictor column
    predictor_columns = st.session_state.predictor_columns
    df = st.session_state.df
    with st.spinner("Creating FAISS indices for predictor columns..."):
        faiss_indices = create_faiss_indices(df, predictor_columns)
    st.session_state.faiss_indices = faiss_indices

    # Create expanders with empty placeholders for each category
    category_expanders = {}
    for category in category_predictor_dict:
        with st.expander(category):
            category_expanders[category] = st.empty()

    total_categories = len(category_predictor_dict.keys())
    processed_categories = 0

    # Initialize the category_descriptions dictionary
    category_descriptions = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_category = {executor.submit(get_target_description, category, category_predictor_dict): category for category in category_predictor_dict}
        
        for future in concurrent.futures.as_completed(future_to_category):
            category = future_to_category[future]
            try:
                reasoning, description = future.result()
                
                # Update the placeholder for this category, using reasoning as tooltip
                category_expanders[category].markdown(description, help=reasoning)
                
                # Add the description to the category_descriptions dictionary
                category_descriptions[category] = description
                
                processed_categories += 1
                progress = processed_categories / total_categories
                update_progress(progress, f"Processed {processed_categories} out of {total_categories} categories")

            except Exception as exc:
                st.error(f"An error occurred while processing {category}: {exc}")

    st.toast("Category descriptions generated!", icon="🔍")

    # Store the category_descriptions in the session state
    st.session_state.category_descriptions = category_descriptions

def render_category_descriptions():
    """
    Render the category descriptions section in the Streamlit app.
    
    This function checks if category data is available and provides a button
    to generate category descriptions. When clicked, it calls the
    process_and_display_categories function to generate and display the descriptions.
    """
    if 'category_predictor_dict' in st.session_state:
        if st.button("Generate Category Descriptions"):
            process_and_display_categories()
    else:
        pass
