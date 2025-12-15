import streamlit as st
import pandas as pd
import re
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

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

st.title("K팝 데몬 헌터스 팬덤 형성 요인 분석")

# 1) CSV 로드
@st.cache_data
def load_data():
    return pd.read_csv("data/naver_news.csv", encoding="utf-8-sig")

df = load_data()

# 2) 분석 텍스트 생성 (title + description)
df["title"] = df["title"].astype(str)
df["description"] = df["description"].astype(str)

text = " ".join(df["title"].tolist()) + " " + " ".join(df["description"].tolist())

# HTML 태그 제거
remove_tags = re.compile(r"<.*?>")
text = re.sub(remove_tags, "", text)

# 3) WordCloud 옵션
st.sidebar.header("옵션")
max_words = st.sidebar.slider("단어 개수", 10, 200, 50, 10)

# 불용어(Stopwords)
stopwords = set(STOPWORDS)
stopwords.update(["뉴스", "기자", "단독", "사진", "영상", "보도"])

# 폰트: 맑은고딕
font_path = "data/malgun.ttf"

wc = WordCloud(
    font_path=font_path,
    background_color="white",
    width=1000,
    height=500,
    max_words=max_words,
    stopwords=stopwords
).generate(text)

# 4) 출력
fig, ax = plt.subplots(figsize=(12, 6))
ax.imshow(wc, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)
