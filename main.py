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

# 수집한 데이터 불러오기
df = pd.read_csv('data/naver_news.csv', encoding='utf-8-sig')

# title과 description을 하나의 문자열로 합치기
df['title'] = df['title'].astype(str)
df['description'] = df['description'].astype(str)
text = ' '.join(df['title'].tolist()) + ' ' + ' '.join(df['description'].tolist())

# HTML 태그 제거
text = re.sub(r'<.*?>', '', text)

# 한글 폰트 경로 찾기
font_path = font_manager.findfont('Malgun Gothic')

# 불용어 설정
stop_words = set(STOPWORDS)
stop_words.update(['뉴스', '기자', '단독', '사진', '영상', '보도'])

# 워드클라우드 객체 생성
wc = WordCloud(
    font_path=font_path,
    max_words=50,
    width=1000,
    height=500,
    stopwords=stop_words,
    background_color='white',
    colormap='viridis'
).generate(text)

# 워드클라우드 시각화 (Streamlit용)
fig, ax = plt.subplots(figsize=(12, 6))
ax.imshow(wc, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)
