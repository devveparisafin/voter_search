import streamlit as st
import pandas as pd

st.set_page_config(page_title="Excel Data Search", layout="wide")

# Load Excel file (change path if needed)
EXCEL_FILE = "data.xlsx"

@st.cache_data
def load_data():
    return pd.read_excel(EXCEL_FILE)

st.title("🔍 Excel Data Search")
st.write("Search and filter data from your Excel file.")

try:
    df = load_data()
    st.success("✅ Data loaded successfully!")

    # Search box
    search_term = st.text_input("Enter search keyword:")

    if search_term:
        # Filter rows where any column contains the search term (case-insensitive)
        results = df[df.apply(lambda row: row.astype(str)
                              .str.contains(search_term, case=False, na=False)
                              .any(), axis=1)]
        st.write(f"### Results for: '{search_term}'")
        st.dataframe(results)
        st.write(f"Total matches found: {len(results)}")
    else:
        st.dataframe(df.head(20))  # show first 20 rows as preview

except FileNotFoundError:
    st.error(f"❌ File '{EXCEL_FILE}' not found. Please place it in the same folder as this script.")
