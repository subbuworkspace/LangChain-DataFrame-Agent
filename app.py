import os
import streamlit as st
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_experimental.tools.python.tool import PythonAstREPLTool
from langchain_google_genai import ChatGoogleGenerativeAI
from data_utils import read_dataframe_bytes, build_namespace

load_dotenv()
st.set_page_config(page_title="LangChain DataFrame Agent", page_icon="📊", layout="wide")
st.title("📊 LangChain DataFrame Agent")
st.write("Upload one or more CSV/Excel datasets. Ask questions in plain English; the agent uses Python and pandas to calculate answers.")

with st.sidebar:
    st.header("Upload data")
    uploads = st.file_uploader("CSV / Excel files", type=["csv", "xlsx", "xls"], accept_multiple_files=True)
    st.caption("Upload order maps to df1, df2, df3, etc.")
    st.warning("This demo executes model-generated Python. Use locally with trusted data; sandbox before deployment.")

if not uploads:
    st.info("Upload data to start.")
    st.markdown("""
**Single dataset:** “How many rows?”, “Show missing values”, “Top 10 products by revenue.”

**Multiple datasets:** “Join customers and orders on customer_id and calculate spend per customer.”

**Three datasets:** “Join customers, orders and products; calculate revenue by product category.”
""")
    st.stop()

datasets, errors = {}, []
for upload in uploads:
    try:
        datasets[upload.name] = read_dataframe_bytes(upload.name, upload.getvalue())
    except Exception as exc:
        errors.append(f"{upload.name}: {exc}")
for error in errors:
    st.error(error)
if not datasets:
    st.stop()

st.subheader("Loaded datasets")
cols = st.columns(min(len(datasets), 3))
for i, (name, df) in enumerate(datasets.items(), start=1):
    with cols[(i - 1) % len(cols)]:
        st.metric(name, f"{len(df):,} rows", f"{len(df.columns)} columns")
        with st.expander("Preview"):
            st.dataframe(df.head(10), use_container_width=True)
            st.caption("Columns: " + ", ".join(map(str, df.columns)))

question = st.text_area("Ask a question about your data", placeholder="Compare average sales across regions, or join two files and find unmatched IDs.")
if st.button("Analyze", type="primary", disabled=not question.strip()):
    try:
        key = os.getenv("GEMINI_API_KEY", "").strip()
        if not key:
            st.error("Set GEMINI_API_KEY in your .env file.")
            st.stop()
        model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
        llm = ChatGoogleGenerativeAI(model=model, google_api_key=key, temperature=0, timeout=60, max_retries=2)
        namespace = build_namespace(datasets)
        tool = PythonAstREPLTool(
            locals=namespace,
            name="python_dataframe",
            description="Use Python/pandas to analyze uploaded data. Frames are df1, df2, df3, etc.; datasets maps these names to frames. Inspect columns before joins. Compute results from data; do not guess."
        )
        agent = create_agent(
            model=llm,
            tools=[tool],
            system_prompt=(
                "You are a careful data analyst. Use python_dataframe for factual calculations. "
                "The first uploaded file is df1, second df2, third df3, and so on. Inspect columns, "
                "types, and keys as needed. For multi-file questions, join only on appropriate keys. "
                "Explain assumptions and missing information. Never invent results. Return a concise answer."
            ),
        )
        mapping = "; ".join(
            f"df{i}: {name}, {len(df)} rows, columns={list(df.columns)}"
            for i, (name, df) in enumerate(datasets.items(), start=1)
        )
        with st.spinner("Agent is analyzing the data..."):
            result = agent.invoke({"messages": [{"role": "user", "content": f"Datasets: {mapping}\nQuestion: {question}"}]})
        messages = result.get("messages", [])
        final = next((m for m in reversed(messages) if getattr(m, "type", "") == "ai" and getattr(m, "content", "")), None)
        answer = final.content if final else "No final answer returned."
        if isinstance(answer, list):
            answer = "\n".join(str(p.get("text", p)) if isinstance(p, dict) else str(p) for p in answer)
        st.subheader("Answer")
        st.write(answer)
    except Exception as exc:
        st.error(f"Analysis failed: {exc}")
        st.caption("Check your API key, model access, package compatibility, and terminal logs.")
