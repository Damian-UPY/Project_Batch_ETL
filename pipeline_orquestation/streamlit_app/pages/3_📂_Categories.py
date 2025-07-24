import streamlit as st
import pandas as pd
from utils.mongo_conn import get_latest_dataset

st.title("📂 Cat Categories")

data = get_latest_dataset()

if data and isinstance(data, list):
    main_doc = data[0] if data else {}
    categories_list = main_doc.get('categories', [])

    if categories_list:
        categories = pd.DataFrame(categories_list)
        if not categories.empty:
            st.dataframe(categories[['id', 'name']])
        else:
            st.warning("Categories data is empty.")
    else:
        st.warning("No category data found in the dataset.")
else:
    st.warning("No data available.")
