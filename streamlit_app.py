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

def fetch_overview(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=3dce868e6efecb8a0cbe08fd02e79f43&language=en-US'.format(
            movie_id))
    data = response.json()
    return data['overview']

def fetch_other_info(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=3dce868e6efecb8a0cbe08fd02e79f43&language=en-US'.format(
            movie_id))
    data = response.json()
    return data['release_date']

def fetch_runtime(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=3dce868e6efecb8a0cbe08fd02e79f43&language=en-US'.format(
            movie_id))
    data = response.json()
    return data['runtime']

def fetch_status_info(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=3dce868e6efecb8a0cbe08fd02e79f43&language=en-US'.format(
            movie_id))
    data = response.json()
    return data['status']

def fetch_vote_avg(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=3dce868e6efecb8a0cbe08fd02e79f43&language=en-US'.format(
            movie_id))
    data = response.json()
    return data['vote_average']

def fetch_vote_count(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=3dce868e6efecb8a0cbe08fd02e79f43&language=en-US'.format(
            movie_id))
    data = response.json()
    return data['vote_count']


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


add_bg_from_local('wallpaper.jpg')


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_overview = []
    movie_release_date = []
    movie_status = []
    vote_rating = []
    vote_total = []
    movie_runtime = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id

        # fetching Poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_overview.append(fetch_overview(movie_id))
        movie_release_date.append(fetch_other_info(movie_id))
        movie_status.append(fetch_status_info(movie_id))
        vote_rating.append(fetch_vote_avg(movie_id))
        movie_runtime.append(fetch_runtime(movie_id))
        vote_total.append(fetch_vote_count(movie_id))

    return recommended_movies, recommended_movies_posters, recommended_movies_overview, movie_release_date, movie_status, \
           vote_rating, vote_total, movie_runtime


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)

new_header = '<p style="color:#f5d547; font-size: 42px; text-align: center; -webkit-text-stroke: 1px #00ff00;">🎬📽️ ' \
             '𝓒𝓲𝓷𝓮-𝓢𝓾𝓰𝓰𝓮𝓼𝓽 📽️🎬</p> '
st.markdown(new_header, unsafe_allow_html=True)

selected_movie_name = st.selectbox('Enter Movie name to get recommendations :-', movies['title'].values)


if st.button('Show Recommendations'):
    names, posters, overview, release_date, status, rating, vote_count, runtime = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown('<div style="border: 2px solid white; padding: 10px; border-radius: 10px;">'
                    f'<img src="{posters[0]}" style="max-width: 100%;"</div>', unsafe_allow_html = True)
        st.markdown(f'<div style="text-align: center;">{names[0]}</div>', unsafe_allow_html = True)

    with col2:
        st.markdown('<div style="border: 2px solid white; padding: 10px; border-radius: 10px;">'
                    f'<img src="{posters[1]}" style="max-width: 100%;"</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="text-align: center;">{names[1]}</div>', unsafe_allow_html = True)

    with col3:
        st.markdown('<div style="border: 2px solid white; padding: 10px; border-radius: 10px;">'
                    f'<img src="{posters[2]}" style="max-width: 100%;"</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="text-align: center;">{names[2]}</div>', unsafe_allow_html = True)

    with col4:
        st.markdown('<div style="border: 2px solid white; padding: 10px; border-radius: 10px;">'
                    f'<img src="{posters[3]}" style="max-width: 100%;"</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="text-align: center;">{names[3]}</div>', unsafe_allow_html = True)

    with col5:
        st.markdown('<div style="border: 2px solid white; padding: 10px; border-radius: 10px;">'
                    f'<img src="{posters[4]}" style="max-width: 100%;"</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="text-align: center;">{names[4]}</div>', unsafe_allow_html = True)


    for i in range(len(names)):
        st.markdown('<hr>', unsafe_allow_html=True)  # Add a horizontal line to separate recommendations
        st.write("")  # Create some space
        st.markdown(f'<p style="color:Orange; font-size: 28px; text-align: center; -webkit-text-stroke: 1px White;">'
                    f'{names[i]}</div>', unsafe_allow_html=True)

        with st.container():  # Create a container for each recommendation
            st.write('<style>div[data-testid="stHorizontalBlock"] > div{width: 100%;}</style>', unsafe_allow_html=True)
            with st.expander("Overview"):
                st.markdown(
                    f'<div style="background-color: #122b52; padding: 10px; border-radius: 10px;">'
                    f'<span style="color:#69dbcc;">{overview[i]}</span>'
                    f'<br><br>'  # Add a line break for spacing
                    f'<span style="color:#098731;"><strong>Status: </strong></span> {status[i]}'
                    f'<br>'
                    f'<span style="color:#098731;"><strong>Release Date:</strong></span> {release_date[i]}'
                    f'<br>'
                    f'<span style="color:#098731;"><strong>Runtime:</strong>:</span> {runtime[i]} minutes'
                    f'<br>'
                    f'<span style="color:#098731;"><strong>Rating:</strong></span> {rating[i]}'
                    f'<br>'
                    f'<span style="color:#098731;"><strong>Total Votes:</strong></span> {vote_count[i]}'
                    f'</div>',
                    unsafe_allow_html=True
                )

            st.markdown(
                f'<div style="padding: 10px; border-radius: 10px; text-align: center;">'
                f'<img src="{posters[i]}" style="max-width: 100%; margin: 0 auto; border: 3px solid white;"></div>',
                unsafe_allow_html=True
            )
