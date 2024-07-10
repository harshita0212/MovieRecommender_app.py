import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    api_key = '4b2449664e5042243b4da762487beb48'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}'
    params = {
        'api_key': api_key,
        'language': 'en-US'
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return None


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]]['movie_id']
        print(movies.head())
        # Fetch poster from API
        recommended_movies.append(movies.iloc[i[0]].title)
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommended_movies_posters.append(poster_url)
        else:
            recommended_movies_posters.append(
                "https://via.placeholder.com/500")  # Placeholder image if poster is not available
    return recommended_movies, recommended_movies_posters


# Load movie data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Load similarity data
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Which movie would you like to watch?',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    for i in range(len(names)):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text(names[i])
            st.image(posters[i])
        if i + 1 < len(names):
            with col2:
                st.text(names[i + 1])
                st.image(posters[i + 1])
        if i + 2 < len(names):
            with col3:
                st.text(names[i + 2])
                st.image(posters[i + 2])