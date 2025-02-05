# Revit Data Analysis Streamlit App

This Streamlit application enables you to upload Revit data, perform basic and complex analysis, and visualize your data from Revit project. It provides flexibility in how data can be loaded (from Excel files or converted from Revit files), and offers multi-page functionality for different types of analysis.

[![](https://datadrivenconstruction.io/wp-content/uploads/2025/02/DataDrivenConstruction-Revit-data-analyse.jpg)](https://datadrivenconstruction.io/wp-content/uploads/2025/02/DataDrivenConstruction-Revit-data-analyse.jpg)

## Key Features

*   **Data Upload:**
    *   Supports uploading data from Excel (.xlsx) files.
    *   Provides an option to convert data from Revit files (.rvt) v2015-2025 using a DDC converter.
        *   The user must provide the path to the DDC converter folder (containing `RvtExporter.exe`) and the path to the Revit file.
*   **Multi-Page Functionality:** The app uses a multi-page structure for better navigation and organization:
    *   **Upload Page:** Handles uploading data from Excel files or converting from Revit files. This is the initial page where data is loaded.
    *   **Complex Analysis Page:** Performs and displays a more detailed statistical analysis and visualizations of the uploaded data. This page becomes visible after data has been uploaded.
    *   **Dynamic Analysis Page:** Allows interactive analysis of uploaded data through filtering, grouping, and pivoting. This page becomes visible after data has been uploaded.
*   **Data Visualization:** Displays:
    *   A preview of the uploaded data.
    *   A detailed summary of column characteristics (Total values, missing values, top values, etc.).
    *   Structure of columns and their data types.
    *   Interactive histograms and boxplots for numeric columns.
    *   Interactive bar charts for categorical columns.
    *   Correlation matrix heatmaps and missing value heatmaps.
*   **Session State:** The app uses Streamlit session state to preserve data, selected options, and user preferences (data, selected columns) between page changes.

## How to Run the App

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <project_folder>
    ```
    Replace `<repository_url>` and `<project_folder>` with your repository details.
2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
    or, if you don't have a `requirements.txt`:
    ```bash
    pip install streamlit seaborn multipage-streamlit matplotlib openpyxl
    ```
    This will install all necessary Python packages (including `streamlit`, `seaborn`, and `matplotlib`). Make sure you have `requirements.txt`; if not, you can generate it using `pip freeze > requirements.txt`.
3.  **Run the Streamlit app:**

    ```bash
    streamlit run MainPage.py
    ```

4.  **Access the app:** Open the URL provided in the terminal in your web browser. Typically, it will be something like `http://localhost:8501`.

## Code Structure

*   **`MainPage.py`:** Contains the main application logic, handles session state, multi-page setup.
*   **`UploadPage.py`** (or equivalent file): Contains the logic for data upload, data conversion, and initial data visualization functions.
*   **`ProfilingScript.py`** (or equivalent file): Contains the logic for the complex and dynamic data analysis pages.

## Session State Variables:

*   `df`: Stores the pandas DataFrame loaded from Excel or converted from a Revit file.
*   `selected_columns`: Stores selected column names (used for analysis).
*   `complex_analysis_selected_columns_widget`: Stores selected columns from the Complex Analysis page.

## Data Loading

The app provides two primary methods for loading data:

1.  **Excel Files:** You can directly upload `.xlsx` Excel files using the file uploader on the "Upload" page.
2.  **Revit Conversion:** To load data from a Revit file:
    *   Select the "Revit Converter" option.
    *   Provide the path to the folder containing the `RvtExporter.exe` file.
    *   Provide the path to your Revit file (`.rvt`).
    *   Click the "Convert Revit File" button to perform the conversion.

## Libraries Used

*   **Streamlit:** For creating the interactive web application.
*   **pandas:** For data manipulation and analysis.
*   **seaborn:** For statistical data visualization.
*   **matplotlib:** For creating basic plots.
*   **multipage_streamlit (or equivalent):** A library to implement multi-page navigation. Replace with the correct library name if required.

## Further Information

This app offers a foundational framework for working with data. You can expand its capabilities by adding:

*   More complex data analysis functions.
*   More interactive visualizations.
*   Advanced filtering and sorting functionality.
*   Data export functions.
*   Custom data analysis tools.
