import streamlit as st 
from naraetool.utils import *
from naraetool.table import *
from st_pages import add_page_title
from datetime import date, datetime, timedelta

setting()

add_page_title()

# 데이터 불러오기
data_frame = load_data("./data_frame.json")

# 데이터 편집

tabletool = DataTable(data_frame)

columns = st.columns(spec=[0.8,0.2])
save_btn = columns[-1].button(
    label="저장",
    use_container_width=True,
    type="primary"
)

column = st.selectbox(
    label="CATEGORY",
    options=["전체", "공통", "AI", "디자인", "백엔드", "프론트엔드"]
)

edited_data = tabletool.insert_table(column=column)
print(data_frame)
print("="*50)
print(edited_data)

if save_btn:
    edited_data.to_json(
        "data_frame.json", 
        orient="records", 
        date_format="iso", 
        indent=4, 
        index=False,
        force_ascii=False
    )