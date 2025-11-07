import streamlit as st
import pandas as pd

st.set_page_config(page_title="Excel Row Search", layout="wide")

st.title("🔍 Excel Row Search")
st.write("Enter a keyword and click **Search** to display all rows containing that text.")

EXCEL_FILE = "2002 AC 63.xlsx"

@st.cache_data
def load_data():
    return pd.read_excel(EXCEL_FILE, engine="openpyxl")

try:
    df = load_data()
    st.success("✅ Excel file loaded successfully!")

    # Search input + button
    search_term = st.text_input("Enter text to search:")
    search_button = st.button("🔍 Search")

    if search_button:
        if not search_term.strip():
            st.warning("Please enter a search term.")
        else:
            matched_rows = []

            # Go row by row
            for _, row in df.iterrows():
                # If row contains the text (case-insensitive)
                if row.astype(str).str.contains(search_term, case=False, na=False).any():
                    matched_rows.append(row)

            # Display results
            if matched_rows:
                result_df = pd.DataFrame(matched_rows)
                st.success(f"✅ Found {len(result_df)} matching rows.")
                st.dataframe(result_df)
            else:
                st.warning(f"No rows found containing '{search_term}'.")

except FileNotFoundError:
    st.error(f"❌ '{EXCEL_FILE}' not found. Please keep it in the same folder as app.py.")
except Exception as e:
    st.error(f"⚠️ Error: {e}")
