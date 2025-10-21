import streamlit as st
import pandas as pd
import os

# --- Candidate List (with unique names) ---
candidates = [
    "Arun",
    "Karan",
    "Sankar A",
    "Parikshit",
    "Vatsal",
    "Sankar B",
    "Yasub"
]

# --- CSV File for Votes ---
VOTES_FILE = "votes.csv"

# Initialize file if not exists
if not os.path.exists(VOTES_FILE):
    df = pd.DataFrame(columns=["Voter", "Vote1", "Vote2", "Vote3"])
    df.to_csv(VOTES_FILE, index=False)

st.title("🗳️ Open Ballot Voting System")
st.write("Each voter must cast **3 votes** for different candidates.")
st.write("Enter your name or email as identity. You can vote only once.")

# --- Load Existing Votes ---
votes_df = pd.read_csv(VOTES_FILE)
voted_users = votes_df["Voter"].tolist()

identity = st.text_input("Your Name or Email")

if identity:
    if identity in voted_users:
        st.warning("⚠️ You have already voted.")
    else:
        selected = st.multiselect(
            "Select exactly 3 candidates:",
            candidates
        )

        if st.button("Submit Vote"):
            if len(selected) != 3:
                st.error("Please select exactly 3 candidates.")
            else:
                # Record the vote
                new_row = {"Voter": identity, "Vote1": selected[0], "Vote2": selected[1], "Vote3": selected[2]}
                votes_df = pd.concat([votes_df, pd.DataFrame([new_row])], ignore_index=True)
                votes_df.to_csv(VOTES_FILE, index=False)
                st.success("✅ Your votes have been recorded. Thank you!")

# --- Show Results ---
st.subheader("📊 Current Vote Totals")

if not votes_df.empty:
    all_votes = votes_df[["Vote1", "Vote2", "Vote3"]].values.flatten()
    results = pd.Series(all_votes).value_counts().reindex(candidates, fill_value=0)
    st.dataframe(results.rename_axis("Candidate").reset_index(name="Votes"))
else:
    st.info("No votes have been cast yet.")

# --- Admin Section ---
with st.expander("🔍 View Voter Details (Admin Use)"):
    st.dataframe(votes_df)
    st.download_button("⬇️ Download Votes CSV", data=votes_df.to_csv(index=False),
                       file_name="votes.csv", mime="text/csv")
