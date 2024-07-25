import streamlit as st 
from naraetool.utils import *
from naraetool.table import *
from st_pages import add_page_title
from datetime import date, datetime, timedelta

setting()
add_page_title()

# 데이터 불러오기
table = Table(path="data_frame.json")
#-------------------------------------------------------------------
# Session state
#-------------------------------------------------------------------
today = datetime.now()

default_data = {
        "category": "공통",
        "status": "⚫ 예정",
        "start_date": today,
        "end_date": today,
        "content": ""
    }

if "input_data" not in st.session_state:
    st.session_state["input_data"] = default_data

if "select_idx" not in st.session_state:
    st.session_state["select_idx"] = None 

if "is_expand" not in st.session_state:
    st.session_state["is_expand"] = False

if "is_new" not in st.session_state:
    st.session_state["is_new"] = False
        
#-------------------------------------------------------------------
# Header
#-------------------------------------------------------------------
# 새로 생성하기 버튼(초기화 버튼)
def click_add_btn():
    st.session_state["is_expand"] = True
    st.session_state["is_new"] = True
    st.session_state["input_data"] = default_data

add_btn = st.button(
    label="➕ ADD", 
    use_container_width=True,
    on_click=click_add_btn
)

# Input Box
with st.expander(label="🔧 EDIT SCHEDULE", expanded=st.session_state["is_expand"]):
    # Input box 생성
    output_data = input_box(st.session_state["input_data"])
    
    # 버튼 생성
    columns = st.columns([0.25,0.2,0.1,0.2,0.25])
    save_btn = columns[1].button(
        label="SAVE", 
        use_container_width=True, 
        type="primary", 
        key="save"
    )
    del_btn = columns[3].button(
        label="DELETE", 
        use_container_width=True, 
        type="primary", 
        key="delete"
    )

    # 저장 버튼을 누르면
    if save_btn:
        # 추가이면
        if st.session_state["is_new"]:
            new_data = make_dataframe(output_data)
            table.add_data(new_data)
        # 수정이면
        else:
            idx = st.session_state["select_idx"] 
            table.replace_data(idx, output_data)
        
        st.rerun()

    # 삭제 버튼을 누르면
    if del_btn:
        idx = st.session_state["select_idx"] 
        table.del_data(idx)

        st.rerun()

#-------------------------------------------------------------------
# Table
#-------------------------------------------------------------------
# 다운로드 버튼
@st.cache_data
def data2json(data):
    json_file = data.to_json(
        orient="records", 
        date_format="iso", 
        indent=4, 
        index=False,
        force_ascii=False
    )
    return json_file.encode("utf-8")

_, col = st.columns(spec=[0.75,0.25])

download_btn = col.download_button(
    label="📥 DOWNLOAD",
    data=data2json(table.data),
    file_name="emozis_schedule.json",
    mime="application/json",
    use_container_width=True
)

# 데이터 프레임 생성
viewer = table.viewer()

select_rows = viewer.selection["rows"]
if len(select_rows) > 0:
    select_data = table.select_data(select_rows[0]).to_dict()

    # 상태 초기화를 하기 위함
    if st.session_state["select_idx"] != select_rows[0]:
       st.session_state["input_data"] = select_data
       st.session_state["select_idx"] = select_rows[0]
       st.session_state["is_new"] = False
       st.rerun() 


