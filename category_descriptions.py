import streamlit as st
import concurrent.futures
from inference.prompts.GetTargetDescription import get_target_description

def process_and_display_categories():
    if 'category_predictor_dict' not in st.session_state:
        st.warning("Please run the analysis first to generate category data.")
        return

    category_predictor_dict = st.session_state.category_predictor_dict

    st.header("Category Descriptions")
    progress_bar = st.progress(0)
    status_text = st.empty()

    # Create expanders with empty placeholders for each category
    category_expanders = {}
    for category in category_predictor_dict:
        with st.expander(category):
            category_expanders[category] = {
                'description': st.empty(),
                'reasoning': st.empty()
            }

    total_categories = len(category_predictor_dict)
    processed_categories = 0

    # Initialize the category_descriptions dictionary
    category_descriptions = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_category = {executor.submit(get_target_description, category, category_predictor_dict): category for category in category_predictor_dict}
        
        for future in concurrent.futures.as_completed(future_to_category):
            category = future_to_category[future]
            try:
                reasoning, description = future.result()
                
                # Update the placeholders for this category
                category_expanders[category]['description'].markdown(f"**Description:** {description}")
                category_expanders[category]['reasoning'].markdown(f"**Reasoning:** {reasoning}")
                
                # Add the description to the category_descriptions dictionary
                category_descriptions[category] = description
                
                processed_categories += 1
                progress = processed_categories / total_categories
                progress_bar.progress(progress)
                status_text.text(f"Processed {processed_categories} out of {total_categories} categories")

            except Exception as exc:
                st.error(f"An error occurred while processing {category}: {exc}")

    status_text.text("All categories processed!")

    # Store the category_descriptions in the session state
    st.session_state.category_descriptions = category_descriptions

def render_category_descriptions():
    if st.button("Generate Category Descriptions"):
        process_and_display_categories()
