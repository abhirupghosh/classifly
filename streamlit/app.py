import streamlit as st
import pandas as pd

def main():
    st.set_page_config(page_title="File Column Viewer", page_icon="📊", layout="wide")
    
    st.title("File Column Viewer")
    
    st.write("Upload a CSV or Excel file to view its columns.")
    
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            
            st.success(f"File '{uploaded_file.name}' successfully uploaded!")
            
            st.subheader("Columns in the file:")
            columns = df.columns.tolist()
            for col in columns:
                st.write(f"- {col}")
            
            st.subheader("Preview of the data:")
            st.dataframe(df.head())
        
        except Exception as e:
            st.error(f"An error occurred while processing the file: {str(e)}")

if __name__ == "__main__":
    main()
