import os
import pathlib

ASSETS_PATH = pathlib.Path(__file__).parent.parent / "assets"
AVATAR_PATH = pathlib.Path(__file__).parent.parent / "assets" / "avatars"
PREFERENCES_PATH = pathlib.Path(__file__).parent.parent / "preferences"


import streamlit as st


def is_init(var: str):
    return var in st.session_state

def not_init(var: str):
    return var not in st.session_state

def get(var: str):
    # I don't think we need this, other than to raise an error
    # if not_init(var):
    #     raise ValueError(f"Variable {var} not initialized")
    return st.session_state.get(var, None)

def set(var: str, value):
    st.session_state[var] = value



# BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# from enum import Enum, auto
# class Colors(Enum):
class Colors():
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7

def colorize(color: int):
    return f'\033[1;3{color}m'

def cprint(string: str, color: Colors):
    print_this = f'\033[1;3{color}m' + string + '\033[0m'

    if os.getenv("DEBUG", True):
        print(print_this)
    else:
        pass
