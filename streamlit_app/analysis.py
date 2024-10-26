import streamlit as st
import pandas as pd
import math

def display_categories_grid(categories, columns=4):
    n = len(categories)
    rows = math.ceil(n / columns)
    grid = [categories[i:i+columns] for i in range(0, n, columns)]
    for row in grid:
        cols = st.columns(columns)
        for idx, item in enumerate(row):
            cols[idx].write(str(item))

def analyze_columns():
    if not st.session_state.predictor_columns:
        st.warning("Please select at least one predictor column.")
    elif not st.session_state.target_column:
        st.warning("Please select a target column.")
    else:
        st.subheader("Analysis Results")
        
        # Display target column information
        target_data = st.session_state.df[st.session_state.target_column]
        target_counts = target_data.value_counts()
        
        # Determine valid categories based on min and max samples per target
        min_samples = st.session_state.get('min_samples_per_target', 1)
        max_samples = st.session_state.get('samples_per_target', 10)
        valid_categories = target_counts[(target_counts >= min_samples) & (target_counts <= max_samples)]
        excluded_categories = target_counts[(target_counts < min_samples) | (target_counts > max_samples)]
        
        # Expander for category information
        with st.expander("## Category Information", expanded=True):
            if len(excluded_categories) > 0:
                st.warning(f"{len(excluded_categories)} categories were excluded due to sample size constraints.")

            st.write(f"**Total number of unique categories:** {target_data.nunique()}")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Number of valid categories:** {len(valid_categories)}")
                st.write("**Valid categories:**")
                display_categories_grid(valid_categories.index)

            with col2:
                st.write(f"**Number of excluded categories:** {len(excluded_categories)}")
                st.write("**Excluded categories:**")
                display_categories_grid(excluded_categories.index)

        
        # Expander for category distribution (only valid categories)
        with st.expander("Category Distribution", expanded=True):
            st.write("**Valid Category Distribution:**")
            st.bar_chart(valid_categories)
        
        # Expander for data preview
        with st.expander("View Data Preview", expanded=False):
            st.dataframe(
                st.session_state.df[
                    st.session_state.predictor_columns + [st.session_state.target_column]
                ],
                use_container_width=True
            )
