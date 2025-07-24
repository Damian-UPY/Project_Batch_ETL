import streamlit as st
import pandas as pd
from utils.mongo_conn import get_latest_dataset

st.title("🖼️ Cat Images")

data = get_latest_dataset()

if isinstance(data, list) and len(data) > 0:
    main_doc = data[0] if isinstance(data[0], dict) else {}

    images_list = main_doc.get('images', []) if isinstance(main_doc, dict) else []

    if images_list and isinstance(images_list, list):
        images = pd.DataFrame(images_list)
        st.subheader("Raw Images Data")
        st.dataframe(images)

        if not images.empty:
            for _, row in images.iterrows():
                url = row.get('url') if 'url' in row else None
                if url:
                    st.image(url, caption=row.get('id', ''), width=250)
    else:
        st.warning("No image data found in the dataset.")
else:
    st.warning("No data available.")

