import streamlit as st
from PIL import Image

# ----------------------------- 앱 기본 설정 -----------------------------
st.set_page_config(page_title="스터디 업 건강 업 병원", page_icon="🩺", layout="centered")

# ----------------------------- 세션 상태 초기화 -----------------------------
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = {}

# ----------------------------- 질문 및 선택지 -----------------------------
questions = [
    {"question": "⏰ 하루 평균 공부 시간은 얼마나 되나요?", "options": ["1시간 이하 🐢", "2~4시간 📘", "5~7시간 📚", "8시간 이상 🔥"]},
    {"question": "🤸 주로 하는 운동은 무엇인가요?", "options": ["달리기 🏃", "헬스 🏋️", "요가 🧘", "거의 안 함 😅"]},
    {"question": "🍽️ 식습관은 어떤가요?", "options": ["정식 식사 🍚", "빵 위주 🥐", "면 위주 🍜", "불규칙해요 ❓"]},
    {"question": "💢 요즘 느끼는 증상은?", "options": ["손목 저림 🤕", "허리 통증 😩", "종아리 붓기 🦵", "두통 🤯", "눈 피로 👀", "어깨 결림 🧊"]},
    {"question": "🪑 공부할 때 자세는 어떤가요?", "options": ["바른 자세 유지 👍", "구부정한 자세 😵", "누워서 공부 😴"]},
]

# ----------------------------- 자세 피드백 -----------------------------
posture_feedback = {
    "바른 자세 유지 👍": "🪑 바른 자세 최고! 지금처럼 유지해요!",
    "구부정한 자세 😵": "💻 등과 목에 무리 가요! 바른 자세로 허리를 펴 보세요!",
    "누워서 공부 😴": "📱 누워서 공부는 집중력 저하와 건강에 안 좋아요! 책상에 앉아서 해요!"
}

# ----------------------------- 첫 화면 -----------------------------
if st.session_state.step == 0:
    st.markdown("""
        <h1 style='text-align: center;'>💖 스터디 업 건강 업 병원에 온 걸 환영해요! 💖</h1>
        <p style='text-align: center;'>당신의 건강을 귀엽게 진단해드릴게요! 아래 정보를 입력해주세요 🩺</p>
    """, unsafe_allow_html=True)

    name = st.text_input("이름 ✏️")
    age = st.number_input("나이 🎂", min_value=6, max_value=25, step=1)
    grade = st.selectbox("학년 🎓", ["초등학생", "중학생", "고등학생"])
    gender = st.radio("성별 🚻", ["여자", "남자", "기타"])

    if st.button("📋 진단 시작하기"):
        st.session_state.answers["name"] = name
        st.session_state.answers["age"] = age
        st.session_state.answers["grade"] = grade
        st.session_state.answers["gender"] = gender
        st.session_state.step = 1
        st.experimental_rerun()

# ----------------------------- 질문 단계 -----------------------------
elif 1 <= st.session_state.step <= len(questions):
    idx = st.session_state.step - 1
    q = questions[idx]

    st.markdown(f"""
        <h2 style='text-align: center; color: #ff69b4;'>❓ {q['question']}</h2>
        <div style='text-align: center;'>💗💗💗💗💗</div><br>
    """, unsafe_allow_html=True)

    for option in q["options"]:
        if st.button(f"💖 {option}"):
            st.session_state.answers[q["question"]] = option
            st.session_state.step += 1
            st.experimental_rerun()

# ----------------------------- 결과 요약 (말풍선) -----------------------------
elif st.session_state.step == len(questions) + 1:
    st.markdown("""
        <div style='text-align: center; font-size: 24px;'>
        🗨️ <b>진단 결과가 나왔어요!</b><br><br>
        아래에서 나의 건강 진단서를 확인해보세요 💌
        </div>
    """, unsafe_allow_html=True)

    if st.button("📄 진단서 확인하기"):
        st.session_state.step += 1
        st.experimental_rerun()

# ----------------------------- 진단서 -----------------------------
elif st.session_state.step == len(questions) + 2:
    name = st.session_state.answers.get("name", "이름없음")
    posture = st.session_state.answers.get("🪑 공부할 때 자세는 어떤가요?", "")
    posture_tip = posture_feedback.get(posture, "")

    st.markdown(f"""
        <div style="background-color:#fffaf0; border: 2px dashed #000; padding: 30px; font-family: 'Courier New', monospace;">
        <h2 style="text-align:center;">📋 {name}님의 건강 보충 진단서 📋</h2>
        <hr>
        <p><b>👧 이름:</b> {st.session_state.answers.get('name')}<br>
        <b>🎂 나이:</b> {st.session_state.answers.get('age')}세<br>
        <b>🎓 학년:</b> {st.session_state.answers.get('grade')}<br>
        <b>🚻 성별:</b> {st.session_state.answers.get('gender')}</p>

        <p><b>⏰ 공부 시간:</b> {st.session_state.answers.get('⏰ 하루 평균 공부 시간은 얼마나 되나요?')}<br>
        <b>🤸 운동 습관:</b> {st.session_state.answers.get('🤸 주로 하는 운동은 무엇인가요?')}<br>
        <b>🍽️ 식습관:</b> {st.session_state.answers.get('🍽️ 식습관은 어떤가요?')}<br>
        <b>💢 느끼는 증상:</b> {st.session_state.answers.get('💢 요즘 느끼는 증상은?')}<br>
        <b>🪑 공부 자세:</b> {st.session_state.answers.get('🪑 공부할 때 자세는 어떤가요?')}</p>

        <hr>
        <p><b>📌 건강 조언:</b><br>
        {posture_tip}<br><br>
        <b>🌟 응원 메시지:</b><br>
        오늘도 건강 챙기느라 수고했어요! 🩷 당신은 정말 멋진 학생이에요! 💪✨<br>
        앞으로도 건강하고 즐겁게 공부하길 응원할게요 🎉🎈</p>

        <p style="text-align: right; font-size: 32px;">🔴 건강 병원 인증 도장 🔴</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🔁 다시 진단하기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
