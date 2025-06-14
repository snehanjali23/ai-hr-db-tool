import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
import re

st.set_page_config(page_title="Universal CSV to SQLite", page_icon="🗃️")
st.title("🗃️ Universal CSV Upload to SQLite")
st.caption("Upload any CSV file — no errors, flexible table creation, works for all formats")

# 📤 Upload CSV
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

def sanitize_table_name(filename):
    """Convert file name to a safe SQLite table name"""
    return re.sub(r'\W+', '_', filename.split(".")[0]).lower()

if uploaded_file:
    try:
        # Step 1: Read CSV into DataFrame
        df = pd.read_csv(uploaded_file)
        st.success("✅ CSV loaded successfully!")
        st.dataframe(df.head())

        # Step 2: Save file locally
        uploads_dir = Path("uploads")
        uploads_dir.mkdir(exist_ok=True)
        file_path = uploads_dir / uploaded_file.name

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.info(f"📁 File saved as: `{file_path.name}`")

        # Step 3: Connect to SQLite and create table
        conn = sqlite3.connect("hr.db")
        table_name = sanitize_table_name(uploaded_file.name)

        # Step 4: Insert into SQLite safely
        df.to_sql(table_name, conn, if_exists="replace", index=False)

        st.success(f"📥 Data successfully inserted into `{table_name}` table in SQLite!")
        st.code(f"SELECT * FROM {table_name} LIMIT 5;", language="sql")

        conn.close()

    except Exception as e:
        st.error(f"❌ Unexpected error while uploading: {e}")
