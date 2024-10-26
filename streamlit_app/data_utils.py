import pandas as pd

def load_data(file):
    """
    Load data from a CSV or Excel file and perform necessary type conversions.
    
    Args:
    file (UploadedFile): The uploaded file object from Streamlit.
    
    Returns:
    pd.DataFrame: The loaded and processed dataframe.
    """
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        df = pd.read_excel(file)
    
    # Convert problematic columns to appropriate types
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str)
        elif df[col].dtype == 'int64':
            # Use nullable integer type to handle potential NaN values
            df[col] = df[col].astype('Int64')
    
    return df
