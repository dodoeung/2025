import streamlit as st
from pathlib import Path
from fpdf import FPDF
import base64

# ----------------------------- 앱 기본 설정 -----------------------------
st.set_page_config(page_title="스터디 업 건강 업 병원", page_icon="🩺", layout="centered")

# ----------------------------- 스타일 -----------------------------
st.markdown("""
    <style>
        body {
            background-color: #FFF0F5;
        }
        .heart-button {
            display: inline-block;
            font-size: 22px;
            padding: 0.4em 1em;
            margin: 8px;
            border: 2px solid pink;
            border-radius: 30px;
            background-color: #ffe4e1;
            color: #d6336c;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.2s ease-in-out;
        }
        .heart-button:hover {
            background-color: #ffccd5;
        }
        .balloon {
            background-color: #fff9c4;
            border: 2px dashed #f48fb1;
            border-radius: 20px;
            padding: 20px;
            font-size: 18px;
            margin: 20px 0;
        }
        .paper {
            background-image: repeating-linear-gradient(white, white 30px, #f0f0f0 31px);
            border: 2px solid #ddd;
            padding: 20px;
            border-radius: 10px;
            font-family: 'Courier New';
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------- 상태 초기화 -----------------------------
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = {}

# ----------------------------- 질문 리스트 -----------------------------
questions = [
    ("오늘 하루 공부 시간은 얼마나 되나요?", ["1시간 이하", "2~3시간", "4~5시간", "6시간 이상"]),
    ("어떤 운동을 주로 하나요?", ["🏃‍♀️ 달리기", "🏋️‍♂️ 헬스", "🧘 요가", "🚫 안 해요"]),
    ("자주 먹는 음식 종류는?", ["🍚 밥", "🍞 빵", "🍜 면", "🍗 고기", "🍭 간식만 먹어요"]),
    ("요즘 느끼는 증상은 무엇인가요?", ["🖐️ 손목 통증", "🦵 종아리 붓기", "👀 눈 피로", "💤 졸림", "🧠 두통", "😣 허리 통증"]),
    ("공부할 때의 자세는?", ["🪑 바른 자세 유지", "💻 구부정한 자세", "📱 누워서 공부"]) 
]

# ----------------------------- 첫 화면 -----------------------------
if st.session_state.step == 0:
    st.markdown("""
    <h1 style='text-align: center;'>🎓 스터디 업 건강 업 병원에 온 걸 환영해요! 🏥</h1>
    <p style='text-align: center;'>당신의 건강을 체크하고, 귀여운 보충 진단서를 받아보세요! 💖</p>
    <div style='text-align: center;'>
        <img src='https://media.giphy.com/media/l0HlQ7LRal6C3RZ6w/giphy.gif' width='250'>
    </div>
    """, unsafe_allow_html=True)

    name = st.text_input("이름을 입력하세요")
    age = st.number_input("나이", 6, 20)
    gender = st.radio("성별", ["여자", "남자", "기타"])
    grade = st.selectbox("학년", ["초등학생", "중학생", "고등학생"])

    if st.button("🩺 진단 시작하기"):
        st.session_state.name = name
        st.session_state.age = age
        st.session_state.gender = gender
        st.session_state.grade = grade
        st.session_state.step = 1

# ----------------------------- 질문 단계 -----------------------------
elif 1 <= st.session_state.step <= len(questions):
    q_idx = st.session_state.step - 1
    question, options = questions[q_idx]

    st.markdown(f"<h3>{question}</h3>", unsafe_allow_html=True)

    for opt in options:
        if st.button(f"❤️ {opt}", key=f"{q_idx}_{opt}"):
            st.session_state.answers[question] = opt
            st.session_state.step += 1
            st.rerun()

# ----------------------------- 결과 보여주기 (말풍선) -----------------------------
elif st.session_state.step == len(questions)+1:
    st.markdown("<div class='balloon'>✅ <b>진단 결과 요약</b><br>", unsafe_allow_html=True)
    for q, ans in st.session_state.answers.items():
        st.markdown(f"<b>{q}</b>: {ans}<br>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("📋 진단서 보기"):
        st.session_state.step += 1
        st.rerun()

# ----------------------------- 진단서 -----------------------------
elif st.session_state.step == len(questions)+2:
    name = st.session_state.name
    st.markdown(f"<h2>📄 {name}의 건강 보충 진단서</h2>", unsafe_allow_html=True)
    st.markdown("<div class='paper'>", unsafe_allow_html=True)

    answers = st.session_state.answers
    study = answers.get(questions[0][0], "")
    food = answers.get(questions[2][0], "")
    symptom = answers.get(questions[3][0], "")
    posture = answers.get(questions[4][0], "")

    posture_tip = {
        "🪑 바른 자세 유지": "🪑 바른 자세 최고! 지금처럼 유지해요!",
        "💻 구부정한 자세": "💻 등과 목에 무리 가요! 바른 자세로 허리를 펴 보세요!",
        "📱 누워서 공부": "📱 누워서 공부는 집중력 저하와 건강에 안 좋아요! 책상에 앉아서 해요!"
    }.get(posture, "")

    st.markdown(f"""
    🔎 <b>주요 증상:</b> {symptom}<br>
    🍱 <b>식습관:</b> {food} — 골고루 먹는 습관을 들이면 건강해져요!<br>
    📖 <b>공부 시간:</b> {study} — 너무 길면 쉬는 시간도 꼭 챙기세요!<br>
    🪑 <b>공부 자세 조언:</b> {posture_tip}<br><br>
    ✅ <b>추가 팁:</b> 매일 물 마시기 💧, 스트레칭 🧘, 충분한 수면 😴<br><br>
    💌 <b>응원 메시지:</b> 오늘도 진단받느라 수고했어요! 당신은 멋진 사람이에요 💖 화이팅! 🚀<br><br>
    🔖 <b>진단 도장:</b> <span style='font-size:24px;'>🔴 스터디 헬스 인증 완료!</span>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # 진단서 저장 기능
    if st.button("📥 진단서 저장하기"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"{name}의 건강 보충 진단서", ln=True, align='C')
        for k, v in st.session_state.answers.items():
            pdf.cell(200, 10, txt=f"{k}: {v}", ln=True)
        pdf.cell(200, 10, txt=f"공부 자세 조언: {posture_tip}", ln=True)
        pdf.cell(200, 10, txt="응원 메시지: 오늘도 수고했어요! 화이팅!", ln=True)

        filepath = f"{name}_진단서.pdf"
        pdf.output(filepath)

        with open(filepath, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            href = f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="{filepath}">📥 진단서 다운로드</a>'
            st.markdown(href, unsafe_allow_html=True)

# 끝!
