import streamlit as st
import pickle
import pandas as pd
import base64
import requests


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=3dce868e6efecb8a0cbe08fd02e79f43&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
        unsafe_allow_html=True
    )


add_bg_from_local('movie_wallpaper.jpg')


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    recommended_movies_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id

        # fetching Poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)

new_header = '<p style="font-color:#8437cc; font-size: 42px;">📽️ 𝓒𝓲𝓷𝓮-𝓢𝓾𝓰𝓰𝓮𝓼𝓽 📽️</p>'
st.markdown(new_header, unsafe_allow_html=True)

selected_movie_name = st.selectbox('Enter Movie name to get recommendations :-', movies['title'].values)

if st.button('Show Recommendations'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0])
        st.write(names[0])

    with col2:
        st.image(posters[1])
        st.write(names[1])

    with col3:
        st.image(posters[2])
        st.write(names[2])

    with col4:
        st.image(posters[3])
        st.write(names[3])

    with col5:
        st.image(posters[4])
        st.write(names[4])
