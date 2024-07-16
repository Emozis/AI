import streamlit as st 
import pathlib
from naraetool.style import *

setting()

path = Path("./meeting")
pdf_list = sorted(path.glob("**/*.pdf"), reverse=True)

for pdf_file in pdf_list:
    with st.expander(label=pdf_file.name, expanded=False):
        pdf_viewer(pdf_file)
