import pickle
import streamlit as st
import requests

# Fetch poster function
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Apply styles
st.markdown(
    """
    <style>
    .big-font {
        font-size: 50px;
        text-align: center;
        color: #ff6347;
    }
    .movie-box {
        text-align: center;
        border: 2px solid #ccc;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .movie-box img {
        border-radius: 10px;
        max-height: 300px;
    }
    .big-button {
        background-color: #ff6347;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 20px;
        border: none;
        cursor: pointer;
    }
    .big-button:hover {
        background-color: #e5533e;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="big-font">✨ Movie Recommender System ✨</p>', unsafe_allow_html=True)

movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('<p class="big-button">Show Recommendation</p>', unsafe_allow_html=True):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)

    for i, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            st.markdown(f'<div class="movie-box"><p>{recommended_movie_names[i]}</p><img src="{recommended_movie_posters[i]}" width="200" /></div>', unsafe_allow_html=True)
