import streamlit as st

st.title("Sign Up!")

age = st.slider("Age")

sex = st.selectbox("Sex", ["M", "F"])

occupation = st.selectbox("Occupation", ["none", "technician", "other", "writer", "executive", "administrator", "student", "lawyer", "educator", "scientist", "entertainment", "programmer", "librarian", "homemaker", "artist", "marketing", "healthcare", "retired", "salesman", "doctor"])

st.button("Sign up")