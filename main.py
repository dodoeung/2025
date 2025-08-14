import streamlit as st
import pandas as pd

# 데이터 준비
data = [
    ["ENFP", "마케터", "마케팅/광고", "창의적 아이디어와 사람과의 교류를 즐기는 직업", "커뮤니케이션, 기획력", "경영학, 광고홍보학", "4000만원"],
    ["ISTJ", "회계사", "금융/회계", "규칙과 체계에 강한 유형에 적합", "꼼꼼함, 분석력", "회계학, 경영학", "5000만원"],
    ["INFP", "작가", "예술/창작", "가치와 스토리 전달에 집중", "글쓰기, 창의성", "문예창작학, 국어국문학", "3500만원"]
]
df = pd.DataFrame(data, columns=["MBTI", "직업명", "분야", "설명", "필요 역량", "관련 학과", "평균 연봉"])

# 앱 제목
st.title("MBTI 기반 진로 추천 💼")

# MBTI 선택
mbti = st.selectbox("당신의 MBTI를 선택하세요:", df["MBTI"].unique())

# 추천 결과
st.subheader(f"{mbti} 유형에 맞는 추천 직업")
results = df[df["MBTI"] == mbti]

for _, row in results.iterrows():
    st.markdown(f"### {row['직업명']} ({row['분야']})")
    st.write(f"**설명:** {row['설명']}")
    st.write(f"**필요 역량:** {row['필요 역량']}")
    st.write(f"**관련 학과:** {row['관련 학과']}")
    st.write(f"**평균 연봉:** {row['평균 연봉']}")
    st.markdown("---")

