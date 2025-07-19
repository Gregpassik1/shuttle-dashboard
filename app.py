import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Shuttle Volume Dashboard")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    df["time_block"] = pd.Categorical(df["time_block"], ordered=True, categories=sorted(df["time_block"].unique()))
    df["day_of_week"] = pd.to_datetime(df["date"]).dt.day_name()

    st.subheader("📊 Heatmap: Passenger Volume by Day and Time")
    heatmap_data = df.groupby(["day_of_week", "time_block"])["passenger_count"].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot(index="day_of_week", columns="time_block", values="passenger_count")
    st.dataframe(heatmap_pivot.fillna(0))

    st.subheader("📈 Line Chart: Volume by Hotel and Time Block")
    line_data = df.groupby(["pickup_location", "time_block"])["passenger_count"].sum().reset_index()
    fig = px.line(line_data, x="time_block", y="passenger_count", color="pickup_location", markers=True)
    st.plotly_chart(fig)

    st.subheader("📉 Total Weekly Volume by Hotel")
    bar_data = df.groupby("pickup_location")["passenger_count"].sum().reset_index()
    fig2 = px.bar(bar_data, x="pickup_location", y="passenger_count", color="pickup_location")
    st.plotly_chart(fig2)

    st.subheader("📦 Box Plot: Variability by Time Block")
    fig3 = px.box(df, x="time_block", y="passenger_count", points="all")
    st.plotly_chart(fig3)
