from io import BytesIO
import pandas as pd

def read_dataframe_bytes(filename: str, content: bytes) -> pd.DataFrame:
    """Load CSV or Excel bytes into a pandas DataFrame."""
    name = filename.lower()
    if name.endswith(".csv"):
        return pd.read_csv(BytesIO(content))
    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(BytesIO(content))
    raise ValueError(f"Unsupported file type: {filename}")

def build_namespace(datasets: dict) -> dict:
    """Expose frames as df1, df2, ... and in a named datasets registry."""
    namespace = {"pd": pd}
    frames = {}
    for i, frame in enumerate(datasets.values(), start=1):
        name = f"df{i}"
        namespace[name] = frame
        frames[name] = frame
    namespace["datasets"] = frames
    return namespace
