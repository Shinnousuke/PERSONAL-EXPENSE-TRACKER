import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load from path directly (replace with your actual path if needed)
CSV_PATH = r"C:\Users\Admin\Desktop\internship_projects\sample_expense_data.csv" # If running locally
# CSV_PATH = "/mnt/data/sample_expense_data.csv"  # Use this if running inside an environment like Jupyter or ChatGPT code interpreter

st.set_page_config(page_title="Personal Finance Tracker", layout="wide")
st.title("📊 Personal Finance Tracker")

# Load data
try:
    df = pd.read_csv(CSV_PATH)
    st.success("Loaded dataset from file successfully!")
except FileNotFoundError:
    st.error(f"CSV file not found at path: {CSV_PATH}")
    st.stop()

# Convert Date column
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df.dropna(subset=['Date', 'Amount'], inplace=True)

# Feature Engineering
df['Month'] = df['Date'].dt.to_period('M')
df['Year'] = df['Date'].dt.year

# Sidebar Filters
st.sidebar.header("Filters")
unique_categories = df['Category'].unique()
selected_categories = st.sidebar.multiselect("Select Categories", unique_categories, default=unique_categories)

# Filter by category
df = df[df['Category'].isin(selected_categories)]

# Display Summary
st.subheader("Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Spend", f"₹{df['Amount'].sum():,.2f}")
col2.metric("Average per Transaction", f"₹{df['Amount'].mean():,.2f}")
col3.metric("Transactions", f"{len(df)}")

# Monthly Expense Trend
st.subheader("📈 Monthly Expense Trend")
monthly_trend = df.groupby('Month')['Amount'].sum().reset_index()
monthly_trend['Month'] = monthly_trend['Month'].astype(str)

fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=monthly_trend, x='Month', y='Amount', marker='o', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Category-wise Expense
st.subheader("🧾 Category-wise Expense Breakdown")
category_totals = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)

fig2, ax2 = plt.subplots(figsize=(8, 4))
category_totals.plot(kind='bar', ax=ax2)
plt.ylabel("Amount (₹)")
plt.xticks(rotation=45)
st.pyplot(fig2)

# Pie chart
st.subheader("📌 Pie Chart of Expenses by Category")
fig3, ax3 = plt.subplots()
category_totals.plot(kind='pie', autopct='%1.1f%%', ax=ax3)
ax3.set_ylabel("")
st.pyplot(fig3)

# Display Data
st.subheader("🧾 Full Data Table")
st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)
