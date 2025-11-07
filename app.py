import streamlit as st
import pandas as pd

st.set_page_config(page_title="Excel Data Search", layout="wide")

st.title("🔍 Excel Data Search")
st.write("Search any text from your Excel file and see all matching rows.")

# Path to your Excel file in root folder
EXCEL_FILE = "2002 AC 63.xlsx"

# Load data once and cache it
@st.cache_data
def load_data():
    return pd.read_excel(EXCEL_FILE, engine="openpyxl")

try:
    df = load_data()
    st.success(f"✅ Loaded {EXCEL_FILE} successfully!")
    st.write("### Data Preview:")
    st.dataframe(df.head())

    # Search input
    search_term = st.text_input("🔎 Enter text to search:")

    if search_term:
        # Search across all columns (case-insensitive)
        filtered_df = df[df.apply(lambda row: row.astype(str)
                                  .str.contains(search_term, case=False, na=False)
                                  .any(), axis=1)]

        if not filtered_df.empty:
            st.write(f"### Results for '{search_term}':")
            st.dataframe(filtered_df)
            st.info(f"Total matches found: {len(filtered_df)}")
        else:
            st.warning(f"No results found for '{search_term}'.")
    else:
        st.info("Type something above to search in the Excel data.")

except FileNotFoundError:
    st.error(f"❌ File '{EXCEL_FILE}' not found. Please make sure it’s in the same folder as `app.py`.")
except Exception as e:
    st.error(f"⚠️ Error reading file: {e}")
