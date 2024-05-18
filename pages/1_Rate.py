import streamlit as st
import pandas as pd
import numpy as np

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

    # Check if the user has 5 or more ratings with a score of 3 or higher
    high_rated_movies = updated_ratings[(updated_ratings['UserID'] == user_id) & (updated_ratings['Rating'] >= 3)]
    if len(high_rated_movies) >= 5:
        print("Vectores recalculados")
        # Recalculate vectors for content-based and collaborative filtering
        recalculate_vectors(user_id, updated_ratings)
    else:
        print("Not enough positive ratings")
    
def recalculate_vectors(user_id, ratings_data):
    # Calculate the content-based vector
    high_rated_movies = ratings_data[(ratings_data['UserID'] == user_id) & (ratings_data['Rating'] >= 3)]
    preference_vector = np.zeros(19)
    
    for _, row in high_rated_movies.iterrows():
        movie_id = row['MovieID']
        rating = row['Rating']
        multiplier = rating - 2  # 3 -> 1, 4 -> 2, 5 -> 3
        
        # Asegurarse de que el ID de la película exista en items_data
        if movie_id in items_data['MovieID'].values:
            movie_genres = items_data[items_data['MovieID'] == movie_id].iloc[0, 1:20].values.astype(int)
            preference_vector += movie_genres * multiplier
    
    # Normalize the vector to have a maximum value of 100
    max_value = preference_vector.max()
    if max_value > 0:
        preference_vector = (preference_vector / max_value) * 100
    
    # Update VectoresColaborativos.txt
    preference_vector = preference_vector.astype(int)
    preferences_array = np.where(preference_vector == 0, 1, preference_vector)
    preferences_str = '\t'.join(map(str, preferences_array.astype(int)))
    update_vector_file('data/VectoresColaborativos.txt', user_id, preferences_str)
    
    # Update VectoresBasadosContenido.txt
    top_indices = preference_vector.argsort()[-6:][::-1]
    top_preferences = np.zeros(19)
    top_preferences[top_indices] = preference_vector[top_indices]
    preferences_str = '\t'.join(map(str, top_preferences.astype(int)))
    update_vector_file('data/VectoresBasadosContenido.txt', user_id, preferences_str)

def update_vector_file(filepath, user_id, new_preferences):
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()
        with open(filepath, 'w') as file:
            for line in lines:
                if line.startswith(str(user_id) + '\t'):
                    file.write(f"{user_id}\t{new_preferences}\n")
                else:
                    file.write(line)
    except FileNotFoundError:
        with open(filepath, 'w') as file:
            file.write(f"{user_id}\t{new_preferences}\n")

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