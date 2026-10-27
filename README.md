# LangChain DataFrame Agent

Upload CSV/Excel files and ask data questions in plain English. The Streamlit UI uses a LangChain agent and a Python/pandas tool to calculate answers from one or multiple DataFrames.

## Features
- Single-table profiling, filtering, aggregation, and summaries.
- Two or more datasets, with frames exposed as `df1`, `df2`, `df3`, etc.
- Natural-language questions; the user does not need to write pandas code.
- Generic tabular workflow applicable to sales, finance, HR, operations, marketing, logistics, and other domains.
- Simple tests for data loading and dataframe namespace mapping.

## How it works
1. Upload one or more CSV/Excel files.
2. pandas loads them into DataFrames.
3. The app exposes the frames to the tool as `df1`, `df2`, `df3`, etc.
4. The user asks a natural-language question.
5. The model decides to call the Python tool and creates a data-analysis operation.
6. Python/pandas executes it and returns observations.
7. The model uses the observed results to form a readable response.

An agent is not automatically omniscient. Answers depend on available columns, data quality, tool execution, and correctly understood business definitions.

## Multi-dataset examples
- **Two files:** `customers.csv` + `orders.csv`: “Join on customer_id and calculate total spend per customer.”
- **Three files:** customers + orders + products: “Join the tables using verified keys and calculate revenue by product category.”
- **More files:** the same pattern continues (`df4`, `df5`, ...). Specify join keys when they are ambiguous. Validate row counts and unmatched keys before trusting totals.

## Setup (Windows)
Use Python 3.11 or 3.12 in a clean virtual environment.

PowerShell:
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Git Bash:
```bash
py -3.12 -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your own Gemini API key. Set `GEMINI_MODEL` to a model currently available to your account. Never commit `.env`.

Run:
```bash
python -m streamlit run app.py
```
Open the local URL printed in the terminal, typically `http://localhost:8501`.

## Package troubleshooting
This uses `create_agent` and `agent.invoke({"messages": [...]})`, not the older `agent.run(...)` pattern. If packages conflict:
```bash
python -m pip check
python -m pip show langchain langchain-core langchain-experimental langchain-google-genai langsmith
```
Prefer a fresh virtual environment over repeated individual downgrades.

## Security warning
`PythonAstREPLTool` executes model-generated Python. This demo is intended for local learning with trusted data. Before deployment, run execution in a sandbox/container with strict filesystem, network, time, and resource limits; add authentication, upload limits, auditing, and data privacy controls. Do not upload confidential or regulated data unless authorized and appropriately protected.

## Files
```text
langchain_dataframe_agent/
├── app.py
├── data_utils.py
├── tests/test_data_utils.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── INTERVIEW_QUESTIONS.md
└── LINKEDIN_POST.txt
```
