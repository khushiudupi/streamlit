import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on April 28th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
df.columns = df.columns.str.strip()  # Clean column names if needed
st.dataframe(df)

st.bar_chart(df, x="Category", y="Sales")

st.dataframe(df.groupby("Category").sum())
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)

sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)
st.line_chart(sales_by_month["Sales"])

# ========== MY ADDITIONS ==========

st.write("## My Additions")

st.write("### Please select a Category from the dropdown below:")
selected_category = st.selectbox("Select a Category", df["Category"].unique())
st.write(f"You selected the Category: **{selected_category}**")

filtered_df = df[df["Category"] == selected_category]

st.write("### Please select one or more Sub-Categories within the chosen Category:")
selected_subcategories = st.multiselect("Select Sub-Category(ies)", filtered_df["Sub_Category"].unique())

final_filtered_df = filtered_df[filtered_df["Sub_Category"].isin(selected_subcategories)]

st.write("### Line Chart: Total Sales for Selected Sub-Categories Over Time")
sales_selected = final_filtered_df.groupby(pd.Grouper(freq='M'))["Sales"].sum()
st.line_chart(sales_selected)

st.write("### Key Metrics for the Selected Items")
total_sales = final_filtered_df["Sales"].sum()
total_profit = final_filtered_df["Profit"].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

overall_profit_margin = (df["Profit"].sum() / df["Sales"].sum()) * 100 if df["Sales"].sum() != 0 else 0
delta_margin = profit_margin - overall_profit_margin

col1, col2, col3 = st.columns(3)
col1.metric(label="Total Sales", value=f"${total_sales:,.2f}")
col2.metric(label="Total Profit", value=f"${total_profit:,.2f}")
col3.metric(label="Profit Margin (%)", value=f"{profit_margin:.2f}%", delta=f"{delta_margin:.2f}%")
