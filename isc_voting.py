import streamlit as st

# Candidates
candidates = [
    "Alice Johnson",
    "Bob Smith",
    "Catherine Lee",
    "David Kim",
    "Evelyn Brown",
    "Franklin White",
    "Grace Adams"
]

# Initialize votes
if "votes" not in st.session_state:
    st.session_state.votes = {c: 0 for c in candidates}
if "voters" not in st.session_state:
    st.session_state.voters = set()

st.title("🗳️ Open Ballot Voting System")
st.write("Each voter must cast **3 votes** for different candidates.")
st.write("Enter your name or email as identity. You can vote only once.")

# Get voter identity
identity = st.text_input("Your Name or Email")

if identity:
    if identity in st.session_state.voters:
        st.warning("⚠️ You have already voted.")
    else:
        selected = st.multiselect(
            "Select exactly 3 candidates:",
            candidates,
        )

        if st.button("Submit Vote"):
            if len(selected) != 3:
                st.error("Please select exactly 3 candidates.")
            else:
                for s in selected:
                    st.session_state.votes[s] += 1
                st.session_state.voters.add(identity)
                st.success("✅ Your votes have been recorded. Thank you!")

# Show current results (open ballot)
st.subheader("📊 Current Results")
for c, v in st.session_state.votes.items():
    st.write(f"**{c}:** {v} votes")

# Display winner
if st.button("Show Winner"):
    winner = max(st.session_state.votes, key=st.session_state.votes.get)
    st.success(f"🏆 Current leader: {winner}")
