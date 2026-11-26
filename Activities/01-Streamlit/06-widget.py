"""This is a simple Streamlit app that demonstrates the use of a slider widget."""

import streamlit as st

"""Create a slider widget in the Streamlit app and display the selected value."""
x = st.slider("Select a value", 0, 100, 50)
st.write("You selected:", x)