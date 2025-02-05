import streamlit as st
import os
import subprocess
import pandas as pd

from Utility.CategoryData import category_base_structure


def create_dataframe_from_dict(data_dict):
    """
    Creates a Pandas DataFrame from a dictionary where keys are categories
    and values are lists of column names.

    Args:
        data_dict: Dictionary with category names as keys and lists of columns as values.

    Returns:
        pandas DataFrame: A DataFrame with "Column Name" and "Category" columns.
    """

    data_rows = []
    for category, columns in data_dict.items():
        for column in columns:
            data_rows.append({
                "Column Name": column,
                "Category": category
            })
    return pd.DataFrame(data_rows)

def analyze_dataframe(df):
    """
    Analyzes a DataFrame and returns a DataFrame with information about each column.

    Args:
        df: pandas DataFrame.

    Returns:
        pandas DataFrame: DataFrame with column information.
    """

    analysis_data = []
    for column in df.columns:
        total_count = df[column].size
        null_count = df[column].isnull().sum()
        top_10_values = df[column].value_counts().nlargest(10).index.tolist()
        top_10_values_str = str(top_10_values) # Convert the list to a string

        analysis_data.append({
            'Column Name': column,
            'Total Value Count': total_count,
            'Number of Missing Values': null_count,
            'Top 10 Values': top_10_values_str
        })

    return pd.DataFrame(analysis_data)

def visualise_loads():
    if st.session_state.df is not None:
        st.subheader("Data Preview")
        try:
            st.write(st.session_state.df.head())
        except:
            st.write("")
        st.subheader("Short description")
        st.write(analyze_dataframe(st.session_state.df))
        st.write("Columns Structure sample")
        st.json(category_base_structure)
        st.dataframe(create_dataframe_from_dict(category_base_structure))

def load_excel_data(uploaded_file):
    """Loads data from an uploaded Excel file.

    Args:
        uploaded_file: The uploaded file object.

    Returns:
        pandas DataFrame: The loaded DataFrame or None if an error occurs.
    """
    try:
        df = pd.read_excel(uploaded_file)
        st.success("Excel data successfully loaded!")
        return df
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return None

def convert_revit_data(path_conv, file_path):
    """Converts Revit data using the DDC converter.

    Args:
        path_conv: Path to the DDC converter folder.
        file_path: Path to the Revit file.

    Returns:
         pandas DataFrame: The converted DataFrame or None if an error occurs.
    """

    try:
        with st.spinner("Converting Revit file..."):
            process = subprocess.Popen(
                [os.path.join(path_conv, 'RvtExporter.exe'), file_path],
                cwd=path_conv,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                st.success("Conversion finished")
                output_file = file_path[:-4] + "_rvt.xlsx"
                df = pd.read_excel(output_file)
                # df.columns = [col.split(' : ')[0] for col in df.columns]  # remove storage type does not work in streamlit visualisation
                st.success("Revit data successfully loaded!")
                return df
            else:
                 st.error(f"Conversion failed. Error message: {stderr.decode('utf-8')}")
                 return None
    except Exception as e:
        st.error(f"Error during Revit conversion: {e}")
        return None

def upload_page():
    st.title("Data Upload")
    data_source = st.radio("Select Data Source", ["Excel File", "Revit Converter"])
    if data_source == "Excel File":
        uploaded_file = st.file_uploader("Upload an Excel file", type="xlsx")
        if uploaded_file is not None:
            df = load_excel_data(uploaded_file)
            if df is not None:
                st.session_state.df = df

    elif data_source == "Revit Converter":
        base_path_conv_path = r"e:\DDC"
        base_revit_file_path = r"e:\DDC\2022 rstadvancedsampleproject.rvt"
        st.subheader("Enter DDC Folder and Revit File Path")
        path_conv = st.text_input("Enter path to DDC converter folder (where RvtExporter.exe is located)", base_path_conv_path)  # DDC folder path via text input
        file_path = st.text_input("Enter path to Revit file (.rvt)", base_revit_file_path)# Revit file path by text input

        if st.button("Convert Revit File"):
            if file_path and path_conv:
                df = convert_revit_data(path_conv, file_path)
                if df is not None:
                    st.session_state.df = df
            else:
                st.warning("Please enter DDC converter folder and Revit file path.")

    visualise_loads()