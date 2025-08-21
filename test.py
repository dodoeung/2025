import streamlit as st

# ----------------------------- 앱 기본 설정 -----------------------------
st.set_page_config(page_title="스터디 업 건강 업 병원", page_icon="🩺", layout="centered")

st.markdown("""
    <style>
    .title {
        font-size: 32px;
        font-weight: bold;
        color: #ff69b4;
        text-align: center;
    }
    .question-box {
        background-color: #fff0f5;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    .heart-button {
        display: inline-block;
        background-color: #ffe6ea;
        color: #d6336c;
        border-radius: 30px;
        padding: 10px 25px;
        margin: 10px;
        font-size: 20px;
        font-weight: bold;
        border: 2px solid #d6336c;
        cursor: pointer;
    }
    .chat-bubble {
        background: #fff0f5;
        border-radius: 20px;
        padding: 20px;
        font-size: 20px;
        color: #333;
        width: 100%;
        max-width: 500px;
        margin: auto;
        margin-bottom: 30px;
    }
    .paper {
        background-image: linear-gradient(to bottom, #fff, #fff), 
                          repeating-linear-gradient(to bottom, transparent, transparent 29px, #ccc 30px);
        background-size: 100% 30px;
        padding: 40px;
        border: 2px solid #ccc;
        border-radius: 15px;
        font-family: 'Comic Sans MS', cursive;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------- 질문 리스트 -----------------------------
questions = [
    {
        "question": "공부는 하루에 몇 시간 하나요?",
        "key": "study_time",
        "options": ["⏰ 1~2시간", "📘 3~4시간", "📚 5시간 이상"]
    },
    {
        "question": "운동은 얼마나 하나요?",
        "key": "exercise",
        "options": ["🏃 거의 안 함", "🤸 일주일 1~2회", "💪 자주 함"]
    },
    {
        "question": "요즘 자세는 어떤가요?",
        "key": "posture",
        "options": ["🪑 바른 자세 유지", "💻 구부정한 자세", "📱 누워서 공부"]
    },
    {
        "question": "공부할 때 어떤 이상을 느끼나요?",
        "key": "symptom",
        "options": ["🖐️ 손목 통증", "🦵 종아리 붓기", "👀 눈 피로", "😴 졸림"]
    },
    {
        "question": "요즘 주로 어떤 음식을 많이 먹나요?",
        "key": "meal_detail",
        "options": [
            "🍞 빵 위주로 먹어요", "🍜 면 종류를 자주 먹어요", "🍚 밥 위주로 먹어요",
            "🍗 고기를 많이 먹어요", "🥬 채소를 잘 챙겨 먹어요", "🍭 군것질을 자주 해요",
            "🥤 탄산, 당류가 많아요", "🍱 골고루 먹으려고 해요"
        ]
    }
]

# ----------------------------- 피드백 데이터 -----------------------------
symptom_feedback = {
    "🖐️ 손목 통증": "💡 손목 스트레칭을 해주고, 손목 받침대를 써보세요!",
    "🦵 종아리 붓기": "🦵 오래 앉아있지 말고 틈틈이 다리 스트레칭 해보세요!",
    "👀 눈 피로": "👀 눈을 자주 깜빡이고, 20분마다 먼 곳을 보며 쉬어주세요!",
    "😴 졸림": "😴 충분한 수면과 규칙적인 식사를 챙겨주세요!"
}
meal_feedback = {
    "🍞 빵 위주로 먹어요": "🥖 빵만 먹으면 영양 불균형! 단백질/채소 보충 필요해요.",
    "🍜 면 종류를 자주 먹어요": "🍜 나트륨 섭취 주의! 국물은 남기고, 과일도 곁들여요.",
    "🍚 밥 위주로 먹어요": "🍚 좋은 식단이에요! 반찬 다양하게 곁들이면 최고!",
    "🍗 고기를 많이 먹어요": "🍗 단백질 OK! 채소도 같이 먹어줘요 🥦",
    "🥬 채소를 잘 챙겨 먹어요": "🥬 좋아요! 탄수화물도 너무 적지 않게 챙겨요.",
    "🍭 군것질을 자주 해요": "🍭 간식은 줄이고 식사를 잘 챙겨보아요!",
    "🥤 탄산, 당류가 많아요": "🥤 당 섭취 줄이기! 물과 과일로 대체해요.",
    "🍱 골고루 먹으려고 해요": "🍱 훌륭해요! 지금처럼 유지하면 좋아요!"
}
posture_feedback = {
    "🪑 바른 자세 유지": "🪑 바른 자세 최고! 지금처럼 유지해요!",
    "💻 구부정한 자세": "💻 등과 목에 무리 가요! 바른 자세로 허리를 펴 보세요!",
    "📱 누워서 공부": "📱 누워서 공부는 집중력 저하와 건강에 안 좋아요! 책상에 앉아서 해요!"
}

# ----------------------------- 상태 관리 -----------------------------
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = {}

# ----------------------------- 페이지 구성 -----------------------------
if st.session_state.step == 0:
    st.markdown("<div class='title'>🏥 스터디 업 건강 업 병원에 온 걸 환영해요!</div>", unsafe_allow_html=True)
    name = st.text_input("이름을 입력해주세요 ✏️")
    if name:
        st.session_state.answers["name"] = name
        if st.button("✅ 진단 시작하기"):
            st.session_state.step += 1

elif 1 <= st.session_state.step <= len(questions):
    q = questions[st.session_state.step - 1]
    st.markdown(f"<div class='question-box'><h3>{q['question']}</h3></div>", unsafe_allow_html=True)
    for option in q["options"]:
        if st.button(option):
            st.session_state.answers[q["key"]] = option
            st.session_state.step += 1

elif st.session_state.step == len(questions) + 1:
    st.markdown("<div class='chat-bubble'>🎉 진단 결과가 나왔어요! <br> 아래 버튼을 눌러 진단서를 확인해 보세요!</div>", unsafe_allow_html=True)
    if st.button("📄 나의 보충 플랜카드 진단서 보기"):
        st.session_state.step += 1

elif st.session_state.step == len(questions) + 2:
    name = st.session_state.answers.get("name", "")
    symptom = st.session_state.answers.get("symptom", "")
    meal_detail = st.session_state.answers.get("meal_detail", "")
    posture = st.session_state.answers.get("posture", "")

    st.markdown(f"<h2 style='text-align:center;'>🩺 {name}님의 보충 진단서</h2>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="paper">
    📌 <b>증상:</b> {symptom}<br>
    🩺 <b>건강 조언:</b> {symptom_feedback.get(symptom, '')}<br><br>
    🍽️ <b>식습관 피드백:</b> {meal_feedback.get(meal_detail, '')}<br><br>
    📖 <b>공부 자세 조언:</b> {posture_feedback.get(posture, '')}<br><br>
    🧘 <b>추천 스트레칭:</b> 가볍게 목 돌리기, 손목 풀기, 다리 들기 운동!<br>
    🪑 <b>올바른 자세:</b> 허리를 곧게 펴고 발을 바닥에 붙여 앉아요.<br><br>
    🌟 <b>응원 메시지:</b> 오늘도 진단한 너는 최고야! 💖<br>
    계속 건강 지키면서 멋진 습관 만들어가요! 화이팅! 🚀<br><br>
    🔖 <b>도장:</b> ✅ 건강 챙김 인증 완료!
    </div>
    """, unsafe_allow_html=True)
