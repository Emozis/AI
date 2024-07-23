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
# Header
#-------------------------------------------------------------------
today = datetime.now()

with st.expander(label="➕ ADD SCHEDULE", expanded=False):
    col1, col2 = st.columns(2)
    # 카테고리 입력
    with col1:
        category = st.selectbox(
            label="CATEGORY",
            options=["공통", "AI", "디자인", "백엔드", "프론트엔드"]
        )
    # 진행상황 입력
    with col2:
        status = st.selectbox(
            label="STATUS",
            options=["⚫ 예정","🔴 진행중","🟢 완료"]
        )
    # 시작, 종료일 입력
    try:
        start_date, end_date = st.date_input(
            label="DATE",
            value=(today, today),
            format="YYYY/MM/DD"
        )
    except:
        pass
    # 내용 입력
    content = st.text_area(
        label="CONTENT",
        height=200
    )

    # 추가 버튼
    add_btn = st.button(
        label="ADD",
        use_container_width=True,
        type="primary"
    )

    # 데이터 추가
    if add_btn:
        new_data = make_dataframe(
            category, start_date, end_date, content, status
        )
        table.add_data(new_data)
#-------------------------------------------------------------------
# Table
#-------------------------------------------------------------------
# 삭제 버튼 생성
del_btn = side_button(
    label="DELETE",
    position="right",
    ratio=0.2,
    type="primary"
)

# 데이터 프레임 생성
viewer = table.viewer()

# 데이터 삭제
if del_btn:
    del_idx = viewer.selection["rows"]
    table.del_data(del_idx)

    st.rerun()