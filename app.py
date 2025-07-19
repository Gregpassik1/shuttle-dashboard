from pathlib import Path

# Updated full version of app.py that includes optimizer and visualization
updated_app_code = """
import streamlit as st
import pandas as pd
import plotly.express as px
from shuttle_optimizer import optimize_schedule

st.set_page_config(layout="wide")
st.title("🚌 Shuttle Volume Dashboard + Optimizer")

uploaded_file = st.file_uploader("Upload shuttle Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df["date"] = pd.to_datetime(df["date"])
    df["day_of_week"] = df["date"].dt.day_name()

    st.subheader("📊 Raw Passenger Volume (Grouped by Pickup & Time Block)")
    grouped = df.groupby(["pickup_location", "time_block"])["passenger_count"].sum().reset_index()
    pivot = grouped.pivot(index="pickup_location", columns="time_block", values="passenger_count").fillna(0)
    st.dataframe(pivot)

    st.subheader("📈 Passenger Volume by Day of Week and Time Block")
    heatmap_data = df.groupby(["day_of_week", "time_block"])["passenger_count"].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot(index="day_of_week", columns="time_block", values="passenger_count").fillna(0)
    st.dataframe(heatmap_pivot)

    fig = px.imshow(
        heatmap_pivot,
        labels=dict(x="Time Block", y="Day of Week", color="Passengers"),
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        aspect="auto",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("⚙️ Select Day to Optimize Shuttle Schedule")
    selected_day = st.selectbox("Day of Week", sorted(df["day_of_week"].unique()))

    day_df = df[df["day_of_week"] == selected_day]
    ordered_blocks = sorted(day_df["time_block"].unique())
    demand_series = (
        day_df.groupby("time_block")["passenger_count"]
        .sum()
        .reindex(ordered_blocks, fill_value=0)
        .tolist()
    )

    if demand_series:
        optimized_schedule = optimize_schedule(demand_series)

        st.subheader("✅ Optimized Shuttle Schedule")
        schedule_df = pd.DataFrame(optimized_schedule, columns=["Time", "Shuttles Required"])
        st.dataframe(schedule_df)

        fig_sched = px.bar(schedule_df, x="Time", y="Shuttles Required", title="Optimized Shuttle Dispatch")
        st.plotly_chart(fig_sched, use_container_width=True)
    else:
        st.info("No data available for selected day.")
else:
    st.warning("Please upload a .xlsx file to get started.")
"""

# Save updated app.py
app_file_path = "/mnt/data/app.py"
Path(app_file_path).write_text(updated_app_code)

app_file_path

