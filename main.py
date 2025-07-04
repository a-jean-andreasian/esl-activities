import os
import streamlit as st
from utils import EslGames
from functools import lru_cache
from typing import LiteralString
import hmac


# Access control =======================================================================================================
@lru_cache(maxsize=1)
def get_password() -> str:
    pwd = os.environ.get('PASSWORD')
    if not pwd:
        with open('.password', 'r', encoding='utf-8') as f:
            pwd = f.read().strip()
            os.environ['PASSWORD'] = pwd
    return pwd


def compare_password(user_input: LiteralString) -> bool:
    return hmac.compare_digest(user_input, get_password())


def access_website():
    if "access_granted" not in st.session_state:
        st.session_state.access_granted = False

    if not st.session_state.access_granted:
        st.write('To access the ESL activities, please enter the password:')

        password = st.text_input("Password", type="password", key="password_input")
        if st.button("Submit"):
            if compare_password(user_input=password.strip()):
                st.session_state.access_granted = True
                st.rerun()
            else:
                st.error("Access denied. Incorrect password.")
    return st.session_state.access_granted


# Actual website =======================================================================================================
# Game display =========================================================================================================
def display_game(game: dict):
    with st.container():
        st.markdown("---")
        st.subheader(game['name'])

        if tags := game.get("tags"):
            cols = st.columns(len(tags))
            for col, tag in zip(cols, tags):
                col.markdown(f"`{tag}`")

        st.write(game['description'])



def games_section():
    esl_games = EslGames()
    esl_games.load_games()
    games: list[dict] = esl_games.games

    with st.expander("ESL Games"):
        for game in games:
            display_game(game)


# Main app =============================================================================================================
if access_website():
    games_section()
    st.divider()
