# Interview Questions: LangChain DataFrame Agent

1. **What is an agent?** A model-driven workflow that can choose tools, inspect tool results, and continue until it can answer.
2. **How is an agent different from a fixed chain?** An agent can decide which tool to call and whether it needs another tool result.
3. **How does this app analyze one DataFrame?** The user asks a question; the model calls a Python/pandas tool; pandas computes a result; the model explains it.
4. **How are multiple datasets exposed?** Uploads become separate frames named `df1`, `df2`, `df3`, and so on.
5. **How would you join customers and orders?** Inspect key columns and data types, then merge on the verified customer key.
6. **Inner join vs left join?** Inner keeps matching keys; left preserves every row from the left table.
7. **What can go wrong in joins?** Wrong keys, inconsistent types, duplicates, null keys, or many-to-many relationships can distort totals.
8. **How do you validate a join?** Compare row counts, unmatched keys, key uniqueness, and reconciled aggregates.
9. **How do you count rows?** `len(df1)` or `df1.shape[0]`.
10. **How do you profile missing values?** `df1.isna().sum()`.
11. **How can the app be domain-agnostic?** Keep the loader and analysis tool generic; inspect the actual schema and ask users to clarify business meaning where needed.
12. **Does the agent automatically know all information?** No. It must inspect and calculate from available columns; it can fail if data or context is incomplete.
13. **Why use `create_agent` and `invoke`?** This is the current LangChain agent pattern; older `agent.run(...)` usage is not used here.
14. **Why is model-generated Python risky?** It can execute unintended operations. Isolate it in a sandbox before deploying to other users.
15. **How do you reduce hallucinations?** Require tool-backed calculations, inspect schema, state assumptions, and validate important outputs independently.
16. **How would you support very large files?** Use profiling, chunking, DuckDB/SQL, or a database instead of loading everything into a prompt.
17. **How would you add charting?** Have the tool return a bounded result table, then render charts with Streamlit.
18. **How would you test this project?** Test loaders, namespace mapping, joins, missing values, unsupported files, API failures, and sandbox controls.

## Demo sequence
1. Upload one CSV and ask for row count.
2. Ask for missing-value counts and group-by analysis.
3. Upload customers and orders; ask for a validated join.
4. Add products as a third file; ask for revenue by category.
5. Explain tool selection, Python execution, tool observations, and the final answer.
