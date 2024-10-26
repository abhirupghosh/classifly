import streamlit as st
from data_utils import load_data

def render_sidebar():
    with st.sidebar:
        st.header("Analysis Settings")
        
        with st.form("analysis_settings"):
            samples_per_target = st.number_input(
                "Samples per target",
                min_value=1,
                max_value=100,
                value=st.session_state.get('samples_per_target', 10),
                help="How many samples do you want to use for each target?"
            )

            min_samples_per_target = st.number_input(
                "Minimum samples per target",
                min_value=1,
                max_value=100,
                value=st.session_state.get('min_samples_per_target', 1),
                help="Minimum number of samples per target."
            )
            
            st.subheader("Additional Context")
            additional_context = st.text_area(
                "Provide any additional context regarding the categories:",
                value=st.session_state.get('additional_context', ''),
                height=150,
                help="This information will be used to improve the analysis of your data."
            )
            
            submit_button = st.form_submit_button("Apply Settings")
        
        if submit_button:
            st.session_state.samples_per_target = samples_per_target
            st.session_state.min_samples_per_target = min_samples_per_target
            st.session_state.additional_context = additional_context
            if st.session_state.get('analyze_button_clicked', False):
                st.session_state.rerun_analysis = True

def render_main_content():
    st.title("Auto Classifier")
    
    st.write("Upload a CSV or Excel file to analyze its columns.")
    
    # Initialize session state variables if they don't exist
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'columns' not in st.session_state:
        st.session_state.columns = []
    if 'predictor_columns' not in st.session_state:
        st.session_state.predictor_columns = []
    if 'target_column' not in st.session_state:
        st.session_state.target_column = None
    if 'samples_per_target' not in st.session_state:
        st.session_state.samples_per_target = 10
    if 'additional_context' not in st.session_state:
        st.session_state.additional_context = ''

    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        try:
            st.session_state.df = load_data(uploaded_file)
            st.session_state.columns = st.session_state.df.columns.tolist()
            st.success(f"File '{uploaded_file.name}' successfully uploaded!")
        except Exception as e:
            st.error(f"An error occurred while processing the file: {str(e)}")
    
    if st.session_state.df is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Select Predictor Columns")
            st.session_state.predictor_columns = st.multiselect(
                "Choose the columns that determine the target:",
                options=st.session_state.columns,
                help="These are the text columns that will be used to predict the target."
            )
        
        with col2:
            st.subheader("Select Target Column")
            st.session_state.target_column = st.selectbox(
                "Choose the column to be predicted:",
                options=[None] + [col for col in st.session_state.columns if col not in st.session_state.predictor_columns],
                help="This is the column that contains the categories you want to predict."
            )
        
        if st.button("Analyze Columns"):
            st.session_state.analyze_button_clicked = True
            st.session_state.rerun_analysis = True
