import streamlit as st
import pandas as pd

class Movie:
    def __init__(self, movie_id, genres, title_year):
        self.movie_id = movie_id
        self.genres = genres
        self.title_year = title_year

class User:
    def __init__(self, user_id, age, gender, occupation):
        self.user_id = user_id
        self.age = age
        self.gender = gender
        self.occupation = occupation

class Rating:
    def __init__(self, user_id, movie_id, rating):
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating
        
# Cargar datos de items.txt
items_data = pd.read_csv("data/items.txt", sep='\t', names=['MovieID'] + [f'Genre_{i}' for i in range(1, 20)] + ['TitleYear'], encoding="latin-1")
movies = {row['MovieID']: Movie(row['MovieID'], row.iloc[1:20], row['TitleYear']) for _, row in items_data.iterrows()}

# Cargar datos de users.txt
users_data = pd.read_csv("data/users.txt", sep='\t', names=['UserID', 'Age', 'Gender', 'Occupation'], encoding="utf-8")
users = {row['UserID']: User(row['UserID'], row['Age'], row['Gender'], row['Occupation']) for _, row in users_data.iterrows()}

def rate_movie(user_id, movie_id, rating):
    # Define the file path
    filepath = "data/u1_base.txt"
    
    # Read the existing ratings into a DataFrame
    try:
        ratings_data = pd.read_csv(filepath, sep='\t', names=['UserID', 'MovieID', 'Rating'], encoding="utf-8")
    except pd.errors.EmptyDataError:
        ratings_data = pd.DataFrame(columns=['UserID', 'MovieID', 'Rating'])
    
    # Check if the user has already rated this movie and remove the old rating
    mask = (ratings_data['UserID'] != user_id) | (ratings_data['MovieID'] != movie_id)
    updated_ratings = ratings_data[mask]
    
    # Append the new rating
    new_rating = pd.DataFrame([[user_id, movie_id, rating]], columns=['UserID', 'MovieID', 'Rating'])
    updated_ratings = pd.concat([updated_ratings, new_rating], ignore_index=True)
    
    # Write the updated DataFrame back to the file
    updated_ratings.to_csv(filepath, sep='\t', index=False, header=False)

st.title("Rate movies!")

movie_names = [movie.title_year for movie_id, movie in movies.items()]

highest_id = len(users)
user_id = st.number_input("Please enter your User ID:", 1, highest_id, None, key = "user_id_rating")

if user_id is not None:
    movie_name = st.selectbox("Select the movie you would like to rate", movie_names)
    movie_id = movie_names.index(movie_name)+1

    rating = st.slider("Rate the movie on a scale from 1 to 5", min_value=1, max_value=5)
    
    if st.button("Rate"):
        rate_movie(user_id, movie_id, rating)
        st.success("Movie was rated successfully!")