import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on March 30th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")
# Add a dropdown for selecting Category
st.write("### Select a Category")
categories = df["Category"].unique()
selected_category = st.selectbox("Choose a Category", categories)

# Filter data based on selection
filtered_df = df[df["Category"] == selected_category]

# Add a multi-select for selecting Sub-Category within the chosen Category
st.write("### Select Sub_Categories")
sub_categories = filtered_df["Sub_Category"].unique()
selected_subcategories = st.multiselect("Choose Sub-Categories", sub_categories, default=sub_categories)

# Further filter data based on selected Sub-Categories
filtered_df = filtered_df[filtered_df["Sub_Category"].isin(selected_subcategories)]

st.write(f"### Data for {selected_category} - {', '.join(selected_subcategories)}")
st.dataframe(filtered_df)


# Show a line chart of sales for the selected sub-categories
st.write("### Sales Trend for Selected Sub-Categories")
sales_trend_subcategories = filtered_df.groupby(["Order_Date", "Sub_Category"])["Sales"].sum().unstack()
st.line_chart(sales_trend_subcategories)

# Calculate metrics
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

# Calculate overall average profit margin
overall_profit_margin = (df["Profit"].sum() / df["Sales"].sum()) * 100 if df["Sales"].sum() != 0 else 0
delta_margin = profit_margin - overall_profit_margin

# Display metrics
st.write("### Key Metrics")
st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
st.metric(label="Profit Margin (%)", value=f"{profit_margin:.2f}%", delta=f"{delta_margin:.2f}%")

