import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data.csv')
    return df

df = load_data()

# Data preprocessing
df['in_theaters_date'] = pd.to_datetime(df['in_theaters_date'], errors='coerce')
df['on_streaming_date'] = pd.to_datetime(df['on_streaming_date'], errors='coerce')
df['runtime_in_minutes'] = pd.to_numeric(df['runtime_in_minutes'], errors='coerce')
df['tomatometer_rating'] = pd.to_numeric(df['tomatometer_rating'], errors='coerce')
df['audience_rating'] = pd.to_numeric(df['audience_rating'], errors='coerce')

# Streamlit app
st.title("Movie Data Analysis Dashboard")

# Sidebar
st.sidebar.header("Filters")
selected_genre = st.sidebar.multiselect("Select Genre", df['genre'].unique())
selected_rating = st.sidebar.multiselect("Select Rating", df['rating'].unique())

# Filter data
if selected_genre:
    df = df[df['genre'].isin(selected_genre)]
if selected_rating:
    df = df[df['rating'].isin(selected_rating)]

# Main content
st.header("Movie Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Movies", len(df))
col2.metric("Average Tomatometer Rating", f"{df['tomatometer_rating'].mean():.2f}")
col3.metric("Average Audience Rating", f"{df['audience_rating'].mean():.2f}")

# Ratings Distribution
st.subheader("Ratings Distribution")
fig = px.histogram(df, x="tomatometer_rating", nbins=20, title="Tomatometer Rating Distribution")
st.plotly_chart(fig)

fig = px.histogram(df, x="audience_rating", nbins=20, title="Audience Rating Distribution")
st.plotly_chart(fig)

# Genre Analysis
st.subheader("Genre Analysis")
genre_counts = df['genre'].value_counts().head(10)
fig = px.bar(x=genre_counts.index, y=genre_counts.values, labels={'x': 'Genre', 'y': 'Count'}, title="Top 10 Genres")
st.plotly_chart(fig)

# Release Date Analysis
st.subheader("Release Date Analysis")
df['release_year'] = df['in_theaters_date'].dt.year
year_counts = df['release_year'].value_counts().sort_index()
fig = px.line(x=year_counts.index, y=year_counts.values, labels={'x': 'Year', 'y': 'Number of Movies'}, title="Movies Released by Year")
st.plotly_chart(fig)

# Runtime Analysis
st.subheader("Runtime Analysis")
fig = px.box(df, y="runtime_in_minutes", title="Movie Runtime Distribution")
st.plotly_chart(fig)

# Tomatometer vs Audience Rating
st.subheader("Tomatometer vs Audience Rating")
fig = px.scatter(df, x="tomatometer_rating", y="audience_rating", hover_data=['movie_title'], title="Tomatometer vs Audience Rating")
st.plotly_chart(fig)

# Word Cloud of Movie Titles
st.subheader("Word Cloud of Movie Titles")
text = ' '.join(df['movie_title'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)

# Top Directors
st.subheader("Top Directors")
director_counts = df['directors'].value_counts().head(10)
fig = px.bar(x=director_counts.index, y=director_counts.values, labels={'x': 'Director', 'y': 'Number of Movies'}, title="Top 10 Directors")
fig.update_xaxes(tickangle=45)
st.plotly_chart(fig)

# Interactive Movie Explorer
st.subheader("Interactive Movie Explorer")
selected_movie = st.selectbox("Select a movie", df['movie_title'].unique())
movie_data = df[df['movie_title'] == selected_movie].iloc[0]

st.write(f"**Title:** {movie_data['movie_title']}")
st.write(f"**Genre:** {movie_data['genre']}")
st.write(f"**Director(s):** {movie_data['directors']}")
st.write(f"**Rating:** {movie_data['rating']}")
st.write(f"**Tomatometer Rating:** {movie_data['tomatometer_rating']}")
st.write(f"**Audience Rating:** {movie_data['audience_rating']}")
st.write(f"**Runtime:** {movie_data['runtime_in_minutes']} minutes")
st.write(f"**Critics Consensus:** {movie_data['critics_consensus']}")

# Correlation Heatmap
st.subheader("Correlation Heatmap")
numeric_cols = ['runtime_in_minutes', 'tomatometer_rating', 'tomatometer_count', 'audience_rating', 'audience_count']
corr_matrix = df[numeric_cols].corr()
fig = px.imshow(corr_matrix, text_auto=True, aspect="auto", title="Correlation Heatmap")
st.plotly_chart(fig)

# Footer
st.markdown("---")
st.write("Data source: Rotten Tomatoes Movie Dataset")
st.write("Dashboard created with Streamlit and Plotly")