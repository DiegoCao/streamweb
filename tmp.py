import pandas as pd
import streamlit as st

df = pd.read_csv("./eplusmtr.csv")
print(df)
st.table(df)
