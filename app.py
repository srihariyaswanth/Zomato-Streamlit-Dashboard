import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Zomato Restaurant Insights", layout="wide")

# Load and clean data
df = pd.read_csv("Zomato-data-.csv")
df.columns = ['name', 'online_order', 'book_table', 'rate', 'votes', 'approx_cost(for two people)', 'listed_in(type)']

df['rate'] = df['rate'].astype(str).str.replace("/5", "", regex=False)
df['rate'] = pd.to_numeric(df['rate'], errors='coerce')
df['online_order'] = df['online_order'].str.strip().str.lower()
df['book_table'] = df['book_table'].str.strip().str.lower()
df['listed_in(type)'] = df['listed_in(type)'].str.strip()
df = df.dropna(subset=['rate', 'approx_cost(for two people)'])

# Sidebar filters
st.sidebar.title("Filter Restaurants")
selected_type = st.sidebar.selectbox("Select Restaurant Type", sorted(df['listed_in(type)'].dropna().unique()))
min_rating, max_rating = st.sidebar.slider("Select Rating Range", 0.0, 5.0, (3.0, 5.0), 0.1)
order_pref = st.sidebar.radio("Online Order Available?", ['all', 'yes', 'no'])

# Apply filters
filtered = df[df['listed_in(type)'] == selected_type]
filtered = filtered[(filtered['rate'] >= min_rating) & (filtered['rate'] <= max_rating)]
if order_pref != 'all':
    filtered = filtered[filtered['online_order'] == order_pref]

# Dashboard title
st.title("Zomato Restaurants Data Explorer")
st.markdown(f"Showing **{len(filtered)}** restaurants of type '**{selected_type}**' with rating between **{min_rating} - {max_rating}**.")

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Average Rating", f"{filtered['rate'].mean():.2f}")
col2.metric("Average Cost for Two", f"₹{filtered['approx_cost(for two people)'].mean():.0f}")
col3.metric("Total Votes", f"{filtered['votes'].sum():,}")

# Top 5 restaurants
st.subheader("Top 5 Restaurants (by Rating & Votes)")
top5 = filtered[filtered['votes'] > 50].sort_values(by=['rate', 'votes'], ascending=[False, False]).head(5)
st.dataframe(top5[['name', 'rate', 'votes', 'approx_cost(for two people)']].reset_index(drop=True))

# Plot 1: Rating Distribution
st.subheader("Rating Distribution")
fig1, ax1 = plt.subplots()
sns.histplot(filtered['rate'], bins=10, kde=True, ax=ax1, color='skyblue')
st.pyplot(fig1)

# Plot 2: Votes vs Rating
st.subheader("Votes vs Rating")
fig2, ax2 = plt.subplots()
sns.scatterplot(data=filtered, x='votes', y='rate', ax=ax2, hue='rate', palette='viridis', alpha=0.7)
st.pyplot(fig2)

# Plot 3: Cost vs Rating
st.subheader("Cost vs Rating")
fig3, ax3 = plt.subplots()
sns.scatterplot(data=filtered, x='approx_cost(for two people)', y='rate', ax=ax3, hue='rate', palette='coolwarm', alpha=0.7)
st.pyplot(fig3)
