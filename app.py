import streamlit as st
import torch
import sqlparse
from transformers import AutoTokenizer, AutoModelForCausalLM

# Initialize model and tokenizer
@st.cache_resource
def load_model():
    # model_name = "./llama_3_sqlcoder_8b"
    model_name = "defog/llama-3-sqlcoder-8b"  # Hugging Face model path
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            load_in_4bit=False
        )
        return tokenizer, model
    except Exception as e:
        st.error(f"Failed to load model: {str(e)}")
        return None, None

# Prompt template
def generate_sql_prompt(question, schema):
    return f"""### Task
Generate a SQL query to answer the following question: {question}

### Database Schema
The query will run on a database with the following schema:
{schema}

### Answer
Given the database schema, here is the SQL query that answers {question}:
sql
"""

# Function to generate SQL query
def generate_sql_query(question, schema, tokenizer, model):
    if not tokenizer or not model:
        return "Error: Model not loaded."
    prompt = generate_sql_prompt(question, schema)
    try:
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to("cuda" if torch.cuda.is_available() else "cpu")
        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
            do_sample=False,
            num_beams=4
        )
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        sql_query = generated_text.split("sql")[1].split("```")[0].strip()
        formatted_sql = sqlparse.format(sql_query, reindent=True, keyword_case="upper")
        return formatted_sql
    except Exception as e:
        return f"Error: Could not generate SQL query. {str(e)}"

# Streamlit app
st.title("NL2SQL Interface with LLaMA-3-SQLCoder-8B")
st.write("Enter a database schema and a natural language query to generate a SQL query.")

# Initialize session state for query history
if "query_history" not in st.session_state:
    st.session_state.query_history = []

# Sample schema
sample_schema = """
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY, -- Unique ID for each product
    name VARCHAR(50), -- Name of the product
    price DECIMAL(10,2), -- Price of each unit of the product
    quantity INTEGER  -- Current quantity in stock
);

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY, -- Unique ID for each customer
    name VARCHAR(50), -- Name of the customer
    address VARCHAR(100) -- Mailing address of the customer
);

    CREATE TABLE salespeople (
    salesperson_id INTEGER PRIMARY KEY, -- Unique ID for each salesperson 
    name VARCHAR(50), -- Name of the salesperson
    region VARCHAR(50) -- Geographic sales region 
);

    CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY, -- Unique ID for each sale
    product_id INTEGER, -- ID of product sold
    customer_id INTEGER,  -- ID of customer who made purchase
    salesperson_id INTEGER, -- ID of salesperson who made the sale
    sale_date DATE, -- Date the sale occurred 
    quantity INTEGER -- Quantity of product sold
);

    CREATE TABLE product_suppliers (
    supplier_id INTEGER PRIMARY KEY, -- Unique ID for each supplier
    product_id INTEGER, -- Product ID supplied
    supply_price DECIMAL(10,2) -- Unit price charged by supplier
);

-- sales.product_id can be joined with products.product_id
-- sales.customer_id can be joined with customers.customer_id 
-- sales.salesperson_id can be joined with salespeople.salesperson_id
-- product_suppliers.product_id can be joined with products.product_id
"""

# Input fields
col1, col2 = st.columns([3, 1])
with col1:
    schema = st.text_area("Database Schema (e.g., CREATE TABLE ...)", height=200, value="")
with col2:
    if st.button("Load Sample Schema"):
        schema = sample_schema
        st.session_state.schema = schema

# Update schema from input
if "schema" not in st.session_state:
    st.session_state.schema = schema
schema = st.session_state.schema

question = st.text_input("Natural Language Query", placeholder="e.g., What is the average salary of employees in the Engineering department?")

# Load model and tokenizer
with st.spinner("Loading model... This may take a few minutes."):
    tokenizer, model = load_model()

# Generate SQL button
if st.button("Generate SQL Query", key="generate"):
    if schema.strip() and question.strip():
        with st.spinner("Generating SQL query..."):
            sql_query = generate_sql_query(question, schema, tokenizer, model)
            st.subheader("Generated SQL Query:")
            st.code(sql_query, language="sql")
            # Add to query history
            st.session_state.query_history.append({"question": question, "schema": schema, "sql": sql_query})
    else:
        st.error("Please provide both a database schema and a query.")

# Display query history
if st.session_state.query_history:
    st.subheader("Query History")
    for i, entry in enumerate(st.session_state.query_history[-5:]):  # Show last 5 queries
        with st.expander(f"Query {i+1}: {entry['question']}"):
            st.write("*Schema:*")
            st.code(entry["schema"], language="sql")
            st.write("*Generated SQL:*")
            st.code(entry["sql"], language="sql")

# Clear history button
if st.button("Clear Query History"):
    st.session_state.query_history = []
    st.rerun()
