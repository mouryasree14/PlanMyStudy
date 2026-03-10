import streamlit as st
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import time
import random

st.set_page_config(page_title="PlanMyStudy", layout="wide")

# Sidebar Navigation
page = st.sidebar.selectbox(
    "Navigation",
    ["Study Planner", "Progress Tracker", "Analytics", "Pomodoro Timer"]
)

# Motivation quotes
quotes = [
    "Success is the sum of small efforts repeated daily.",
    "Push yourself, because no one else will do it for you.",
    "Study now, shine later.",
    "Consistency beats intensity.",
    "Dream big and work hard."
]

# ---------------- STUDY PLANNER ---------------- #

if page == "Study Planner":

    st.title("📚 PlanMyStudy - Smart Study Planner")
    st.info(random.choice(quotes))

    subjects = st.text_input("Enter subjects (comma separated)")
    exam_date = st.date_input("Select exam date")
    hours_per_day = st.number_input("Study hours per day", 1, 12)

    if st.button("Generate Study Plan"):

        if subjects == "":
            st.warning("Please enter subjects")

        else:
            subject_list = [s.strip() for s in subjects.split(",")]

            today = date.today()
            days_left = (exam_date - today).days

            if days_left <= 0:
                st.error("Exam date must be in the future")

            else:
                hours_per_subject = hours_per_day / len(subject_list)

                data = []

                for i in range(days_left):
                    for subject in subject_list:
                        data.append({
                            "Day": f"Day {i+1}",
                            "Subject": subject,
                            "Hours": round(hours_per_subject, 2)
                        })

                df = pd.DataFrame(data)

                st.success(f"You have {days_left} days to prepare!")

                st.dataframe(df)

                # Save dataframe to session
                st.session_state["plan"] = df

                # Download button
                csv = df.to_csv(index=False)

                st.download_button(
                    "Download Study Plan",
                    csv,
                    "study_plan.csv",
                    "text/csv"
                )

# ---------------- PROGRESS TRACKER ---------------- #

elif page == "Progress Tracker":

    st.title("✅ Study Progress Tracker")

    if "plan" not in st.session_state:
        st.warning("Generate a study plan first.")
    else:
        df = st.session_state["plan"]

        completed = 0
        total = len(df)

        for i in range(len(df)):
            if st.checkbox(f"{df.iloc[i]['Day']} - {df.iloc[i]['Subject']} ({df.iloc[i]['Hours']} hrs)"):
                completed += 1

        progress = completed / total

        st.progress(progress)

        st.write(f"Completed: {completed} / {total} tasks")

# ---------------- ANALYTICS ---------------- #

elif page == "Analytics":

    st.title("📊 Study Analytics")

    if "plan" not in st.session_state:
        st.warning("Generate a study plan first.")
    else:
        df = st.session_state["plan"]

        subject_hours = df.groupby("Subject")["Hours"].sum()

        fig, ax = plt.subplots()

        ax.bar(subject_hours.index, subject_hours.values)

        ax.set_title("Total Study Hours per Subject")
        ax.set_ylabel("Hours")

        st.pyplot(fig)

# ---------------- POMODORO TIMER ---------------- #

elif page == "Pomodoro Timer":

    st.title("⏱ Pomodoro Study Timer")

    st.write("Focus for **25 minutes**, then take a **5 minute break**.")

    if st.button("Start Study Session"):

        with st.spinner("Study session started... Stay focused!"):
            time.sleep(5)

        st.success("Great job! Time for a break 🎉")

    if st.button("Start Break"):
        with st.spinner("Break time... Relax!"):
            time.sleep(3)

        st.success("Break finished! Back to study 💪")