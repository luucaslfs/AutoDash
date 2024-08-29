# Generated dashboard code will be inserted here
import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv("Data/Marketing+Data/marketing_data.csv")
    df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'])
    df['Age'] = 2023 - df['Year_Birth']
    return df

df = load_data()

# Set up the dashboard
st.title('Marketing Campaign Dashboard')

# Sidebar filters
st.sidebar.header('Filters')
country_filter = st.sidebar.multiselect('Select Countries', df['Country'].unique(), default=df['Country'].unique())
education_filter = st.sidebar.multiselect('Select Education Levels', df['Education'].unique(), default=df['Education'].unique())

# Apply filters
filtered_df = df[(df['Country'].isin(country_filter)) & (df['Education'].isin(education_filter))]

# Basic statistics
st.header('Basic Statistics')
col1, col2, col3 = st.columns(3)
col1.metric('Total Customers', len(filtered_df))
col2.metric('Average Age', round(filtered_df['Age'].mean(), 1))
col3.metric('Average Income', f"${filtered_df['Income'].mean():,.0f}")

# Visualizations
st.header('Visualizations')

# Visualization 1: Income Distribution by Education
fig1 = px.box(filtered_df, x='Education', y='Income', color='Education',
              title='Income Distribution by Education Level')
st.plotly_chart(fig1)

# Visualization 2: Customer Recency vs Total Amount Spent
filtered_df['TotalAmount'] = filtered_df['MntWines'] + filtered_df['MntFruits'] + \
                             filtered_df['MntMeatProducts'] + filtered_df['MntFishProducts'] + \
                             filtered_df['MntSweetProducts'] + filtered_df['MntGoldProds']

chart = alt.Chart(filtered_df).mark_circle().encode(
    x='Recency',
    y='TotalAmount',
    color='Education',
    tooltip=['ID', 'Age', 'Income', 'Education', 'Recency', 'TotalAmount']
).properties(
    width=700,
    height=400,
    title='Customer Recency vs Total Amount Spent'
)
st.altair_chart(chart)

# Customer Segmentation
st.header('Customer Segmentation')
segment_by = st.selectbox('Segment by', ['Education', 'Marital_Status', 'Country'])

segment_data = filtered_df.groupby(segment_by).agg({
    'ID': 'count',
    'Income': 'mean',
    'TotalAmount': 'mean'
}).reset_index()

segment_data.columns = [segment_by, 'Customer Count', 'Avg Income', 'Avg Total Spent']
segment_data['Avg Income'] = segment_data['Avg Income'].round(2)
segment_data['Avg Total Spent'] = segment_data['Avg Total Spent'].round(2)

st.dataframe(segment_data)

# Campaign Performance
st.header('Campaign Performance')
campaign_data = filtered_df[['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5']].sum()
campaign_data = pd.DataFrame({'Campaign': campaign_data.index, 'Acceptances': campaign_data.values})

fig3 = px.bar(campaign_data, x='Campaign', y='Acceptances',
              title='Campaign Acceptance Rates')
st.plotly_chart(fig3)

# Correlation Heatmap
st.header('Feature Correlation')
numeric_cols = ['Income', 'Age', 'Kidhome', 'Teenhome', 'Recency', 'MntWines', 'MntFruits',
                'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds',
                'NumDealsPurchases', 'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases']

corr_matrix = filtered_df[numeric_cols].corr()

fig4 = px.imshow(corr_matrix, zmin=-1, zmax=1, color_continuous_scale='RdBu_r',
                 title='Correlation Heatmap of Numeric Features')
st.plotly_chart(fig4)

# Footer
st.markdown('---')
st.markdown('Dashboard created with Streamlit by Your Name')

if __name__ == "__main__":
    st.sidebar.info("This dashboard is generated using AI.")
    