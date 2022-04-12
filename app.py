import streamlit as st
import pickle
import pandas as pd
import requests

# API KEY
API_KEY = ""


# import movies_data.pkl (dictionary)
movies_dict = pickle.load(open('movies_data.pkl', 'rb'))
movies_data = pd.DataFrame(movies_dict)  # Convert dictionary to dataframe

# import similarity_matrix.pkl
similarity_matrix = pickle.load(open('similarity_matrix.pkl', 'rb'))


def fetch_poster(movie_id, API_KEY):
    # Fetch poster from API
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US")
    data = response.json()
    poster_path = "https://image.tmdb.org/t/p/original" + data['poster_path']
    return poster_path


def recommend(movie):
    # Get movie index
    movie_index = movies_data[movies_data['title'] == movie].index[0]
    indices = pd.Series(similarity_matrix[movie_index].argsort()[-10:-1][::-1])

    # Get the title of the 10 most similar movies
    result_title = movies_data['title'].iloc[indices].values

    # Get the id of the 10 most similar movies
    result_id = movies_data['id'].iloc[indices].values

    # Fetch poster from API
    with st.spinner('Wait for it...'):
        result_poster = [fetch_poster(id, API_KEY) for id in result_id]
    st.title('Recommended films for you: ')

    # Return the result
    return result_title, result_poster


st.title('Movie Recommender System')


option = st.selectbox("Choose your favorite film",
                      (movies_data['title'].values))


st.markdown("""
<style>
.big-font {
    font-size:15px !important;
    font-weight:bold;
    margin-top:20px;
    margin-right:20px;
}
</style>
""", unsafe_allow_html=True)

if st.button('Recommend'):
    st.write('Selected Film:', option)
    results_title, results_poster = recommend(option)
    for i in range(0, 7, 3):
        for index, col in enumerate(st.columns(3)):
            with col:
                st.markdown(
                    f'<p class="big-font">{results_title[index + i]}</p>', unsafe_allow_html=True)
                st.image(results_poster[index + i], width=200)
