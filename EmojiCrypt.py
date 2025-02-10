import streamlit as st
import time
import os
import pandas as pd
import random

# Constants
TIME_LIMIT = 600  # 10 minutes
USERNAME = "EmojiCrypt"
PASSWORD = "Student"

# Initialize session state variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "decoded_message" not in st.session_state:
    st.session_state.decoded_message = ""
if "time_taken" not in st.session_state:
    st.session_state.time_taken = 0
if "user_details" not in st.session_state:
    st.session_state.user_details = ""
if "challenge_data" not in st.session_state:
    st.session_state.challenge_data = None
if "emoji_paragraph" not in st.session_state:
    st.session_state.emoji_paragraph = None
if "correct_answer" not in st.session_state:
    st.session_state.correct_answer = None
if "final_score" not in st.session_state:
    st.session_state.final_score = 0

# Function to generate a new challenge
def generate_new_challenge():
    emoji_dict = {
        "🚀": "Astronauts", "🌕": "explore", "🌠": "the", "🛰️": "mysteries", "🔭": "of", "✨": "the", "🛸": "universe",
        "📖": "Reading", "🧠": "improves", "💡": "our", "✍️": "understanding", "📚": "of", "🔍": "the world",
        "🎶": "Music", "🎹": "brings", "🎤": "joy", "🎻": "and", "🥁": "fills", "🎺": "our", "🎸": "hearts",
        "🌍": "Protecting", "💚": "nature", "♻️": "is", "🌱": "important", "🚯": "for", "🏞️": "the future",
        "🏆": "Success", "💪": "requires", "🎯": "determination", "🏅": "and", "🎖️": "hard", "🚀": "work",
        "🎨": "Creativity", "🖌️": "inspires", "🖼️": "art", "🎭": "and", "🎬": "films", "📷": "capture", "📹": "memories"
    }

    emoji_list = list(emoji_dict.keys())
    random.shuffle(emoji_list)

    selected_emojis = emoji_list[:50]
    emoji_paragraph = " ".join(selected_emojis)
    correct_answer = " ".join([emoji_dict[emoji] for emoji in selected_emojis])

    return emoji_paragraph, correct_answer, emoji_dict

# Generate challenge if it doesn't exist
if st.session_state.challenge_data is None:
    emoji_paragraph, correct_answer, emoji_dict = generate_new_challenge()
    st.session_state.emoji_paragraph = emoji_paragraph
    st.session_state.correct_answer = correct_answer
    st.session_state.challenge_data = emoji_dict

# Login System
if not st.session_state.authenticated:
    st.title("🔐 Emoji Crypt Challenge - Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.authenticated = True
            st.session_state.start_time = time.time()  # Start timer on login
            st.rerun()
        else:
            st.error("❌ Incorrect username or password!")

else:
    # Timer that updates continuously
    elapsed_time = time.time() - st.session_state.start_time
    time_left = max(TIME_LIMIT - elapsed_time, 0)
    milliseconds = int((time_left % 1) * 1000)
    st.sidebar.warning(f"⏳ Time Left: {int(time_left)}.{milliseconds:03d} seconds")

    if time_left <= 0:
        st.error("⏰ Time is up! Please submit your answer.")
        st.session_state.submitted = True

    # Sidebar with emoji-word mapping
    st.sidebar.header("📜 Emoji Word Mapping")
    for emoji, word in st.session_state.challenge_data.items():
        st.sidebar.write(f"{emoji} → {word}")

    # Title
    st.markdown("<h1 style='text-align: center;'>🧩 Emoji Crypt Challenge</h1>", unsafe_allow_html=True)

    # User details input
    st.subheader("📝 Enter Your Details:")
    user_details = st.text_input("Full Name, Roll No, Semester, Department:", key="user_details")

    # Display large emoji paragraph
    st.subheader("🔍 Decrypt This Emoji Paragraph:")
    st.markdown(f"<h2 style='text-align: center; font-size: 24px;'>{st.session_state.emoji_paragraph}</h2>", unsafe_allow_html=True)

    # Writing area for decrypted text
    decoded_text = st.text_area("Write your decrypted sentence here:", key="decoded_text")

    # Submit button
    if st.button("🚀 Submit Answer") and not st.session_state.submitted:
        if not decoded_text.strip():
            st.error("❌ Your answer cannot be empty!")
        elif not user_details.strip():
            st.error("❌ Please enter your full details!")
        else:
            st.session_state.time_taken = round(time.time() - st.session_state.start_time, 3)
            st.session_state.submitted = True

            # New Scoring System
            total_words = len(st.session_state.correct_answer.split())
            user_words = decoded_text.split()

            correct_words = sum(1 for w1, w2 in zip(user_words, st.session_state.correct_answer.split()) if w1 == w2)
            decryption_completion = (len(user_words) / total_words) * 60
            decryption_correctness = (correct_words / total_words) * 80
            correctness = 70 if decoded_text.strip() == st.session_state.correct_answer else 0
            time_score = (60 - (st.session_state.time_taken / TIME_LIMIT) * 60)

            final_score = round((0.7 * correctness) + (0.6 * decryption_completion) + (0.8 * decryption_correctness) + (1.0 * time_score), 2)
            st.session_state.final_score = final_score

            if decoded_text.strip() == st.session_state.correct_answer:
                st.success(f"✅ Correct! Submitted in {st.session_state.time_taken} seconds!")
            else:
                st.error("❌ Incorrect decryption! You will not be added to the leaderboard.")

            # Save to leaderboard
            leaderboard_file = "emoji_leaderboard.csv"
            if os.path.exists(leaderboard_file):
                try:
                    leaderboard_df = pd.read_csv(leaderboard_file)
                    if not all(col in leaderboard_df.columns for col in ["Username", "Time (s)", "Score"]):
                        raise ValueError("Invalid file structure. Resetting leaderboard.")
                except Exception:
                    leaderboard_df = pd.DataFrame(columns=["Username", "Time (s)", "Score"])
            else:
                leaderboard_df = pd.DataFrame(columns=["Username", "Time (s)", "Score"])

            # Append new entry
            new_entry = pd.DataFrame([[user_details, st.session_state.time_taken, final_score]], columns=["Username", "Time (s)", "Score"])
            leaderboard_df = pd.concat([leaderboard_df, new_entry], ignore_index=True)
            leaderboard_df.to_csv(leaderboard_file, index=False)

            st.rerun()

    # Show Leaderboard
    if st.session_state.submitted:
        st.sidebar.header("🏆 Leaderboard")
        if os.path.exists("emoji_leaderboard.csv"):
            st.sidebar.dataframe(pd.read_csv("emoji_leaderboard.csv").sort_values(by="Time (s)", ascending=True), use_container_width=True)
        else:
            st.sidebar.info("Leaderboard will appear after the first correct submission.")
