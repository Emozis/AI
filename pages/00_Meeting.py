import streamlit as st 
from pathlib import Path
from naraetool.utils import *
from streamlit_pdf_viewer import pdf_viewer

setting()

st.title("📚 회의록")

path = Path("./static/meeting")
meeting_list = sorted(path.glob("**/*.md"), reverse=True)

isexpand = True
for meeting in meeting_list:
    with st.expander(label=meeting.name, expanded=isexpand):
        read_mdfile(meeting)
        isexpand = False

