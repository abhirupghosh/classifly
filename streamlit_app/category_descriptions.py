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

    # Create placeholders for each category
    category_placeholders = {category: st.empty() for category in category_predictor_dict}

    total_categories = len(category_predictor_dict)
    processed_categories = 0

    provider = st.session_state.provider
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_category = {executor.submit(get_target_description, category, category_predictor_dict, provider): category for category in category_predictor_dict}
        
        for future in concurrent.futures.as_completed(future_to_category):
            category = future_to_category[future]
            try:
                reasoning, description = future.result()
                
                # Update the placeholder for this category
                with category_placeholders[category].container():
                    st.markdown(f"**{category}**")
                    st.markdown(f"**Description:** {description}")
                    
                    # Create a button to show reasoning
                    if st.button(f"Show reasoning for {category}"):
                        st.info(reasoning)
                
                processed_categories += 1
                progress = processed_categories / total_categories
                progress_bar.progress(progress)
                status_text.text(f"Processed {processed_categories} out of {total_categories} categories")

            except Exception as exc:
                st.error(f"An error occurred while processing {category}: {exc}")

    status_text.text("All categories processed!")

def render_category_descriptions():
    if st.button("Generate Category Descriptions"):
        process_and_display_categories()
