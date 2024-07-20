import streamlit as st 
import pandas as pd 
from datetime import date, datetime 

default_frame = pd.DataFrame(
    {
        "category": pd.Series(["전체"], dtype='str'),
        "start_date": pd.Series(["2024/07/17"], dtype='datetime64[ns]'),
        "end_date": pd.Series(["2024/07/17"], dtype='datetime64[ns]'),
        "content": pd.Series(["내용을 입력하세요"], dtype='str'),
        "status": pd.Series(["🔴 예정"], dtype='str')
    }
)

def load_data(path="./data_frame.json"):
    data = pd.read_json(path, orient="records")
    if data.shape[0] == 0:
        data = default_frame
    else:
        data["start_date"] = pd.to_datetime(data["start_date"])
        data["end_date"] = pd.to_datetime(data["end_date"])

    return data 


class DataTable:
    def __init__(self, data):
        self.data = data 
        self.column_config = {
            "category": st.column_config.SelectboxColumn(
                "분류",
                width="small",
                options=[
                    "공통","AI","디자인","백엔드","프론트엔드","통신"
                ],
                required=True
            ),
            "start_date": st.column_config.DateColumn(
                "시작 일시",
                width="small",
                default=datetime.now().date(),
                min_value=date(2024, 1, 1),
                max_value=date(2050, 12, 31),
                format="YYYY/MM/DD"
            ),
            "end_date": st.column_config.DateColumn(
                "종료 일시",
                width="small",
                default=datetime.now().date(),
                min_value=date(2024, 1, 1),
                max_value=date(2050, 12, 31),
                format="YYYY/MM/DD"
            ),
            "content": st.column_config.TextColumn(
                "내용",
                width="medium",
                help="Streamlit **widget** commands 🎈",
                default="입력",
            ),
            "status": st.column_config.SelectboxColumn(
                "진행상황",
                width="small",
                options=[
                    "🔴 예정","🟢 진행중","🔵 완료"
                ],
                required=True
            ),
        }
        
    def insert_table(self, column):
        if column == "전체":
            data = self.data.sort_values(by=["category"])
        else:
            data = self.data[self.data["category"]==column]

        table = st.data_editor(
            data.reset_index(drop=True),
            hide_index=True,
            num_rows="dynamic",
            use_container_width=True,
            column_config=self.column_config
        )

        return table