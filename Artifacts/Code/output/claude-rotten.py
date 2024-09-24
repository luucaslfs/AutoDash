import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Movie Dashboard", layout="wide")

# Carregar os dados
@st.cache_data
def load_data():
    df = pd.read_csv('data.csv')
    df['in_theaters_date'] = pd.to_datetime(df['in_theaters_date'], errors='coerce')
    df['on_streaming_date'] = pd.to_datetime(df['on_streaming_date'], errors='coerce')
    df['runtime_in_minutes'] = pd.to_numeric(df['runtime_in_minutes'], errors='coerce')
    df['tomatometer_rating'] = pd.to_numeric(df['tomatometer_rating'], errors='coerce')
    df['audience_rating'] = pd.to_numeric(df['audience_rating'], errors='coerce')
    return df

df = load_data()

# Título
st.title('Movie Dashboard')

# Sidebar
st.sidebar.header('Filters')
selected_genre = st.sidebar.multiselect('Select Genre', df['genre'].unique())
selected_rating = st.sidebar.multiselect('Select Rating', df['rating'].unique())

# Aplicar filtros
if selected_genre:
    df = df[df['genre'].isin(selected_genre)]
if selected_rating:
    df = df[df['rating'].isin(selected_rating)]

# Layout principal
col1, col2 = st.columns(2)

# Gráfico de dispersão: Tomatometer Rating vs Audience Rating
with col1:
    st.subheader('Tomatometer Rating vs Audience Rating')
    fig = px.scatter(df, x='tomatometer_rating', y='audience_rating', hover_name='movie_title',
                     color='tomatometer_status', size='tomatometer_count')
    st.plotly_chart(fig, use_container_width=True)

# Histograma: Runtime Distribution
with col2:
    st.subheader('Runtime Distribution')
    fig = px.histogram(df, x='runtime_in_minutes', nbins=30)
    st.plotly_chart(fig, use_container_width=True)

# Top 10 Directors
top_directors = df['directors'].value_counts().head(10)
fig = px.bar(top_directors, x=top_directors.index, y=top_directors.values, title='Top 10 Directors')
st.plotly_chart(fig, use_container_width=True)

# Genre Distribution
genre_counts = df['genre'].value_counts()
fig = px.pie(genre_counts, values=genre_counts.values, names=genre_counts.index, title='Genre Distribution')
st.plotly_chart(fig, use_container_width=True)

# Tomatometer Status Distribution
tomatometer_status_counts = df['tomatometer_status'].value_counts()
fig = px.pie(tomatometer_status_counts, values=tomatometer_status_counts.values, names=tomatometer_status_counts.index, title='Tomatometer Status Distribution')
st.plotly_chart(fig, use_container_width=True)

# Movies over time
df['year'] = df['in_theaters_date'].dt.year
movies_per_year = df.groupby('year').size().reset_index(name='count')
fig = px.line(movies_per_year, x='year', y='count', title='Number of Movies Released per Year')
st.plotly_chart(fig, use_container_width=True)

# Word Cloud of Movie Titles
def plot_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

st.subheader('Word Cloud of Movie Titles')
all_titles = ' '.join(df['movie_title'])
plot_wordcloud(all_titles)

# Estatísticas interativas
st.subheader('Interactive Statistics')
column = st.selectbox('Select a column for statistics', ['tomatometer_rating', 'audience_rating', 'runtime_in_minutes'])
st.write(df[column].describe())

# Top Movies
st.subheader('Top Movies')
sort_by = st.selectbox('Sort by', ['tomatometer_rating', 'audience_rating', 'tomatometer_count', 'audience_count'])
top_n = st.slider('Number of top movies to show', 5, 50, 10)

top_movies = df.sort_values(sort_by, ascending=False).head(top_n)
st.table(top_movies[['movie_title', sort_by]])

# Footer
st.markdown('---')
st.write('Data source: Rotten Tomatoes')