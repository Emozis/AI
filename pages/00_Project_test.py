import streamlit as st 
from naraetool.utils import *
from naraetool.mongodb import mongo
from naraetool.schedule import input_box, Schedule, date2str
from datetime import datetime

setting(layout="wide")

# DB 컬렉션 연결
if "mongo" not in st.session_state:
    mongo.connect_collection("project")
    st.session_state["mongo"] = mongo
else:
    mongo = st.session_state["mongo"]

# 데이터 업데이트
schedule = Schedule(mongo.documents)
#-------------------------------------------------------------------
# Session state
#-------------------------------------------------------------------
today = datetime.now()

default_data = {
    "category": "AI",
    "status": "⚫ 예정",
    "start_date": date2str(today),
    "end_date": date2str(today),
    "title": "",
    "content": ""
}

if "input_data" not in st.session_state:
    st.session_state["input_data"] = default_data

if "is_expand" not in st.session_state:
    st.session_state["is_expand"] = False

if "is_new" not in st.session_state:
    st.session_state["is_new"] = False

def add_click():
    st.session_state["is_expand"] = True
    st.session_state["is_new"] = True
    st.session_state["input_data"] = default_data

def save_click():
    input_data =st.session_state["input_data"]
    output_data = st.session_state["output_data"]
    # 추가
    if st.session_state["is_new"]:
        mongo.create(output_data)
    # 수정
    else:
        mongo.update(input_data, output_data)

    st.session_state["is_expand"] = True
    st.session_state["input_data"] = default_data

def del_click():
    input_data =st.session_state["input_data"]
    # 삭제
    mongo.delete(input_data)

    st.session_state["is_expand"] = True
    st.session_state["input_data"] = default_data
#-------------------------------------------------------------------
# Header
#-------------------------------------------------------------------
st.title("🔥 프로젝트 진행상황")
vertical_space(30)

# Add Button(초기화 버튼)
_, center, _ = st.columns([0.15,0.7,0.15])
add_btn = center.button(
    label="➕ ADD", 
    type="primary",
    use_container_width=True,
    on_click=add_click
)

# Edit Schedule
_, center, _ = st.columns([0.15,0.7,0.15])
with center.expander(
    label=":gear: EDIT SCHEDULE", 
    expanded=st.session_state["is_expand"]
):
    # Form
    output_data = input_box(st.session_state["input_data"])
    st.session_state["output_data"] = output_data

    # Buttons
    columns = st.columns([0.25,0.2,0.1,0.2,0.25])
    ## Save Button
    save_btn = columns[1].button(
        label="SAVE", 
        use_container_width=True, 
        type="primary", 
        key="save",
        on_click=save_click
    )
    ## Delete Button
    del_btn = columns[3].button(
        label="DELETE", 
        use_container_width=True, 
        type="primary", 
        key="delete",
        on_click=del_click
    )

vertical_space(20)
#-------------------------------------------------------------------
# Body
#-------------------------------------------------------------------
input_text_align("Schedule", font=30)
vertical_space(5)
input_text_align("⚫ 예정 🔴 진행중 🟢 완료", align="right")
vertical_space(20)

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    schedule.make_container("디자인")
with col2:
    schedule.make_container("AI")
with col3:
    schedule.make_container("백엔드")
with col4:
    schedule.make_container("프론트엔드")