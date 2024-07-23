# python -m streamlit run Home.py
import streamlit as st 
from naraetool.utils import *
from st_pages import show_pages_from_config, add_page_title

setting()

# Sidebar
show_pages_from_config()
add_page_title()

# LinkTree
st.markdown("Docs")
st.link_button(
    label=":blue[💡 프로젝트 소개]",
    url="https://meta-persona-ai.streamlit.app/%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%20%EC%86%8C%EA%B0%9C",
    use_container_width=True,
    # type="primary"
)

st.link_button(
    label=":blue[🔥 프로젝트 진행 상황]",
    url="https://meta-persona-ai.streamlit.app/%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%20%EC%A7%84%ED%96%89%EC%83%81%ED%99%A9",
    use_container_width=True,
    # type="primary"
)

st.link_button(
    label=":blue[📋 2024.07.15 회의록]",
    url="https://meta-persona-ai.streamlit.app/%ED%9A%8C%EC%9D%98%EB%A1%9D",
    use_container_width=True,
    # type="primary"
)

st.markdown("Total")
st.link_button(
    label=":blue[🔗 Google Drive 바로 가기]",
    url="https://drive.google.com/drive/folders/1SZaUQ8dmTElSgmZb7Cfk4XAHWrqpHK7y?usp=drive_link",
    use_container_width=True,
    # type="primary"
)

st.link_button(
    label=":blue[🔗 GitHub 바로 가기]",
    url="https://github.com/meta-persona-ai",
    use_container_width=True,
    # type="primary"
)

st.link_button(
    label=":blue[🔗 Discord 바로 가기]",
    url="https://discord.com/channels/1261648325648846949/1261648326239981571",
    use_container_width=True,
    # type="primary"
)

st.markdown("Backend")
st.link_button(
    label=":blue[🔗 Erdcloud 바로 가기]",
    url="https://www.erdcloud.com/d/N6MPQufNdp4DaFZSy",
    use_container_width=True,
    # type="primary"
)

st.markdown("Frontend")
st.link_button(
    label=":blue[🔗 Figma 바로 가기]",
    url="https://www.figma.com/design/OWaBrYgkomUUl5DYBudCKi?node-id=0-1",
    use_container_width=True,
    # type="primary"
)

    