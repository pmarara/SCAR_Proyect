import streamlit as st
import pandas as pd

class User:
    def __init__(self, user_id, age, gender, occupation):
        self.user_id = user_id
        self.age = age
        self.gender = gender
        self.occupation = occupation

users_data = pd.read_csv("users.txt", sep='\t', names=['UserID', 'Age', 'Gender', 'Occupation'], encoding="utf-8")
users = {row['UserID']: User(row['UserID'], row['Age'], row['Gender'], row['Occupation']) for _, row in users_data.iterrows()}
user_id = len(users)+1


def signupuser(id, age, sex, occupation):
    # Open the file in append mode
    with open("users.txt", "a") as file:
        file.write(f"\n{id}\t{age}\t{sex}\t{occupation}")
        users_data = pd.read_csv("users.txt", sep='\t', names=['UserID', 'Age', 'Gender', 'Occupation'], encoding="utf-8")
        users = {row['UserID']: User(row['UserID'], row['Age'], row['Gender'], row['Occupation']) for _, row in users_data.iterrows()}
        user_id = len(users)+1




st.title("Sign Up!")

st.number_input("ID", value=user_id, disabled=True)

age = st.slider("Age")

sex = st.selectbox("Sex", ["M", "F"])

occupation = st.selectbox("Occupation", ["none", "technician", "other", "writer", "executive", "administrator", "student", "lawyer", "educator", "scientist", "entertainment", "programmer", "librarian", "homemaker", "artist", "marketing", "healthcare", "retired", "salesman", "doctor"])

if st.button("Sign up"):
    signupuser(user_id, age, sex, occupation)
    st.success("User signed up successfully!")