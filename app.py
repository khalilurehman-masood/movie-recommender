import streamlit as st
import pickle
import pandas as pd
import requests
API='044c439f347c78aaf89c397898617a70'
movies_df = pd.read_pickle('movies.pkl')
similarities = pickle.load(open('similarities.pkl','rb'))

movies_titles = movies_df['title'].values
st.title('Movie Recommender System')

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwNDRjNDM5ZjM0N2M3OGFhZjg5YzM5Nzg5ODYxN2E3MCIsIm5iZiI6MTcyMjg2Mzc0Ni43ODk2MjMsInN1YiI6IjY2YjBjZjVkOWNmMGFhNzI1ZmExMTdiYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.vM1dANx63Hi6a7nbMMaw9T0AXxblQtY82fvlvsYJqBA"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies_df[movies_df['title']==movie].index[0]
    similarity = similarities[movie_index]

    similar_movies = sorted(list(enumerate(similarity)), reverse=True,key=lambda x:x[1])[1:6]
    sim_movies = []
    for item in similar_movies:
        sim_movies.append(movies_df.iloc[item[0]])

    return sim_movies



selected_movie_name = st.selectbox(
    'Select a movie to find similar movies.',
    movies_titles
)

if st.button('Recommend'):
    similar_movies = recommend(selected_movie_name)
    for i in similar_movies:
        poster_path = fetch_poster(i.movie_id)
        st.header(i.title)
        st.image(poster_path)
        
    

