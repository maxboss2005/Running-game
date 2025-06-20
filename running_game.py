import streamlit as st
import time
import random

# Set config
st.set_page_config(page_title="🏃 Streamlit Runner", layout="centered")

# Setup game state
if "player_y" not in st.session_state:
    st.session_state.player_y = 1  # 0 = jumping, 1 = ground
    st.session_state.obstacle_x = 9
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.jump_timer = 0

st.title("🏃 Streamlit Runner Game")

def draw_game():
    grid = [["⬜"] * 10 for _ in range(2)]
    if not st.session_state.game_over:
        grid[st.session_state.player_y][1] = "🧍‍♂️"
        grid[1][st.session_state.obstacle_x] = "🚧"
    else:
        grid[st.session_state.player_y][1] = "💀"
        grid[1][st.session_state.obstacle_x] = "🚧"

    for row in grid:
        st.write("".join(row))

# Draw current game state
draw_game()

# Game controls
col1, col2 = st.columns([1, 3])
with col1:
    if st.button("⬆️ Jump") and not st.session_state.game_over:
        st.session_state.player_y = 0
        st.session_state.jump_timer = 2

with col2:
    if st.button("🔄 Restart"):
        st.session_state.player_y = 1
        st.session_state.obstacle_x = 9
        st.session_state.score = 0
        st.session_state.jump_timer = 0
        st.session_state.game_over = False
        st.experimental_rerun()

# Game loop (triggered on refresh)
if not st.session_state.game_over:
    time.sleep(0.3)

    # Handle jump
    if st.session_state.jump_timer > 0:
        st.session_state.jump_timer -= 1
    else:
        st.session_state.player_y = 1

    # Move obstacle
    st.session_state.obstacle_x -= 1
    if st.session_state.obstacle_x < 0:
        st.session_state.obstacle_x = 9 if random.random() > 0.3 else 10
        st.session_state.score += 1

    # Check collision
    if st.session_state.obstacle_x == 1 and st.session_state.player_y == 1:
        st.session_state.game_over = True

    st.experimental_rerun()

# Scoreboard
st.subheader(f"🏆 Score: {st.session_state.score}")
if st.session_state.game_over:
    st.error("💥 Game Over!")