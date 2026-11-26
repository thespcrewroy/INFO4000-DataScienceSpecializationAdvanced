"""This is a comprehensive Streamlit form that collects user information."""
from time import time
import streamlit as st

"""Create a title for the Streamlit app."""
st.title("Comprehensive Streamlit Form")

"""Create a form in Streamlit to collect user information."""
with st.form("my_form"):
    st.header("User Information")
    name = st.text_input("Name") # text input for username
    bio = st.text_area("Bio") # text area for user bio
    age = st.number_input("Age", min_value=0, max_value=120, step=1) # number input for age
    dob = st.date_input("Date of Birth") # date input for date of birth
    subscribe = st.checkbox("Subscribe to newsletter") # checkbox for subscription
    gender = st.radio("Gender", options=["Male", "Female", "Other"]) # radio buttons for gender selection
    country = st.selectbox("Country", options=["USA", "India", "UK", "Other"]) # select box for country selection
    hobbies = st.multiselect("Hobbies", options=["Reading", "Traveling", "Gaming", "Cooking"]) # multiselect for hobbies
    satisfaction = st.slider("Satisfaction Level", min_value=0, max_value=10, step=1) # slider for satisfaction level
    uploaded_file = st.file_uploader("Upload a Profile Picture", type=["png", "jpg", "jpeg"]) # file uploader for profile picture
    favorite_color = st.color_picker("Pick a Favorite Color") # color picker for favorite color
    submitted = st.form_submit_button("Submit") # submit button for the form

    """Check if the form is submitted and display the entered information."""
    if submitted:
        st.success("Form submitted successfully!")
        st.write("### Entered Information :")
        st.write(f"**Full Name**: {name}")
        st.write(f"**Bio**: {bio}")
        st.write(f"**Age**: {age}")
        st.write(f"**Date of Birth**: {dob}")
        st.write(f"**Contact Time**: {time()}")
        st.write(f"**Subscribd**: {subscribe}")
        st.write(f"**Gender**: {gender}")
        st.write(f"**Country**: {country}")
        st.write(f"**Hobbies**: {', '.join(hobbies)}")
        st.write(f"**Satisfaction**: {satisfaction}")
        st.write(f"**Favorite Color**: {favorite_color}")
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Profile Picture", use_column_width=True)