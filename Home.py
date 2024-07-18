# python -m streamlit run Home.py
import streamlit as st 
from naraetool.style import *
from st_pages import show_pages_from_config

setting()

show_pages_from_config()


read_mdfile("./docs/readme.md")
    