# NLP2SQL

## NL2SQL Streamlit App — README

This repository provides a Streamlit web app that generates SQL queries from natural language questions using the LLaMA-3-SQLCoder-8B model via Hugging Face Transformers. Users can input a database schema and a question, and the app returns a formatted SQL query.

---

## Features

- **Natural Language to SQL:** Converts user questions into SQL queries using a state-of-the-art LLM.
- **Custom Schema Support:** Paste or load your own database schema.
- **Query History:** View and manage your previous queries.
- **Formatted SQL Output:** Outputs are formatted for readability.
- **Streamlit UI:** Simple, interactive web interface.

---

## Dependencies

Add these to your `requirements.txt` or install with `pip install -r requirements.txt`:

```
streamlit>=1.25.0
torch>=2.0.0
transformers>=4.40.0
sqlparse>=0.4.4
```

> **Note:**
> - For best performance, a machine with a GPU supporting `bfloat16` is recommended.
> - The app downloads the model from Hugging Face (`defog/llama-3-sqlcoder-8b`). You may need to accept model terms on Hugging Face and may need to authenticate if running in a restricted environment.

---

## Quick Start

1. **Clone the Repository**

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the App**

```bash
streamlit run app.py
```

4. **Using the App**
    - Paste your database schema in the schema box or click "Load Sample Schema".
    - Enter your natural language question.
    - Click "Generate SQL Query" to see the generated query.
    - View your query history or clear it as needed.

---

## File Structure

```
.
├── app.py            # Main Streamlit application
├── requirements.txt  # Python dependencies
├── README.md         # This file
```


---

## Example Usage

- **Schema:**

```sql
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name VARCHAR(50),
    price DECIMAL(10,2),
    quantity INTEGER
);
```

- **Example Questions:**
_"List the names of all products with price greater than \$100"

"Show the names of customers who bought more than 5 products in a single sale."

"Find the average supply price for each product."

"What was the total quantity of products sold by region?"

"List all sales that occurred after January 1, 2024."

"Which suppliers supply products with a price lower than $50?"

"Get the total sales quantity per customer, sorted by highest to lowest."_
- **Generated SQL:**

```sql
SELECT name
FROM products
WHERE price > 100;
```


---

## Troubleshooting

- **Model Download Issues:**
If you face issues downloading the model, ensure you have a stable internet connection and access to Hugging Face Hub.
- **CUDA/Device Issues:**
The app will use GPU if available; otherwise, it will fall back to CPU (which is slower).
- **Streamlit Cache:**
The model is loaded with `@st.cache_resource` for faster reloads.

---

## License

This project is for research and educational purposes. Please check the license terms for the LLaMA-3-SQLCoder-8B model on Hugging Face before commercial use.

---

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)
- [Defog AI](https://huggingface.co/defog/llama-3-sqlcoder-8b)

---

## Contact

For questions or issues, please open an issue in this repository.

---


<div style="text-align: center">⁂</div>

[^1]: https://docs.streamlit.io/develop/api-reference/connections/st.connections.sqlconnection

[^2]: https://discuss.streamlit.io/t/running-a-sql-query-and-then-filtering-it-without-rerunning-the-script/83646

[^3]: https://github.com/prateekralhan/Natural-Language-2-SQL-Query

[^4]: https://www.youtube.com/watch?v=HBei8Pt9Ds8

[^5]: https://sqlgpt.streamlit.app

[^6]: https://stackoverflow.com/questions/79195754/how-to-use-downloaded-llama-model-in-streamlit

[^7]: https://blog.streamlit.io/snowchat-leveraging-openais-gpt-for-sql-queries/

[^8]: https://discuss.huggingface.co/t/need-help-performance-issues-transformers-automodelforcausallm-from-pretrained-mosaicml-mpt-7b-instruct/42882

