import streamlit as st 
import pandas as pd 
from datetime import date, datetime 

def input_box(input_data):
    category_ops = {"공통":0, "AI":1, "디자인":2, "백엔드":3, "프론트엔드":4}
    status_ops = {"⚫ 예정":0, "🔴 진행중":1, "🟢 완료":2}

    col1, col2 = st.columns(2)
    # 카테고리 입력
    with col1:
        category = st.selectbox(
            label="CATEGORY",
            index=category_ops[input_data["category"]],
            options=category_ops.keys()
        )
    # 진행상황 입력
    with col2:
        status = st.selectbox(
            label="STATUS",
            index=status_ops[input_data["status"]],
            options=status_ops.keys()
        )
    # 시작, 종료일 입력
    try:
        start_date, end_date = st.date_input(
            label="DATE",
            value=(input_data["start_date"], input_data["end_date"]),
            format="YYYY/MM/DD"
        )
    except:
        pass
    # 내용 입력
    content = st.text_area(
        label="CONTENT",
        value=input_data["content"],
        height=200
    )

    output_data = {
        "category": category,
        "status": status,
        "start_date": start_date,
        "end_date": end_date,
        "content": content
    }

    return output_data

def make_dataframe(output_data) -> pd.DataFrame:
    data = pd.DataFrame(
        {
            "category": pd.Series([output_data["category"]], dtype='str'),
            "start_date": pd.Series([output_data["start_date"]], dtype='datetime64[ns]'),
            "end_date": pd.Series([output_data["end_date"]], dtype='datetime64[ns]'),
            "content": pd.Series([output_data["content"]], dtype='str'),
            "status": pd.Series([output_data["status"]], dtype='str')
        }
    )

    return data


class Table:
    def __init__(self, path="data.json"):
        self.path = path
        self.data = self._load_data()
        self.column_config = {
            "category": st.column_config.TextColumn(
                "분류",
                width="small"
            ),
            "start_date": st.column_config.DateColumn(
                "시작 일시",
                width="small",
                format="YYYY/MM/DD"
            ),
            "end_date": st.column_config.DateColumn(
                "종료 일시",
                width="small",
                format="YYYY/MM/DD"
            ),
            "content": st.column_config.TextColumn(
                "내용",
                width="medium"
            ),
            "status": st.column_config.TextColumn(
                "진행상황",
                width="small"
            )
        }

    def _load_data(self):
        data = pd.read_json(self.path, orient="records")
        if data.shape[0] == 0:
            columns = ["category", "start_date", "end_date", "content", "status"]
            return pd.DataFrame(columns=columns)
        else:
            data["start_date"] = pd.to_datetime(data["start_date"])
            data["end_date"] = pd.to_datetime(data["end_date"])

        return data 
    
    @staticmethod
    def viewer_rerun():
        ""
    
    def viewer(self):
        data_viewer = st.dataframe(
            data=self.data,
            key="data",
            on_select=self.viewer_rerun,
            selection_mode="single-row",
            use_container_width=True,
            hide_index=True,
            height=2000,
            column_config=self.column_config
        )

        return data_viewer
    
    def select_data(self, idx):
        sub_data = self.data.iloc[idx]
        return sub_data

    def add_data(self, new_data):
        self.data = pd.concat([self.data, new_data])
        self.data = self.data.sort_values(by=["category","start_date"])
        self.save_data()

    def replace_data(self, idx, new_data):
        self.data.iloc[idx] = new_data
        self.save_data()

    def del_data(self, del_idx):
        self.data = self.data.drop(index=del_idx)
        self.save_data()

    def save_data(self):
        self.data.to_json(
            self.path, 
            orient="records", 
            date_format="iso", 
            indent=4, 
            index=False,
            force_ascii=False
        )

   
        



