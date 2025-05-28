# app.py
import streamlit as st
from datetime import date
import pandas as pd
import os
from habit_logger import log_habit
from system_scanner import scan_directory, save_to_csv
from dashboard import (
    load_logs, plot_mood_trend, plot_time_allocation,
    plot_correlation, plot_bubble, plot_time_stacked
)

st.set_page_config(page_title="Digital Habit Tracker", layout="centered")

st.title("🧠 Digital Habit Tracker")

menu = st.sidebar.selectbox("Navigate", ["Daily Habit Logger", "System File Scanner", "Dashboard"])

if menu == "Daily Habit Logger":
    st.subheader("📘 Daily Habit Logger")
    mood = st.slider("Mood (1-10)", 1, 10, 5)
    study = st.number_input("Hours of Study", min_value=0, max_value=24, value=1)
    sleep = st.number_input("Hours of Sleep", min_value=0, max_value=24, value=8)
    fun = st.number_input("Hours of Entertainment", min_value=0, max_value=24, value=2)
    topic = st.text_input("Topics Studied")

    if st.button("Log Today's Habit"):
        today = date.today()
        csv_path = "data/daily_logs.csv"
        with open(csv_path, "a", newline="") as file:
            import csv
            writer = csv.writer(file)
            writer.writerow([today, mood, study, sleep, fun, topic])

        try:
            log_habit()  # Save to DB
            st.success("Habit logged successfully!")
        except Exception as e:
            st.error(f"Error logging habit: {e}")

elif menu == "System File Scanner":
    st.subheader("🗂️ System File Scanner")
    folder = st.text_input("Enter folder path to scan")
    if st.button("Scan Folder"):
        if os.path.isdir(folder):
            try:
                df = scan_directory(folder)
                st.success(f"Scanned {len(df)} files")
                st.dataframe(df.head())
                save_to_csv(df)
            except Exception as e:
                st.error(f"Error scanning directory: {e}")
        else:
            st.warning("Invalid folder path")

elif menu == "Dashboard":
    st.subheader("📊 Dashboard Visualizations")
    try:
        df = load_logs()
        df = df.sort_values("date")

        # Filter
        min_date = df["date"].min().date()
        max_date = df["date"].max().date()
        start_date, end_date = st.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

        filtered_df = df[(df["date"] >= pd.to_datetime(start_date)) & (df["date"] <= pd.to_datetime(end_date))]

        st.markdown("### Mood Over Time")
        st.pyplot(plot_mood_trend(filtered_df))

        st.markdown("### Average Time Allocation")
        st.pyplot(plot_time_allocation(filtered_df))

        st.markdown("### Mood vs Activities Correlation")
        st.pyplot(plot_correlation(filtered_df))

        st.markdown("### Study vs Mood Bubble Chart")
        st.pyplot(plot_bubble(filtered_df))

        st.markdown("### Daily Time Stacked Bar")
        st.pyplot(plot_time_stacked(filtered_df))

    except Exception as e:
        st.error(f"Error loading dashboard: {e}")
