import streamlit as st

st.set_page_config(page_title="스터디 업 건강 업 병원", page_icon="💉", layout="centered")

# 상태 초기화
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# 질문과 선택지 (다양하게 확장)
questions = [
    {
        'key': 'study_time',
        'question': '하루에 얼마나 공부하나요? 📚⏰',
        'options': ['1시간 이하 💤', '1~3시간 🙂', '3~5시간 😅', '5시간 이상 🔥']
    },
    {
        'key': 'exercise',
        'question': '어떤 운동을 하나요? 🏃‍♂️🏋️‍♀️🧘‍♂️',
        'options': ['달리기 🏃‍♀️', '헬스 💪', '요가 🧘‍♀️', '수영 🏊‍♂️', '걷기 🚶‍♂️', '운동 안 함 🙅‍♂️']
    },
    {
        'key': 'diet',
        'question': '주로 어떤 식사를 하나요? 🍚🥐🍜',
        'options': ['밥 🍚', '빵 🥐', '면 🍜', '고기 🍗', '채소 🥦', '간식 위주 🍫']
    },
    {
        'key': 'posture',
        'question': '공부할 때 어떤 자세인가요? 💺🪑',
        'options': ['바른 자세 👍', '구부정한 자세 😓', '누워서 😴', '책상 앞에 엎드림 😵']
    },
    {
        'key': 'symptoms',
        'question': '요즘 어떤 증상이 있나요? 🩺',
        'options': ['손목 저림 ✋', '어깨 결림 🧍‍♂️', '종아리 붓기 🦵', '눈 피로 👀', '두통 🤯', '허리통증 🧍‍♀️', '목 통증 🦒']
    },
]

# 자세별 조언
posture_feedback = {
    '바른 자세 👍': "🪑 바른 자세를 유지하고 있어요! 아주 좋아요! 꾸준히 해주세요!",
    '구부정한 자세 😓': "💻 허리와 목이 아플 수 있으니, 바른 자세로 앉아보세요.",
    '누워서 😴': "📱 누워서 공부하면 집중력이 떨어지고 건강에 안 좋아요.절대 누워서 공부는 하지 마세요.!",
    '책상 앞에 엎드림 😵': "😵 너무 힘든 자세에요. 바른 자세를 권장해요!"
}

# 증상별 조언
symptom_feedback = {
    '손목 저림 ✋': "손목을 주물러 풀어주거나 천천히 돌리면서 스트레칭을 해주고 잠시 펜을 놓고 손의 휴식을 주세요.",
    '어깨 결림 🧍‍♂️': "어깨 돌리기와 스트레칭을 자주 해주세요.",
    '종아리 붓기 🦵': "가벼운 다리 스트레칭과 자주 일어나 걷기를 추천하고, 집에서는 폼롤러를 통해서 다리 붓기를 빼주면 좋을 것 같아요.",
    '눈 피로 👀': "20분마다 먼 곳을 바라보며 눈 휴식을 취하거나 초록나무를 보면서 눈을 정화해요.",
    '두통 🤯': "잠시 눈을 감고 1분동안 휴식을 취하고 수분 섭취가 중요해요.",
    '허리통증 🧍‍♀️': "올바른 자세와 허리 스트레칭을 해주세요.",
    '목 통증 🦒': "목을 오른쪽으로 한 바퀴 왼쪽으로 한바퀴 돌리면서 스트레칭하고 자세 교정을 권장해요."
}

# 식습관별 조언
diet_feedback = {
    '밥 🍚': "균형 잡힌 식사를 하려고 노력 중이네요! 좋아요! 하지만 많이 먹으면 안돼요!",
    '빵 🥐': "탄수화물이 많아요. 채소와 단백질도 챙기세요.",
    '면 🍜': "영양 불균형 주의! 밥과 채소도 섭취하세요.",
    '고기 🍗': "단백질은 좋지만 과도한 섭취는 조절이 필요해요.",
    '채소 🥦': "건강한 선택! 꾸준히 챙기면 좋아요.",
    '간식 위주 🍫': "간식은 줄이고 맛있는 밥이 들어간 식사를 잘 챙기도록 해요."
}

# 질문별 키를 가지고 답변에 맞게 결과 조합 함수
def generate_tips(answers):
    tips = []

    # 증상에 따른 팁
    symptom = answers.get('symptoms', '')
    if symptom in symptom_feedback:
        tips.append(f"🔹 증상 조언: {symptom_feedback[symptom]}")

    # 자세에 따른 팁
    posture = answers.get('posture', '')
    if posture in posture_feedback:
        tips.append(f"🔹 자세 조언: {posture_feedback[posture]}")

    # 식습관에 따른 팁
    diet = answers.get('diet', '')
    if diet in diet_feedback:
        tips.append(f"🔹 식습관 조언: {diet_feedback[diet]}")

    # 공부 시간에 따른 팁
    study_time = answers.get('study_time', '')
    if '1시간 이하' in study_time:
        tips.append("🔹 공부 시간: 조금 더 꾸준히 해보면 좋아요!")
    elif '5시간 이상' in study_time:
        tips.append("🔹 공부 시간: 너무 무리하지 말고 휴식도 챙기세요!")

    # 운동 여부
    exercise = answers.get('exercise', '')
    if '운동 안 함' in exercise:
        tips.append("🔹 운동: 가벼운 운동부터 시작해보세요!")

    if not tips:
        tips.append("👍 건강한 생활 습관을 잘 유지하고 있네요!")

    return "\n".join(tips)

# 0단계: 사용자 정보 입력
if st.session_state.step == 0:
    st.markdown("""
        <h1 style='text-align:center; color:#ff69b4;'>🎉 스터디 업 건강 업 병원에 온 걸 환영해요! 🎉</h1>
        <p style='text-align:center;'>귀엽고 친절하게 건강 상태를 진단해드립니다! 아래 정보를 입력해 주세요.</p>
    """, unsafe_allow_html=True)

    with st.form("user_form"):
        name = st.text_input("이름 ✏️")
        age = st.number_input("나이 🎂", min_value=6, max_value=25, step=1)
        grade = st.selectbox("학년 🎓", ['초등학생', '중학생', '고등학생'])
        gender = st.radio("성별 🚻", ['여자', '남자', '기타'])
        submit = st.form_submit_button("진단 시작하기 💖")

        if submit:
            if not name:
                st.warning("이름을 입력해주세요!")
            else:
                st.session_state.user_info = {
                    'name': name,
                    'age': age,
                    'grade': grade,
                    'gender': gender
                }
                st.session_state.step = 1
                st.rerun()

# 1~N단계: 질문 화면 (한 번에 하나씩)
elif 1 <= st.session_state.step <= len(questions):
    q = questions[st.session_state.step - 1]
    st.markdown(f"<h2 style='text-align:center; color:#ff69b4;'>❓ {q['question']}</h2>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; font-size:24px;'>💗💗💗💗💗</div>", unsafe_allow_html=True)

    for option in q['options']:
        if st.button(f"💖 {option}"):
            st.session_state.answers[q['key']] = option
            st.session_state.step += 1
            st.rerun()

# 결과 요약 (말풍선)
elif st.session_state.step == len(questions) + 1:
    user = st.session_state.user_info
    answers = st.session_state.answers
    tips = generate_tips(answers)

    st.markdown(f"""
    <div style='background:#D1F2EB; padding:30px; border-radius:30px; max-width:600px; margin:auto;'>
        <h2 style='text-align:center;'>💬 {user['name']}님의 건강 상태 진단 결과 💬</h2>
        <ul style='font-size:18px;'>
            <li>📚 공부 시간: {answers.get('study_time', '')}</li>
            <li>🏃 운동: {answers.get('exercise', '')}</li>
            <li>🍽️ 식사: {answers.get('diet', '')}</li>
            <li>🪑 공부 자세: {answers.get('posture', '')}</li>
            <li>🩺 증상: {answers.get('symptoms', '')}</li>
        </ul>
        <h3>💡 맞춤 건강 조언 💡</h3>
        <pre style='white-space: pre-wrap; font-size:16px;'>{tips}</pre>
    </div>
    """, unsafe_allow_html=True)

    if st.button("📄 나의 보충 플랜카드 진단서 보기"):
        st.session_state.step += 1
        st.rerun()

# 진단서 페이지
elif st.session_state.step == len(questions) + 2:
    user = st.session_state.user_info
    answers = st.session_state.answers
    tips = generate_tips(answers)

    st.markdown(f"""
    <div style="
        background-color:#fffaf0; 
        border: 3px dashed #aaa; 
        padding: 40px; 
        font-family: 'Courier New', monospace; 
        max-width: 700px; 
        margin:auto;
        box-shadow: 6px 6px 8px rgba(0,0,0,0.1);
        border-radius: 15px;
        position: relative;
    ">
        <h1 style="text-align:center; margin-bottom: 5px;">📋 {user['name']}님의 보충 진단서 📋</h1>
        <hr>
        <p><b>👧 이름:</b> {user['name']}  <b>🎂 나이:</b> {user['age']}세</p>
        <p><b>🎓 학년:</b> {user['grade']}  <b>🚻 성별:</b> {user['gender']}</p>
        <hr>
        <p><b>⏰ 공부 시간:</b> {answers.get('study_time', '')}</p>
        <p><b>🤸 운동 습관:</b> {answers.get('exercise', '')}</p>
        <p><b>🍽️ 식습관:</b> {answers.get('diet', '')}</p>
        <p><b>🪑 공부 자세:</b> {answers.get('posture', '')}</p>
        <p><b>💢 느끼는 증상:</b> {answers.get('symptoms', '')}</p>
        <hr>
        <h3>💡 건강 조언</h3>
        <pre style="white-space: pre-wrap; font-size:16px;">{tips}</pre>
        <hr>
        <h3>🥕 추천 음식 & 스트레칭</h3>
        <p>🍌 바나나, 🥦 브로콜리, 🥛 우유</p>
        <p>🧘‍♀️ 목/어깨 스트레칭, 손목 돌리기, 허리 펴기</p>
        <hr>
        <p style="text-align:right; font-size: 32px; color: red; font-weight:bold; user-select:none;">🖋️ 진단 완료 도장</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔁 다시 시작하기"):
        for key in ['step', 'user_info', 'answers']:
            del st.session_state[key]
        st.rerun()
