import streamlit as st

st.set_page_config(            # 페이지 설정
    page_title="K팝 데몬 헌터스 팬덤 형성 요인 분석",   # 페이지 Tab의 타이틀
    page_icon="🤖",                 # 페이지 Tab의 아이콘
    layout="wide",                  # 페이지 레이아웃
    # 사이드바 초기 상태
    initial_sidebar_state="expanded",
    # 페이지 오른쪽 상부의 메뉴
    menu_items={
        'Get help': "https://docs.streamlit.io",
        'Report a bug': "https://streamlit.io",
        'About': "### 주은강 \n - [Contact](https://www.instagram.com/zoollllk/)"
    }
)