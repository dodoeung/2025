import streamlit as st
import random

# 앱 기본 설정
st.set_page_config(page_title="스터디 업 건강 업 병원 💉", page_icon="🩺", layout="centered")

# 애니메이션 효과용 이모지
sparkle = "✨"
stars = "🌟"

# 페이지 상태 초기화
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# 질문 리스트
questions = [
    {
        "question": "공부는 하루에 몇 시간 정도 해요?",
        "key": "study_time",
        "options": ["📘 1시간 이하", "📗 2~3시간", "📕 4~6시간", "📙 7시간 이상"]
    },
    {
        "question": "요즘 주로 하는 운동은 뭐예요?",
        "key": "exercise",
        "options": ["🏃 달리기", "💪 헬스", "🧘 요가/스트레칭", "🚫 운동 안 해요"]
    },
    {
        "question": "식사는 어떻게 하고 있어요?",
        "key": "diet",
        "options": ["🍚 밥 위주", "🍞 빵 위주", "🍜 면 위주", "🍗 고기 위주", "🍭 간식 위주"]
    },
    {
        "question": "공부할 때 주로 어떤 증상이 느껴져요?",
        "key": "symptom",
        "options": ["🖐️ 손목 통증", "👀 눈 피로", "🧠 두통", "🦵 종아리 붓기", "😵 어깨 결림"]
    },
    {
        "question": "공부할 때 주로 어떤 자세인가요?",
        "key": "posture",
        "options": ["🪑 바른 자세 유지", "💻 구부정한 자세", "📱 누워서 공부"]
    },
]

# 증상별 피드백
symptom_feedback = {
    "🖐️ 손목 통증": "손목 스트레칭을 해주고, 손목 받침대를 써보세요!",
    "👀 눈 피로": "20분 공부 후 20초 동안 먼 곳을 바라보는 습관을 들이세요!",
    "🧠 두통": "휴식이 필요해요! 물도 충분히 마시고 스트레칭도 해보세요.",
    "🦵 종아리 붓기": "가볍게 다리 스트레칭을 하거나 자리에서 일어나 움직이세요!",
    "😵 어깨 결림": "어깨를 돌려주는 스트레칭과 바른 자세를 유지해보세요!"
}

# 식단 피드백
diet_feedback = {
    "🍚 밥 위주": "균형 잡힌 식사를 유지하고 있어요! 좋아요!",
    "🍞 빵 위주": "탄수화물 위주의 식사! 단백질과 채소를 추가해보세요!",
    "🍜 면 위주": "면만 먹으면 영양 불균형이 올 수 있어요! 밥도 챙겨 먹어요~",
    "🍗 고기 위주": "단백질은 좋지만 채소도 함께 먹어줘야 해요!",
    "🍭 간식 위주": "간식만 먹지 말고 정식 식사를 꼭 챙기도록 해요!"
}

# 자세 피드백
posture_feedback = {
    "🪑 바른 자세 유지": "🪑 바른 자세 최고! 지금처럼 유지해요!",
    "💻 구부정한 자세": "💻 등과 목에 무리 가요! 바른 자세로 허리를 펴 보세요!",
    "📱 누워서 공부": "📱 누워서 공부는 집중력 저하와 건강에 안 좋아요! 책상에 앉아서 해요!"
}

# 시작 페이지
if st.session_state.step == 0:
    st.markdown(f"""
        <div style='text-align: center;'>
            <h1>{sparkle} 스터디 업 건강 업 병원에 온 걸 환영해요! {sparkle}</h1>
            <p>귀엽고 건강하게 공부 습관을 체크해봐요!</p>
            <img src='https://media.tenor.com/JBgYzQHm3rYAAAAi/kawaii.gif' width='200'>
        </div>
    """, unsafe_allow_html=True)

    with st.form("user_info"):
        name = st.text_input("이름을 입력해주세요")
        age = st.number_input("나이", min_value=6, max_value=20, step=1)
        gender = st.radio("성별", ["여자", "남자", "기타"])
        grade = st.selectbox("학년", ["초등학생", "중학생", "고등학생"])
        submitted = st.form_submit_button("진단 시작하기 💖")
        if submitted:
            st.session_state.user = {"name": name, "age": age, "gender": gender, "grade": grade}
            st.session_state.step = 1

# 질문 단계
elif 1 <= st.session_state.step <= len(questions):
    q = questions[st.session_state.step - 1]
    st.markdown(f"""
        <div style='background-color:#FFF0F5; padding:20px; border-radius:15px;'>
            <h2>{stars} {q['question']}</h2>
        </div>
    """, unsafe_allow_html=True)

    for option in q['options']:
        if st.button(option, key=option):
            st.session_state.answers[q['key']] = option
            st.session_state.step += 1
            st.experimental_rerun()

# 결과 출력 단계 (말풍선)
elif st.session_state.step == len(questions) + 1:
    st.markdown(f"""
        <div style='padding:20px;'>
            <h2>🗨️ 진단 결과 요약</h2>
            <div style='background:#D1F2EB; padding:20px; border-radius:20px;'>
                <p><b>{st.session_state.user['name']}</b> 님의 건강 상태를 분석했어요!</p>
                <ul>
                    <li>📚 공부 시간: {st.session_state.answers.get("study_time")}</li>
                    <li>🏃 운동: {st.session_state.answers.get("exercise")}</li>
                    <li>🍽️ 식사: {st.session_state.answers.get("diet")}</li>
                    <li>😖 증상: {st.session_state.answers.get("symptom")}</li>
                    <li>🧍 자세: {st.session_state.answers.get("posture")}</li>
                </ul>
            </div>
        </div>
        <br>
        <center><button onclick="window.location.reload()">🔁 다시 시작하기</button></center>
    """, unsafe_allow_html=True)

    if st.button("📄 나의 보충 플랜카드 진단서 만들기"):
        st.session_state.step += 1

# 진단서 단계
elif st.session_state.step == len(questions) + 2:
    name = st.session_state.user['name']
    symptom = st.session_state.answers.get("symptom", "")
    diet = st.session_state.answers.get("diet", "")
    posture = st.session_state.answers.get("posture", "")

    symptom_tip = symptom_feedback.get(symptom, "")
    diet_tip = diet_feedback.get(diet, "")
    posture_tip = posture_feedback.get(posture, "")

    st.markdown(f"""
        <div style='background-image: linear-gradient(to bottom, #fffaf0, #fff0f5); padding:40px; border-radius:20px;'>
            <h1 style='text-align:center;'>📋 {name} 님의 보충 진단서</h1>
            <hr>
            <p><b>😖 증상:</b> {symptom}</p>
            <p><b>🩺 건강 조언:</b> {symptom_tip}</p>
            <p><b>🍱 식습관 피드백:</b> {diet_tip}</p>
            <p><b>📖 공부 자세 조언:</b> {posture_tip}</p>
            <p><b>🌈 추가 플랜:</b> 물 마시기 💧 / 스트레칭 🧘 / 충분한 수면 😴</p>
            <br>
            <p style='font-size:18px;'>🌟 <b>응원 메시지:</b> 오늘도 열심히 진단한 당신! 너무 멋져요 💖<br>
            계속 건강 지키면서 멋진 공부 습관 만들어가요! 화이팅! 🚀✨</p>
            <br><br>
            <p style='text-align:right;'>✔️ 스터디업 병원 공식 도장 🖋️</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><center><button onclick=\"window.location.reload()\">🔁 다시 시작하기</button></center>", unsafe_allow_html=True)
