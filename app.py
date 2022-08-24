import pickle
import requests
import pandas as pd
import streamlit as st

st.title('Movie Recommender System')

movies_list = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_list)

similarity = pickle.load(open('similarity (1).pkl', 'rb'))


def fetch_poster(movi_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=4518644790353540e1317e4b10be4b4a'.format(movi_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movi_index = movies[movies["original_title"] == movie].index[0]
    similar = similarity[movi_index]
    similar_movi = sorted(list(enumerate(similar)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_poster_path = []
    for i in similar_movi:
        movi_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].original_title)
        # fetch poster
        recommended_poster_path.append(fetch_poster(movi_id))
    return recommended_movies,recommended_poster_path



selected_movie_name = st.selectbox(
    'Select Movie Name',
    movies['original_title'].values)

if st.button('Recommend'):
    name,posters = recommend(selected_movie_name)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.text(name[0])
        st.image(posters[0])

    with col2:
        st.text(name[1])
        st.image(posters[1])


    with col3:
        st.text(name[2])
        st.image(posters[2])


    # for i in recommendations:
    #     st.write(i)
