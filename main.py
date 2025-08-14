import streamlit as st
import pandas as pd

st.set_page_config(page_title="MBTI 진로 추천 💼", page_icon="💡", layout="wide")

# 🎯 데이터 준비
data = [
    # ENFP
    ["ENFP", "마케터", "💡 마케팅/광고", "창의적이고 사람을 좋아하는 성향", "경영학, 광고홍보학"],
    ["ENFP", "스타트업 창업가", "🚀 창업/경영", "새로운 시도와 네트워킹에 강점", "경영학, 창업학"],
    ["ENFP", "유튜버", "🎥 미디어/콘텐츠", "자유로운 창작과 대중 소통에 적합", "미디어학, 방송연예학"],

    # ISTJ
    ["ISTJ", "회계사", "📊 금융/회계", "규칙과 체계를 잘 지키는 성향", "회계학, 경영학"],
    ["ISTJ", "공무원", "🏛 공공/행정", "안정성과 성실함이 강점", "행정학, 법학"],
    ["ISTJ", "품질관리원", "🔍 제조/품질관리", "세부사항과 정확성에 집중", "산업공학, 기계공학"],

    # INFP
    ["INFP", "작가", "📖 예술/창작", "가치와 스토리를 중시", "문예창작학, 국어국문학"],
    ["INFP", "상담가", "🗣 상담/심리", "타인의 감정을 잘 이해", "심리학, 사회복지학"],
    ["INFP", "번역가", "🌏 언어/국제", "언어 감각과 깊은 몰입", "영문학, 통번역학"],

    # ENTJ
    ["ENTJ", "기업 임원", "💼 경영/리더십", "전략적 사고와 리더십", "경영학, MBA"],
    ["ENTJ", "투자분석가", "📈 금융/투자", "데이터 기반 의사결정", "경제학, 금융학"],
    ["ENTJ", "변호사", "⚖️ 법률", "체계적 분석과 협상력", "법학"],

    # 여기에 나머지 MBTI 유형도 추가 가능
]

df = pd.DataFrame(data, columns=["MBTI", "직업명", "분야", "설명", "관련 학과"])

# 🎨 스타일 적용
st.markdown("""
    <style>
        .job-card {
            background-color: #fdf6ec;
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        }
        .job-title {
            font-size: 20px;
            font-weight: bold;
            color: #ff7f50;
        }
        .job-field {
            font-size: 16px;
            font-weight: 500;
            color: #444;
        }
        .job-desc {
            font-size: 14px;
            margin-top: 5px;
            color: #555;
        }
    </style>
""", unsafe_allow_html=True)

# 🚀 앱 제목
st.title("✨ MBTI 기반 진로 추천 서비스 ✨")
st.write("당신의 성격에 맞는 직업을 찾아보세요 💡")

# 🔍 MBTI 선택
mbti = st.selectbox("MBTI를 선택하세요:", sorted(df["MBTI"].unique()))

# 📌 결과 표시
results = df[df["MBTI"] == mbti]

st.subheader(f"{mbti} 유형의 추천 직업 💖")
cols = st.columns(3)  # 한 줄에 3개 카드

for idx, row in enumerate(results.iterrows()):
    i = idx % 3
    with cols[i]:
        st.markdown(f"""
            <div class="job-card">
                <div class="job-title">{row[1]['직업명']}</div>
                <div class="job-field">{row[1]['분야']}</div>
                <div class="job-desc">💬 {row[1]['설명']}</div>
                <div class="job-desc">🎓 관련 학과: {row[1]['관련 학과']}</div>
            </div>
        """, unsafe_allow_html=True)

