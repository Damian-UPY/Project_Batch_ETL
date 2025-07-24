import streamlit as st
from utils.helpers import load_css

st.set_page_config(page_title="Cats Insights", page_icon="🐱", layout="wide")
load_css("styles/style.css")

st.title("🐾 Welcome to Cats Insights Dashboard")
st.write("Explore cat breeds, view images, and analyze categories using The Cat API data.")
st.markdown("---")
st.write("Navigate using the sidebar to explore different sections of the dashboard.")
