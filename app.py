import pickle
import streamlit as st
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500x750.png?text=Poster+Not+Available"  # Placeholder for missing posters
    except Exception as e:
        return "https://via.placeholder.com/500x750.png?text=Error+Fetching+Poster"

# Recommendation function
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:  # Top 5 recommendations
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        st.error(f"An error occurred while recommending movies: {e}")
        return [], []

# Streamlit UI setup
st.header('Movie Recommender System')

# Load data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Dropdown for movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Show recommendations when the button is clicked
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Display recommendations in a grid
    if recommended_movie_names:
        cols = st.columns(5)  # Create 5 columns
        for idx, col in enumerate(cols):
            if idx < len(recommended_movie_names):
                with col:
                    st.text(recommended_movie_names[idx])
                    st.image(recommended_movie_posters[idx])
    else:
        st.error("No recommendations found. Please select a valid movie.")





