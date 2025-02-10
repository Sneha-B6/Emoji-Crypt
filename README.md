# Emoji-Crypt
# Emoji Crypt Challenge

## Overview
The **Emoji Crypt Challenge** is a fun and interactive Streamlit-based game where participants decrypt an emoji-based paragraph within a **10-minute time limit**. Players must log in, decipher the emoji meanings using the provided mappings, and submit their decrypted text. The system evaluates the accuracy of the decryption and updates the leaderboard accordingly.

## Features
- **Secure Login**: Access restricted to authorized users (Username: `EmojiCrypt`, Password: `Student`).
- **Randomized Challenges**: Each session presents a new emoji paragraph to decrypt.
- **Time-Limited Game**: Players have **600 seconds** (10 minutes) to submit their response.
- **Emoji Word Mapping**: Sidebar displays emoji-to-word translations for guidance.
- **Scoring System**:
  - Completion percentage and correctness impact final score.
  - Bonus points for accurate and timely submissions.
- **Leaderboard**: Stores and ranks successful players based on time and score.

## Installation & Setup
### Prerequisites
Ensure you have **Python 3** and **Streamlit** installed.

```bash
pip install streamlit pandas
```

### Running the App
Clone or download the script and navigate to the project folder. Then, run:

```bash
streamlit run app.py
```

## How to Play
1. **Login** with the credentials:
   - **Username**: EmojiCrypt
   - **Password**: Student
2. **Read the Emoji Paragraph** displayed on the screen.
3. **Use the Sidebar Mapping** to decrypt the paragraph.
4. **Enter Your Details** (Name, Roll No, Semester, Department).
5. **Write the Deciphered Text** in the input box.
6. **Submit** before the timer runs out!
7. **Check the Leaderboard** for scores and rankings.

## Scoring System
- **Correctness (70%)**: Full points if the decryption matches exactly.
- **Completion (60%)**: Partial points if some words are correct.
- **Time Bonus (Variable)**: Faster submissions score higher.
- **Final Score Formula**:
  ```
  final_score = (0.7 * correctness) + (0.6 * completion) + (0.8 * accuracy) + (1.0 * time_score)
  ```

## Files & Data Storage
- **emoji_leaderboard.csv**: Stores player scores and times.
- **app.py**: Main Streamlit application script.

## Notes
- The challenge resets upon restart.
- Incorrect submissions will not be added to the leaderboard.

## License
This project is for educational and fun use. Feel free to modify and enhance it!


