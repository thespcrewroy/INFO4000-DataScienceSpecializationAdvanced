"""This is a simple Streamlit app to visualize data."""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

"""Generate a sine wave and displays it using Matplotlib in a Streamlit app."""
x = np.arange(0, 10, 0.1)
y = np.sin(x)

"""Create a simple line plot using Matplotlib and displays it in a Streamlit app."""
fig, ax = plt.subplots()
ax.plot(x, y)

"""Display the Matplotlib figure in the Streamlit app."""
st.pyplot(fig)