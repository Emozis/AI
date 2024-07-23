import streamlit as st 
import pandas as pd 
from datetime import date, datetime 


def make_dataframe(
        category:str="-",
        start_date:datetime="1999/12/31",
        end_date:datetime="1999/12/31",
        content:str="-",
        status:str="-"
    ) -> pd.DataFrame:
    dataframe = pd.DataFrame(
        {
            "category": pd.Series([category], dtype='str'),
            "start_date": pd.Series([start_date], dtype='datetime64[ns]'),
            "end_date": pd.Series([end_date], dtype='datetime64[ns]'),
            "content": pd.Series([content], dtype='str'),
            "status": pd.Series([status], dtype='str')
        }
    )

    return dataframe

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
    
    def viewer(self):
        data_viewer = st.dataframe(
            data=self.data,
            key="data",
            on_select="rerun",
            selection_mode="multi-row",
            use_container_width=True,
            hide_index=True,
            column_config=self.column_config
        )

        return data_viewer

    def add_data(self, new_data):
        self.data = pd.concat([self.data, new_data])
        self.data = self.data.sort_values(by=["category","start_date"])
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

   
        



