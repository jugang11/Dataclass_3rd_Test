import streamlit as st
import pandas as pd
import re
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from konlpy.tag import Okt
import altair as alt
from collections import Counter

st.set_page_config(
    page_title="K팝 데몬 헌터스 팬덤 형성 요인 분석",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get help': "https://docs.streamlit.io",
        'Report a bug': "https://streamlit.io",
        'About': "### 주은강 \n - [Contact](https://www.instagram.com/zoollllk/)"
    }
)

st.title("K팝 데몬 헌터스 팬덤 형성 요인 분석")

# 수집한 데이터 불러오기
@st.cache_data
def load_data():
    return pd.read_csv("data/naver_news.csv", encoding="utf-8-sig")

df = load_data()

# 전처리: 날짜 변환
df["pubDate"] = pd.to_datetime(df["pubDate"])
df["date"] = df["pubDate"].dt.date

# 전처리: 텍스트 합치기
df["title"] = df["title"].astype(str)
df["description"] = df["description"].astype(str)
text = " ".join(df["title"].tolist()) + " " + " ".join(df["description"].tolist())

# HTML 태그 제거
text = re.sub(r"<.*?>", "", text)

# 형태소 분석 (명사 추출) - 캐싱
@st.cache_data
def extract_all_nouns(text):
    okt = Okt()
    return okt.nouns(text)

all_nouns = extract_all_nouns(text)

# ========== 사이드바 옵션 ==========
st.sidebar.header("옵션")
max_words = st.sidebar.slider("워드클라우드 단어 개수", 10, 200, 50, 10)
top_n = st.sidebar.slider("Top 키워드 개수", 5, 30, 15, 5)

# ========== 1. 워드클라우드 ==========
st.header("1. 워드클라우드")

stopwords = set(STOPWORDS)
stopwords.update(["뉴스", "기자", "단독", "사진", "영상", "보도", "것", "등", "수", "위"])

font_path = "data/malgun.ttf"

wc = WordCloud(
    font_path=font_path,
    background_color="white",
    width=1000,
    height=500,
    max_words=max_words,
    stopwords=stopwords
).generate(" ".join(all_nouns))

fig, ax = plt.subplots(figsize=(12, 6))
ax.imshow(wc, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

# ========== 2. 시계열 분석 (Altair) ==========
st.header("2. 일별 기사량 추이")

min_date = df["date"].min()
max_date = df["date"].max()

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("시작일", min_date)
with col2:
    end_date = st.date_input("종료일", max_date)

df_filtered = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

daily_counts = df_filtered.groupby("date").size().reset_index(name="count")
daily_counts["date"] = pd.to_datetime(daily_counts["date"])

chart = alt.Chart(daily_counts).mark_line(point=True).encode(
    x=alt.X("date:T", title="날짜"),
    y=alt.Y("count:Q", title="기사 수"),
    tooltip=["date:T", "count:Q"]
).properties(
    height=400
).interactive()

st.altair_chart(chart, use_container_width=True)
