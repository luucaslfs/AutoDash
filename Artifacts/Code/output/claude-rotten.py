import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data.csv')
    return df
df = load_data()
# Title
st.title('Movie Analysis Dashboard')
# Sidebar
st.sidebar.header('Filters')
selected_genre = st.sidebar.multiselect('Select Genre', df['genre'].unique())
min_rating = st.sidebar.slider('Minimum Tomatometer Rating', 0, 100, 0)
# Filter data
if selected_genre:
    df_filtered = df[df['genre'].isin(selected_genre)]
else:
    df_filtered = df
df_filtered = df_filtered[df_filtered['tomatometer_rating'].astype(float) >= min_rating]
# Main content
st.header('Movie Overview')
# Genre distribution
genre_counts = df_filtered['genre'].value_counts()
fig_genre = px.pie(values=genre_counts.values, names=genre_counts.index, title='Genre Distribution')
st.plotly_chart(fig_genre)
# Rating distribution
fig_rating = px.histogram(df_filtered, x='tomatometer_rating', title='Tomatometer Rating Distribution')
st.plotly_chart(fig_rating)
# Audience vs Critic ratings
fig_audience_critic = px.scatter(df_filtered, x='tomatometer_rating', y='audience_rating', 
                                 hover_data=['movie_title'], title='Audience vs Critic Ratings')
st.plotly_chart(fig_audience_critic)
# Top rated movies
st.subheader('Top Rated Movies')
top_movies = df_filtered.sort_values('tomatometer_rating', ascending=False).head(10)
st.table(top_movies[['movie_title', 'tomatometer_rating', 'audience_rating']])
# Runtime analysis
st.subheader('Runtime Analysis')
df_filtered['runtime_in_minutes'] = pd.to_numeric(df_filtered['runtime_in_minutes'], errors='coerce')
fig_runtime = px.box(df_filtered, x='genre', y='runtime_in_minutes', title='Movie Runtime by Genre')
st.plotly_chart(fig_runtime)
# Correlation heatmap
st.subheader('Correlation Heatmap')
numeric_cols = ['tomatometer_rating', 'tomatometer_count', 'audience_rating', 'audience_count']
corr_matrix = df_filtered[numeric_cols].corr()
fig_corr = go.Figure(data=go.Heatmap(z=corr_matrix.values, x=corr_matrix.index, y=corr_matrix.columns))
fig_corr.update_layout(title='Correlation Heatmap')
st.plotly_chart(fig_corr)
# Movie release timeline
st.subheader('Movie Release Timeline')
df_filtered['in_theaters_date'] = pd.to_datetime(df_filtered['in_theaters_date'], errors='coerce')
fig_timeline = px.scatter(df_filtered, x='in_theaters_date', y='tomatometer_rating', 
                          hover_data=['movie_title'], title='Movie Release Timeline')
st.plotly_chart(fig_timeline)
# Word cloud of movie titles
st.subheader('Movie Title Word Cloud')
from wordcloud import WordCloud
import matplotlib.pyplot as plt
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(df_filtered['movie_title']))
fig_wordcloud, ax = plt.subplots()
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig_wordcloud)
# Interactive movie search
st.subheader('Movie Search')
search_term = st.text_input('Enter a movie title')
if search_term:
    results = df[df['movie_title'].str.contains(search_term, case=False)]
    if not results.empty:
        st.table(results[['movie_title', 'genre', 'tomatometer_rating', 'audience_rating']])
    else:
        st.write('No results found.')