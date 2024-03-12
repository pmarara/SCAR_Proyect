import streamlit as st
from streamlit_card import card

st.title("Welcome to the Palu movie recommender!")  

highest_id = 943
uid = st.number_input("Please enter your User ID:", 1, highest_id, None)
  
if uid is not None:
  rec = st.selectbox("Pick type of recommendation", ["Demographic", "Based on content", "Collaborative", "Hybrid"])
  
  recommendations = []
  class Recommendation:
      def __init__(self, title, ratio):
          self.title = title
          self.ratio = ratio
  recommendations.append(Recommendation("Inception", 88))
  recommendations.append(Recommendation("The Dark Knight", 90))
  recommendations.append(Recommendation("The Godfather", 92))
  
  for i, e in enumerate(recommendations):
    card(
      key="card" + str(i),
      title=e.title,
      text="Ratio: " + str(e.ratio),
      styles={
        "card": {
          "width": "700px",
          "height": "150px",
          "margin": "0px",
          "box-shadow": "none",
        },
        "title": {
          "font-size": "1.75em",
        }
      }
    )