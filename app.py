import streamlit as st
import pandas as pd
import time
from thefuzz import fuzz

st.set_page_config(page_title="Gujarati Voter Search", layout="wide")

st.title("Viramgam Voter List - 2002")
EXCEL_FILE = "2002 AC 63.xlsx"

@st.cache_data
def load_data():
    return pd.read_excel(EXCEL_FILE, engine="openpyxl")

try:
    df = load_data()
    st.success("✅ Voter list loaded successfully!")

    search_term = st.text_input("🔍 Enter Gujarati name to search:")
    search_button = st.button("Search")

    if search_button:
        if not search_term.strip():
            st.warning("Please enter a name to search.")
        else:
            matched_rows = []

            with st.spinner("🔎 Searching voter list..."):
                time.sleep(0.3)

                for _, row in df.iterrows():
                    # Convert each cell to string for comparison
                    for cell in row.astype(str):
                        # Exact match or fuzzy match threshold
                        if (
                            search_term in cell
                            or fuzz.partial_ratio(search_term, cell) > 80
                        ):
                            matched_rows.append(row)
                            break  # move to next row once matched

                time.sleep(0.2)

            if matched_rows:
                result_df = pd.DataFrame(matched_rows)
                st.success(f"✅ Found {len(result_df)} possible matches.")
                st.dataframe(result_df, use_container_width=True)
            else:
                st.warning(f"No voters found similar to '{search_term}'.")

except FileNotFoundError:
    st.error(f"❌ '{EXCEL_FILE}' not found. Please keep it in the same folder as app.py.")
except Exception as e:
    st.error(f"⚠️ Error: {e}")
