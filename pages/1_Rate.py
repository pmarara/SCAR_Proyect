import streamlit as st

import sys
sys.path.append('../')
from Recommendation import Movie, movies, users

st.title("Rate movies!")

movie_names = [movie.title_year for movie_id, movie in movies.items()]

highest_id = len(users)
user_id = st.number_input("Please enter your User ID:", 1, highest_id, None, key = "user_id_rating")

if user_id is not None:
    movie_name = st.selectbox("Select the movie you would like to rate", movie_names)
    movie_id = movie_names.index(movie_name)+1

    rating = st.slider("Rate the movie on a scale from 1 to 5", min_value=1, max_value=5)
    
    if st.button("Rate"):
        #rate_movie(user_id, movie_id, rating)
        st.success("Movie was rated successfully!")