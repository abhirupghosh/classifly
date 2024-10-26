import streamlit as st
from inference.prompts.CreateCategorizationPrompt import get_category

def render_testbench():
    st.header("Categorization Testbench")

    if 'category_predictor_dict' not in st.session_state or 'category_descriptions' not in st.session_state:
        st.warning("Please run the analysis and generate category descriptions first.")
        return

    predictor_columns = st.session_state.predictor_columns
    
    # Create input fields for each predictor column
    user_inputs = {}
    for column in predictor_columns:
        user_inputs[column] = st.text_input(f"Enter value for {column}")

    if st.button("Run Categorization"):
        process_testbench(user_inputs)

def process_testbench(user_inputs):
    categories = list(st.session_state.category_descriptions.keys())
    category_descriptions = st.session_state.category_descriptions

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

    # Move category descriptions to sidebar
    with st.sidebar:
        st.header("Category Descriptions")
        for cat, desc in category_descriptions.items():
            with st.expander(cat):
                st.write(desc)

def add_testbench_to_app():
    if 'category_predictor_dict' in st.session_state and 'category_descriptions' in st.session_state:
        render_testbench()
    else:
        pass
