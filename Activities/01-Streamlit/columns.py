import streamlit as st

"""
This is a simple Streamlit app to demonstrate the use of columns.
"""
col1, col2, col3 = st.columns(3)

col1.write("This is column 1")
col1.text_area("Enter text in column 1", height=150)

col2.write("This is column 2")
col3.write("This is column 3")