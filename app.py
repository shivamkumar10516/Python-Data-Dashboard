import streamlit as st
import pandas as pd

# 1. FRONTEND: Page Configuration & Header
st.set_page_config(page_title="Hackathon Analytics Dash", layout="wide")
st.title("🚀 Hackathon Data Analytics Dashboard")
st.subheader("Turn your raw data into immediate visual insights")

# 2. BACKEND/API: File Uploader Component
uploaded_file = st.file_uploader("Upload your project CSV or Excel data file", type=["csv", "xlsx"])

# 3. LOGIC & DATA PROCESSING (The "Backend" work)
if uploaded_file is not None:
    # Read the data using Pandas (just like your normal analyst workflow)
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # FRONTEND: Show raw data preview toggler
    if st.checkbox("Show Raw Data Preview"):
        st.write(df.head()) 
        # Download the uploaded data
    st.download_button(
    label="⬇️ Download Data",
    data=df.to_csv(index=False),
    file_name="downloaded_data.csv",
    mime="text/csv"
   )
    # BACKEND: Calculate core metrics dynamically
    st.markdown("### 📊 Core Key Performance Indicators (KPIs)")
    
    # Let's assume the user selects a numeric column to analyze
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_cols) > 0:
        # Create columns layout on the website frontend
        col1, col2, col3 = st.columns(3)
        
        selected_col = st.selectbox("Select a metric column to calculate KPIs:", numeric_cols)
        
        # Calculate stats
        total_value = df[selected_col].sum()
        avg_value = df[selected_col].mean()
        row_count = len(df)
        
        # Display metrics beautifully on screen
        col1.metric(label=f"Total {selected_col}", value=f"{total_value:,.2f}")
        col2.metric(label=f"Average {selected_col}", value=f"{avg_value:,.2f}")
        col3.metric(label="Total Data Rows", value=row_count)
        
        # 4. DATA VISUALIZATION (Dynamic charts generated instantly)
        st.markdown("### 📈 Visual Chart")
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if len(categorical_cols) > 0:
            x_axis = st.selectbox("Select Category (X-Axis):", categorical_cols)
            # Group data for the chart
            chart_data = df.groupby(x_axis)[selected_col].sum().reset_index()
            # Render interactive chart
            st.bar_chart(data=chart_data, x=x_axis, y=selected_col)
        else:
            st.info("Add a text/category column to your data to unlock bar charts!")
            st.line_chart(df[selected_col])
    else:
        st.warning("No numeric columns found in this dataset to generate KPIs.")

else:
    # Default screen when no file is uploaded yet
    st.info("☝️ Please upload a CSV or Excel file above to start the engine.")
