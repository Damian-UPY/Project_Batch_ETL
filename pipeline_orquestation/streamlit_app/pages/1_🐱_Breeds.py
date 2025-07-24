import streamlit as st
import pandas as pd
from utils.mongo_conn import get_latest_dataset
from utils.charts import plot_avg_intelligence

st.title("🐱 Cat Breeds Overview")

data = get_latest_dataset()

if isinstance(data, list) and len(data) > 0:
    main_doc = data[0] if isinstance(data[0], dict) else {}

    breeds_list = main_doc.get('breeds', []) if isinstance(main_doc, dict) else []

    if breeds_list and isinstance(breeds_list, list):
        breeds = pd.DataFrame(breeds_list)
        st.subheader("Raw Breeds Data")
        st.dataframe(breeds)

        # Solo mostrar columnas si existen
        cols_to_show = [col for col in ['name', 'origin', 'intelligence'] if col in breeds.columns]
        if cols_to_show:
            st.subheader("Filtered Columns")
            st.dataframe(breeds[cols_to_show])

            if 'intelligence' in breeds.columns:
                fig = plot_avg_intelligence(breeds)
                st.plotly_chart(fig)
        else:
            st.warning("No expected columns found.")
    else:
        st.warning("No breed data found in the dataset.")
else:
    st.warning("No data available.")
