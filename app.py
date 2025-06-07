import streamlit as st
import sqlite3
import os
import re
from groq import Groq
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=api_key)

# Streamlit page config
st.set_page_config(page_title="Ask Your HR Database", page_icon="📊")
st.title("📊 Ask Your HR Database")
st.caption("Ask a question in plain English (e.g., 'Show average salary by department')")

# Function to convert question to SQL
def generate_sql(question):
    prompt = f"""
You are an expert SQL assistant. Convert this natural language question into a valid SQLite SQL query.
Do NOT include ``` or any other formatting — return only the SQL query.

Question: {question}
Table: employees(id, name, department, designation, salary, location, hire_date)
"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# Function to execute SQL
def execute_sql_query(query):
    conn = sqlite3.connect("hr.db")
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        cols = [desc[0] for desc in cursor.description]
        return rows, cols
    except Exception as e:
        return str(e), []
    finally:
        conn.close()

# Input box
question = st.text_input("Ask a question:")

# Process query
if question:
    with st.spinner("⏳ Thinking..."):
        sql = generate_sql(question)
        st.subheader("💡 Generated SQL")
        st.code(sql, language="sql")

        result, cols = execute_sql_query(sql)

    if isinstance(result, str):
        st.error(f"❌ SQL Error: {result}")
    elif result:
        st.success("✅ Result:")
        st.dataframe([dict(zip(cols, row)) for row in result])
    else:
        st.warning("⚠️ No results found.")

# HR insights
with sqlite3.connect("hr.db") as conn:
    cur = conn.cursor()
    cur.execute("SELECT AVG(salary) FROM employees WHERE department='HR'")
    avg_salary = cur.fetchone()[0]

    cur.execute("SELECT MAX(salary) FROM employees WHERE department='HR'")
    max_salary = cur.fetchone()[0]

    cur.execute("SELECT name FROM employees WHERE department='HR' AND salary=(SELECT MAX(salary) FROM employees WHERE department='HR')")
    top_earners = cur.fetchall()

st.markdown("### 🔍 HR Department Salary Insights")
st.markdown(f"**Average Salary in HR:** 💰 ${avg_salary}")
st.markdown(f"**Highest Salary in HR:** 🏆 ${max_salary}")

st.markdown("**Top Earning Employee(s):**")
for name in top_earners:
    st.write(f"👤 {name[0]} (${max_salary})")
