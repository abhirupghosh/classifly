from concurrent.futures import ThreadPoolExecutor
import streamlit as st
from inference.prompts.CreateCategorizationPrompt import get_category
from rag.search_index import search_index
import numpy as np

def render_testbench():
    st.header("Categorization Testbench")

    if 'category_predictor_dict' not in st.session_state or 'category_descriptions' not in st.session_state or 'faiss_indices' not in st.session_state:
        pass
    else:
        predictor_columns = st.session_state.predictor_columns
        
        # Create input fields for each predictor column
        user_inputs = {}
        for column in predictor_columns:
            user_inputs[column] = st.text_input(f"Enter value for {column}")

        if st.button("Run Categorization"):
            process_testbench(user_inputs)

    # Always show the category descriptions in the sidebar
    with st.sidebar:
        st.header("Category Descriptions")
        if 'category_descriptions' in st.session_state:
            for cat, desc in st.session_state.category_descriptions.items():
                with st.expander(cat):
                    st.write(desc)
        else:
            st.write("Category descriptions not available yet.")

def process_testbench(user_inputs):
    categories = list(st.session_state.category_descriptions.keys())
    category_descriptions = st.session_state.category_descriptions

    # Create a dictionary of the input predictor values
    predictor_values_dict = {column: user_inputs[column] for column in st.session_state.predictor_columns if user_inputs[column]}

    # Prepare predictor values string
    predictor_values = "\n".join([f"{key}: {value}" for key, value in user_inputs.items() if value])

    if not predictor_values:
        st.warning("Please enter at least one predictor value.")
        return

    provider = st.session_state.provider
    with st.spinner("Processing..."):
        reasoning, category = get_category(categories, category_descriptions, predictor_values, provider)

    st.subheader("Results")
    st.markdown(f":blue[**Predicted Category:**] {category}", help=reasoning)

    # Search for top 5 similar tickets
    search_top_tickets(predictor_values_dict)

    # Move category descriptions to sidebar
    with st.sidebar:
        st.header("Category Descriptions")
        for cat, desc in category_descriptions.items():
            with st.expander(cat):
                st.write(desc)

def search_top_tickets(query):
    # Initialize lists to store all results
    all_distances = []
    all_indices = []

    # Search each column with its respective index
    for column, search_term in query.items():
        if column in st.session_state.faiss_indices and search_term:
            index = st.session_state.faiss_indices[column]
            with ThreadPoolExecutor() as executor:
                future = executor.submit(search_index, index, None, search_term, k=10)
                distances, indices = future.result()
            all_distances.extend(distances)
            all_indices.extend(indices)

    # Combine results and sort by distance
    combined_results = sorted(zip(all_distances, all_indices), key=lambda x: x[0])

    # Get unique top 5 results (avoiding duplicates)
    top_5_indices = []
    seen_indices = set()
    for _, idx in combined_results:
        if idx not in seen_indices:
            top_5_indices.append(idx)
            seen_indices.add(idx)
            if len(top_5_indices) == 5:
                break

    # Fetch the corresponding rows from the dataframe
    top_5_tickets = st.session_state.df.iloc[top_5_indices]

    # Display the results
    st.subheader("Top 5 Similar Tickets")
    for _, ticket in top_5_tickets.iterrows():
        with st.expander(f"Ticket: {ticket['Ticket ID']}"):
            for column in st.session_state.predictor_columns:
                st.text(f"{column}: {ticket[column]}")
