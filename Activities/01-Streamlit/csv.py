import streamlit as st
import pandas as pd
from pathlib import Path

"""
This is a simple Streamlit app that reads a CSV file and displays 
it in a table, bar chart, and a line chart.
"""
report_path = Path(__file__).parent / "report.csv" # get the path of the csv file
data = pd.read_csv(report_path) # read csv file using pandas
st.write(data) # write csv dataa to streamlit
st.bar_chart(data) # create a bar chart using the csv data
st.line_chart(data) # create a line chart using the csv data
