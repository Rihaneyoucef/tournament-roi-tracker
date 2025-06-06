import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page title
st.title("🎾 Tournament Cost & ROI Tracker")
st.write("Track your tournament expenses, match results, and calculate your ROI.")

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "Tournament", "Date", "Location", "Category",
        "Entry Fee", "Flights", "Hotel", "Meals", "Coaching", "Miscellaneous",
        "Match Wins", "Match Losses", "Ranking Points"
    ])

# Form for data input
with st.form("Tournament Entry"):
    st.subheader("Add Tournament Data")
    tournament = st.text_input("Tournament Name")
    date = st.date_input("Date")
    location = st.text_input("Location")
    category = st.selectbox("Category", ["J30", "J60", "J100", "ITF", "National", "Other"])
    
    entry_fee = st.number_input("Entry Fee (€)", min_value=0.0)
    flights = st.number_input("Flight Cost (€)", min_value=0.0)
    hotel = st.number_input("Hotel Cost (€)", min_value=0.0)
    meals = st.number_input("Meal Cost (€)", min_value=0.0)
    coaching = st.number_input("Coaching Fee (€)", min_value=0.0)
    misc = st.number_input("Miscellaneous (€)", min_value=0.0)

    match_wins = st.number_input("Match Wins", min_value=0)
    match_losses = st.number_input("Match Losses", min_value=0)
    ranking_points = st.number_input("Ranking Points Gained", min_value=0)

    submitted = st.form_submit_button("Add Tournament")
    if submitted:
        new_row = pd.DataFrame.from_dict({
            "Tournament": [tournament], "Date": [date], "Location": [location], "Category": [category],
            "Entry Fee": [entry_fee], "Flights": [flights], "Hotel": [hotel], "Meals": [meals],
            "Coaching": [coaching], "Miscellaneous": [misc],
            "Match Wins": [match_wins], "Match Losses": [match_losses], "Ranking Points": [ranking_points]
        })
        st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
        st.success("Tournament data added!")

# Display data
if not st.session_state.data.empty:
    st.subheader("📊 Tournament Summary")
    st.dataframe(st.session_state.data)

    # Cost calculations
    st.session_state.data["Total Cost"] = st.session_state.data[[
        "Entry Fee", "Flights", "Hotel", "Meals", "Coaching", "Miscellaneous"
    ]].sum(axis=1)

    st.session_state.data["Cost per Point"] = st.session_state.data.apply(
        lambda row: row["Total Cost"] / row["Ranking Points"] if row["Ranking Points"] > 0 else 0, axis=1
    )

    st.session_state.data["Cost per Win"] = st.session_state.data.apply(
        lambda row: row["Total Cost"] / row["Match Wins"] if row["Match Wins"] > 0 else 0, axis=1
    )

    st.subheader("💰 ROI Analysis")
    st.write("### Total Spent per Tournament")
    fig1, ax1 = plt.subplots()
    ax1.bar(st.session_state.data["Tournament"], st.session_state.data["Total Cost"])
    ax1.set_ylabel("€")
    ax1.set_xticklabels(st.session_state.data["Tournament"], rotation=45, ha='right')
    st.pyplot(fig1)

    st.write("### Cost per Ranking Point")
    fig2, ax2 = plt.subplots()
    ax2.bar(st.session_state.data["Tournament"], st.session_state.data["Cost per Point"])
    ax2.set_ylabel("€/Point")
    ax2.set_xticklabels(st.session_state.data["Tournament"], rotation=45, ha='right')
    st.pyplot(fig2)

    st.write("### Cost per Match Win")
    fig3, ax3 = plt.subplots()
    ax3.bar(st.session_state.data["Tournament"], st.session_state.data["Cost per Win"])
    ax3.set_ylabel("€/Win")
    ax3.set_xticklabels(st.session_state.data["Tournament"], rotation=45, ha='right')
    st.pyplot(fig3)

    # Totals summary
    st.subheader("📈 Cumulative Stats")
    total_cost = st.session_state.data["Total Cost"].sum()
    total_points = st.session_state.data["Ranking Points"].sum()
    total_wins = st.session_state.data["Match Wins"].sum()

    st.metric("Total Spent", f"€{total_cost:.2f}")
    st.metric("Total Ranking Points", total_points)
    st.metric("Total Match Wins", total_wins)
    st.metric("Avg. Cost per Point", f"€{(total_cost / total_points):.2f}" if total_points > 0 else "-")
    st.metric("Avg. Cost per Win", f"€{(total_cost / total_wins):.2f}" if total_wins > 0 else "-")
else:
    st.info("No tournament data yet. Use the form above to add your first tournament.")
