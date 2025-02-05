import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from multipage_streamlit import State


def complex_analysis() -> None:
    """Create complex analysis from load data frame. We can choose column for detail analysis"""
    state = State(__name__)

    st.title("Complex Analysis")

    _df = st.session_state.df

    # Store selected columns in session_state with a key
    selected_columns = st.multiselect(
        "Select columns for analysis",
        _df.columns.to_list(),
        key=state("complex_analysis_selected_columns")
    )

    # Main Information
    with st.expander("Main Information", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", _df.shape[0])
        with col2:
            st.metric("Number of Features", _df.shape[1])
        with col3:
            st.metric("Missing Values", _df.isna().sum().sum())

        st.write("Data Types")
        dtypes = _df.dtypes.reset_index()
        dtypes.columns = ["Column", "Type"]
        st.dataframe(dtypes, hide_index=True)

    if not selected_columns:
        st.warning("No columns selected for analysis")
        st.stop()

    filtered_df = _df[selected_columns]

    # Data Type Separation
    numeric_cols = filtered_df.select_dtypes(include='number').columns.tolist()
    categorical_cols = filtered_df.select_dtypes(exclude='number').columns.tolist()

    # Statistics
    with st.expander("Statistics"):
        if numeric_cols:
            st.subheader("Numeric Statistics")
            st.dataframe(filtered_df[numeric_cols].describe().T)

        if categorical_cols:
            st.subheader("Categorical Statistics")
            stats = []
            for col in categorical_cols:
                stats.append({
                    "Column Name": col,
                    "Unique Values": filtered_df[col].nunique(),
                    "Most Frequent Value": filtered_df[col].mode().iloc[0],
                    "Frequency": filtered_df[col].value_counts().iloc[0]
                })
            st.dataframe(pd.DataFrame(stats))

    # Visualizations
    # Visualizations
    with st.expander("Visualizations"):
        tab1, tab2, tab3, tab4 = st.tabs([
            "Distributions",
            "Correlations",
            "Missing Values Heatmap",
            "Categorical Analysis",
        ])

        with tab1:
            try:
                if numeric_cols:
                    col = st.selectbox("Select Numeric Column", numeric_cols, key=state("complex_analysis_numeric_column_selectbox"))
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

                    # Histogram
                    sns.histplot(filtered_df[col], kde=True, ax=ax1)
                    ax1.set_title(f"Distribution of {col}")
                    ax1.set_xlabel(col)
                    ax1.set_ylabel("Frequency")
                    ax1.text(0.5, -0.2, f"Shows the distribution of values in '{col}'.", ha='center', va='top', transform=ax1.transAxes, fontsize=8, color='gray')

                    # Boxplot
                    sns.boxplot(x=filtered_df[col], ax=ax2)
                    ax2.set_title(f"Boxplot of {col}")
                    ax2.set_xlabel(col)
                    ax2.text(0.5, -0.2, f"Shows the median, quartiles, and outliers for '{col}'.", ha='center', va='top', transform=ax2.transAxes, fontsize=8, color='gray')

                    st.pyplot(fig)
                else:
                    st.warning("No numeric columns available for visualization")
            except Exception as e:
                st.error(e)

        with tab2:
            if len(numeric_cols) > 1:
                st.subheader("Correlation Matrix")
                corr = filtered_df[numeric_cols].corr()
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
                ax.set_title("Correlation Matrix")
                ax.text(0.5, -0.1, "Shows the correlation between numeric columns.  Values near +1/-1 are strong positive/negative correlations, while values near 0 are weak correlations.", ha='center', va='top', transform=ax.transAxes, fontsize=8, color='gray')
                st.pyplot(fig)
            else:
                st.warning("Need at least two numeric columns for correlation analysis")

        with tab3:
            st.subheader("Missing Values Heatmap")
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.heatmap(filtered_df.isna().T, cmap="viridis", cbar=False, ax=ax)
            ax.set_title("Missing Values Heatmap")
            ax.text(0.5, -0.1, "Visualizes missing data; darker colors indicate more missing values.", ha='center', va='top', transform=ax.transAxes, fontsize=8, color='gray')
            st.pyplot(fig)

        with tab4:
            if categorical_cols:
                col = st.selectbox("Select Categorical Column", categorical_cols, key=state("complex_analysis_categorical_column_selectbox"))
                top_n = st.slider("Top N Values", 5, 50, 10, key="complex_analysis_top_n_slider")
                counts = filtered_df[col].value_counts().nlargest(top_n)
                fig, ax = plt.subplots(figsize=(10, 4))
                sns.barplot(x=counts.index, y=counts.values, ax=ax)
                plt.xticks(rotation=45)
                ax.set_title(f"Top {top_n} Values in {col}")
                ax.set_ylabel("Frequency")
                ax.text(0.5, -0.2, f"Shows the frequency of the top {top_n} values in '{col}'.", ha='center', va='top', transform=ax.transAxes, fontsize=8, color='gray')
                st.pyplot(fig)
            else:
                st.warning("No categorical columns available for visualization")

    # Detailed Analysis
    with st.expander("Detailed Analysis"):
        st.subheader("Data Preview")
        rows = st.slider("Number of Rows", 5, 100, 10, key="complex_analysis_rows_slider")
        st.dataframe(filtered_df.head(rows), use_container_width=True)
        if st.checkbox("Show Column Info", key=state("complex_analysis_show_column_info_checkbox")):
            for col in selected_columns:
                st.write(f"**{col}**")
                col1, col2 = st.columns(2)
                with col1:
                    st.write("First Values", filtered_df[col].head().tolist())
                with col2:
                    st.write("Unique Values Count", filtered_df[col].nunique())
                st.divider()
        state.save()

def dynamic_analysis() -> None:
    state = State(__name__)

    st.title("Dynamic Data Analysis")
    filtered_df = st.session_state.df
    selected_columns = st.multiselect(
        "Select columns:",
        filtered_df.columns,
        key=state("dynamic_analysis")
    )
    if not selected_columns:
        st.warning("Please select columns for analysis")
        st.stop()


    # 2. Dynamic cascade filters
    with st.expander("Dynamic Filters"):
        for idx, column in enumerate(selected_columns):
            available_options = filtered_df[column].unique().tolist()
            selected_values = st.multiselect(
                f"Filter by column {column}: ({len(available_options)} options)",
                options=available_options,
                key=state(f"filter_{column}_{idx}")
            )
            if selected_values:
                filtered_df = filtered_df[filtered_df[column].isin(selected_values)]
    updated_df = filtered_df[selected_columns] if selected_columns else filtered_df
    # 3. Display filtered results

    st.subheader("Filtering Results")
    st.write(f"Found records: {len(filtered_df)}")
    st.dataframe(updated_df)
    # 4. Analysis section
    st.subheader("Data Analysis")

    # 5. Grouping and aggregation with all functions
    st.markdown(f"**Grouping and Aggregation**")
    group_cols = st.multiselect(
        "Select columns for grouping",
        options=updated_df.columns,
        key=state("group_by")
    )

    numeric_cols = updated_df.select_dtypes(include=np.number).columns.tolist()
    agg_cols = st.multiselect(
        "Select columns for aggregation",
        options=numeric_cols,
        key=state("agg_cols")
    )

    # Fixed aggregation functions
    agg_funcs = ['sum', 'mean', 'median', 'min', 'max', 'count']

    if group_cols and agg_cols:
        try:
            grouped_df = updated_df.groupby(group_cols)[agg_cols].agg(agg_funcs)
            st.write("Grouping Results:")
            st.dataframe(grouped_df.reset_index().round(2))
        except Exception as e:
            st.error(f"Error during grouping: {str(e)}")

    # 6. Pivot table
    st.markdown(f"**Pivot Table**")
    col1, col2, col3 = st.columns(3)

    with col1:
        pivot_index = st.selectbox("Select column for pivot table rows", updated_df.columns, key=state("pivot_index"))
    with col2:
        pivot_columns = st.selectbox("Select column for pivot table columns", updated_df.columns, key=state("pivot_columns"))
    with col3:
        pivot_values = st.selectbox("Select column for values", numeric_cols, key=state("pivot_values"))

    pivot_func = st.selectbox(
        "Select aggregation function",
        options=['mean', 'sum', 'count', 'min', 'max'],
        key=state("pivot_func")
    )

    if pivot_index and pivot_values and pivot_func:
        try:
            pivot_table = pd.pivot_table(
                filtered_df,
                index=pivot_index,
                columns=pivot_columns,
                values=pivot_values,
                aggfunc=pivot_func,
                fill_value=0
            )
            st.write("Pivot Table Result:")
            st.dataframe(pivot_table.round(2))
        except Exception as e:
            st.error(f"Error creating pivot table: {str(e)}")

    state.save()