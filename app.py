import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=d165c32a1ef53a9d8c04ca5b305a55aa')
    data = response.json()
    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movies_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movies_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # Use the actual TMDB movie ID, not the index
        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetch poster from API using the movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
    
    # Ensure return only after completing the loop
    return recommended_movies, recommended_movies_poster

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Choose a movie:',
    movies['title'].values
)

if st.button('Recommended Movies for You:'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    #create 5 col in  single rowe
    cols= st.columns(5)
    # Ensure we have at least 5 recommendations
    for i in range(len(recommended_movie_names)):
          with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])

 





