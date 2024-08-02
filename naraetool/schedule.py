import streamlit as st 
from naraetool.utils import *
from naraetool.mongodb import mongo 
from datetime import datetime 

def date2str(date):
    format = "%Y-%m-%dT%H:%M:%S.%f"
    date_string = date.strftime(format)[:-3]
    return date_string

def str2date(date_string):
    date = datetime.fromisoformat(date_string)
    return date

def input_box(input_data):
    today = datetime.now()
    start_date, end_date = today, today

    category_ops = {"AI":0, "디자인":1, "백엔드":2, "프론트엔드":3}
    status_ops = {"⚫ 예정":0, "🔴 진행중":1, "🟢 완료":2}
    output_data = 0

    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox(
            label="CATEGORY",
            index=category_ops[input_data["category"]],
            options=category_ops.keys()
        )
    
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
            value=(
                str2date(input_data["start_date"]), 
                str2date(input_data["end_date"])
            ),
            format="YYYY/MM/DD"
        )
    except:
        pass

    # 내용 입력
    title = st.text_input(
        label="TITLE",
        value=input_data["title"]
    )
    content = st.text_area(
        label="CONTENT",
        value=input_data["content"],
        height=150
    )

    output_data = {
        "category": category,
        "status": status,
        "start_date": date2str(start_date),
        "end_date": date2str(end_date),
        "title": title,
        "content": content
    }

    return output_data

class Schedule:
    def __init__(self, documents):
        self.categories = ["디자인", "AI", "백엔드", "프론트엔드"]

        self.documents = sorted(documents, key=lambda x: self.set_order(x["status"]))
        self.docs_by_cat = self._transform_docs()

    @staticmethod
    def set_order(status):
        custom_order = {"⚫ 예정":0, "🔴 진행중":1, "🟢 완료":2}

        return custom_order[status]
    
    def _transform_docs(self):
        docs_by_cat = {x: [] for x in self.categories}
        for doc in self.documents:
            docs_by_cat[doc["category"]].append(doc)

        return docs_by_cat

    @staticmethod
    def inner_container(content):
        st.markdown(f"""\
                    <div class="prj-container">
                    {content}
                    </div>
                    """, unsafe_allow_html=True)
        
    @staticmethod 
    def edit_click(doc):
        st.session_state["input_data"] = doc
        st.session_state["is_expand"] = True
        st.session_state["is_new"] = False
        print(doc)

    def _edit_button(self, i, category, schedule):
        _, col = st.columns([0.8,0.2])
        col.button(
            label=":lower_left_fountain_pen: EDIT",
            use_container_width=True,
            key=f"{category}{i}",
            on_click=self.edit_click,
            args=[schedule]
        )

    def make_container(self, category):
        data = self.docs_by_cat[category]

        box = st.container(border=True)
        box.markdown(f"{category}({len(data)})")
        for i, schedule in enumerate(data):
            with box.expander(label=f"{schedule['status'][0]} {schedule['title']}"):
                
                input_text_align(
                    f"🗓️일정: {schedule['start_date'][:10]}-{schedule['end_date'][:10]}", 
                    font=14, 
                    align="left"
                )
                
                content = schedule["content"].replace("\n", "<br>")
                self.inner_container(content)
                
                self._edit_button(i, category, schedule)
                
