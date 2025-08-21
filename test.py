import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="스터디 업 건강 업 병원", page_icon="💉", layout="centered")

# --- CSS 스타일 ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gamja+Flower&display=swap');

body {
  background: linear-gradient(135deg, #fceabb 0%, #f8b500 100%);
  font-family: 'Gamja Flower', cursive;
  color: #4b2e83;
  margin: 0; padding: 0;
}

/* 전체 섹션 박스 스타일 */
.section-box {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 25px;
  padding: 30px 40px;
  max-width: 700px;
  margin: 30px auto;
  box-shadow: 0 8px 32px 0 rgba(255, 105, 180, 0.25);
  border: 3px solid #ff69b4;
  position: relative;
}

/* 제목 */
h1, h2, h3 {
  text-align: center;
  color: #d81e5b;
  text-shadow: 1px 1px 1px #ffb6c1;
  margin-bottom: 20px;
}

/* 큰 하트 버튼 스타일 */
.big-heart-btn {
  background-color: #ff69b4 !important;
  border-radius: 50px !important;
  font-size: 22px !important;
  padding: 15px 30px !important;
  margin: 10px !important;
  color: white !important;
  font-weight: bold !important;
  border: none !important;
  cursor: pointer !important;
  transition: transform 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 105, 180, 0.6);
}
.big-heart-btn:hover {
  background-color: #ff1493 !important;
  transform: scale(1.1);
}

/* 말풍선 스타일 */
.bubble {
  background: #ffb6c1;
  border-radius: 30px 30px 30px 0;
  padding: 25px 30px;
  max-width: 600px;
  margin: 40px auto;
  font-size: 20px;
  box-shadow: 3px 3px 15px rgba(255, 105, 180, 0.4);
  color: #4b2e83;
  position: relative;
  font-weight: 600;
}

/* 말풍선 꼬리 */
.bubble::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 20px;
  width: 0; height: 0;
  border: 15px solid transparent;
  border-top-color: #ffb6c1;
  border-bottom: 0;
  margin-left: -15px;
  margin-bottom: -15px;
}

/* 진단서 종이 배경 줄무늬 */
.paper-bg {
  background: repeating-linear-gradient(
    0deg,
    #fffaf0,
    #fffaf0 18px,
    #ffe4e1 18px,
    #ffe4e1 19px
  );
  border: 4px dashed #ff69b4;
  padding: 40px 50px;
  max-width: 700px;
  margin: 30px auto 50px;
  font-family: 'Courier New', monospace;
  box-shadow: 8px 8px 25px rgba(255, 20, 147, 0.2);
  border-radius: 20px;
  position: relative;
}

/* 진단서 제목 */
.diagnosis-title {
  text-align: center;
  font-size: 36px;
  margin-bottom: 5px;
  color: #d81e5b;
  text-shadow: 2px 2px 5px #ffb6c1;
}

/* 진단서 도장 */
.stamp {
  position: absolute;
  bottom: 30px;
  right: 30px;
  font-size: 60px;
  color: #ff1493;
  font-weight: bold;
  user-select: none;
  text-shadow: 1px 1px 3px #d81e5b;
}

/* 추천 음식 & 스트레칭 */
.recommend {
  font-size: 18px;
  margin-top: 15px;
  color: #a80055;
}

/* 리스트 아이템 이모지 */
ul li {
  margin-bottom: 10px;
  font-weight: 600;
}

/* 입력폼 스타일 */
input[type="text"], input[type="number"], select {
  border-radius: 15px;
  border: 2px solid #ff69b4;
  padding: 8px 15px;
  font-size: 18px;
  color: #4b2e83;
  font-weight: 600;
  margin-bottom: 15px;
  width: 100%;
  box-sizing: border-box;
}

form > div {
  margin-bottom: 15px;
}

/* 성별 라디오 버튼 꾸미기 */
input[type="radio"] {
  margin-right: 10px;
  accent-color: #ff1493;
}

/* 다시 시작 버튼 */
.restart-btn {
  background-color: #ff1493 !important;
  border-radius: 50px !important;
  font-size: 20px !important;
  padding: 12px 25px !important;
  margin: 30px auto 50px;
  color: white !important;
  font-weight: bold !important;
  border: none !important;
  cursor: pointer !important;
  display: block;
  box-shadow: 0 5px 20px rgba(255, 20, 147, 0.5);
  transition: transform 0.3s ease;
}
.restart-btn:hover {
  transform: scale(1.1);
}
</style>
""", unsafe_allow_html=True)

# 상태 초기화
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# 질문과 선택지 (확장된 이모지 포함)
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

# 조언 데이터
posture_feedback = {
    '바른 자세 👍': "🪑 바른 자세를 유지하고 있어요! 아주 좋아요! 꾸준히 해주세요!",
    '구부정한 자세 😓': "💻 허리와 목이 아플 수 있으니, 바른 자세로 앉아보세요.",
    '누워서 😴': "📱 누워서 공부하면 집중력이 떨어지고 건강에 안 좋아요. 절대 누워서 공부는 하지 마세요!",
    '책상 앞에 엎드림 😵': "😵 너무 힘든 자세에요. 바른 자세를 권장해요!"
}
symptom_feedback = {
    '손목 저림 ✋': "손목을 주물러 풀어주거나 천천히 돌리면서 스트레칭을 해주고 잠시 펜을 놓고 손의 휴식을 주세요.",
    '어깨 결림 🧍‍♂️': "어깨 돌리기와 스트레칭을 자주 해주세요.",
    '종아리 붓기 🦵': "가벼운 다리 스트레칭과 자주 일어나 걷기를 추천하고, 집에서는 폼롤러를 통해서 다리 붓기를 빼주면 좋을 것 같아요.",
    '눈 피로 👀': "20분마다 먼 곳을 바라보며 눈 휴식을 취하거나 초록나무를 보면서 눈을 정화해요.",
    '두통 🤯': "잠시 눈을 감고 1분동안 휴식을 취하고 수분 섭취가 중요해요.",
    '허리통증 🧍‍♀️': "올바른 자세와 허리 스트레칭을 해주세요.",
    '목 통증 🦒': "목을 오른쪽으로 한 바퀴 왼쪽으로 한바퀴 돌리면서 스트레칭하고 자세 교정을 권장해요."
}
diet_feedback = {
    '밥 🍚': "균형 잡힌 식사를 하려고 노력 중이네요! 좋아요! 하지만 많이 먹으면 안돼요!",
    '빵 🥐': "탄수화물이 많아요. 채소와 단백질도 챙기세요.",
    '면 🍜': "영양 불균형 주의! 밥과 채소도 섭취하세요.",
    '고기 🍗': "단백질은 좋지만 과도한 섭취는 조절이 필요해요.",
    '채소 🥦': "건강한 선택! 꾸준히 챙기면 좋아요.",
    '간식 위주 🍫': "간식은 줄이고 맛있는 밥이 들어간 식사를 잘 챙기도록 해요."
}

# 결과 팁 생성 함수
def generate_tips(answers):
    tips = []

    symptom = answers.get('symptoms', '')
    if symptom in symptom_feedback:
        tips.append(f"🔹 증상 조언: {symptom_feedback[symptom]}")

    posture = answers.get('posture', '')
    if posture in posture_feedback:
        tips.append(f"🔹 자세 조언: {posture_feedback[posture]}")

    diet = answers.get('diet', '')
    if diet in diet_feedback:
        tips.append(f"🔹 식습관 조언: {diet_feedback[diet]}")

    study_time = answers.get('study_time', '')
    if '1시간 이하' in study_time:
        tips.append("🔹 공부 시간: 조금 더 꾸준히 해보면 좋아요!")
    elif '5시간 이상' in study_time:
        tips.append("🔹 공부 시간: 너무 무리하지 말고 휴식도 챙기세요!")

    exercise = answers.get('exercise', '')
    if '운동 안 함' in exercise:
        tips.append("🔹 운동: 가벼운 운동부터 시작해보세요!")

    # 공부 자세 조언 & 격려
    tips.append("\n💡 추가 조언:")
    tips.append("📌 공부할 때는 바른 자세를 유지하고, 50분 공부 후 10분 휴식을 꼭 챙기세요! 😉")
    tips.append("💪 힘들어도 조금씩 꾸준히 하면 건강과 성적 모두 챙길 수 있어요! 화이팅! 🎉")

    return "\n".join(tips)

# --- 앱 단계별 UI ---

# 0단계: 사용자 정보 입력
if st.session_state.step == 0:
    st.markdown("""
        <div class="section-box">
        <h1>🎉 스터디 업 건강 업 병원에 온 걸 환영해요! 🎉</h1>
        <p style="text-align:center; font-size:18px; color:#d81e5b;">귀엽고 친절하게 건강 상태를 진단해드립니다! 아래 정보를 입력해 주세요.</p>
        </div>
    """, unsafe_allow_html=True)

    with st.form("user_form", clear_on_submit=False):
        name = st.text_input("이름 ✏️")
        age = st.number_input("나이 🎂", min_value=6, max_value=25, step=1)
        grade = st.selectbox("학년 🎓", ['초등학생', '중학생', '고등학생'])
        gender = st.radio("성별 🚻", ['여자', '남자', '기타'])
        submit = st.form_submit_button("진단 시작하기 💖")

        if submit:
            if not name.strip():
                st.warning("이름을 입력해주세요!")
            else:
                st.session_state.user_info = {
                    'name': name.strip(),
                    'age': age,
                    'grade': grade,
                    'gender': gender
                }
                st.session_state.step = 1
                st.experimental_rerun()

# 1~N단계: 질문 하나씩 (하트 모양 버튼)
elif 1 <= st.session_state.step <= len(questions):
    q = questions[st.session_state.step - 1]
    st.markdown(f"""
    <div class="section-box">
    <h2>❓ {q['question']}</h2>
    <div style="text-align:center; font-size: 30px; margin-bottom: 20px;">💗💗💗💗💗</div>
    """, unsafe_allow_html=True)

    cols = st.columns(len(q['options']))
    for i, option in enumerate(q['options']):
        if cols[i].button(f"💖 {option}", key=f"{q['key']}_{option}"):
            st.session_state.answers[q['key']] = option
            st.session_state.step += 1
            st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# 결과 말풍선 페이지
elif st.session_state.step == len(questions) + 1:
    user = st.session_state.user_info
    answers = st.session_state.answers
    tips = generate_tips(answers)

    st.markdown(f"""
    <div class="bubble">
        💬 {user['name']}님의 건강 상태 진단 결과를 알려드려요!<br><br>
        <ul>
            <li>📚 공부 시간: {answers.get('study_time', '')}</li>
            <li>🏃 운동: {answers.get('exercise', '')}</li>
            <li>🍽️ 식사: {answers.get('diet', '')}</li>
            <li>🪑 공부 자세: {answers.get('posture', '')}</li>
            <li>🩺 증상: {answers.get('symptoms', '')}</li>
        </ul>
        <br>
        <pre style="white-space: pre-wrap; font-size:18px;">{tips}</pre>
    </div>
    """, unsafe_allow_html=True)

    if st.button("📄 나의 보충 플랜카드 진단서 보기"):
        st.session_state.step += 1
        st.experimental_rerun()

# 진단서 페이지 (줄무늬 종이 + 도장 + 귀여운 이모지 + 컬러풀)
elif st.session_state.step == len(questions) + 2:
    user = st.session_state.user_info
    answers = st.session_state.answers
    tips = generate_tips(answers)

    st.markdown(f"""
    <div class="paper-bg">
        <h1 class="diagnosis-title">📋 {user['name']}님의 보충 진단서 📋</h1>
        <hr>
        <p><b>👧 이름:</b> {user['name']}  &nbsp;&nbsp; <b>🎂 나이:</b> {user['age']}세</p>
        <p><b>🎓 학년:</b> {user['grade']}  &nbsp;&nbsp; <b>🚻 성별:</b> {user['gender']}</p>
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
        <p class="recommend">🍌 바나나, 🥦 브로콜리, 🥛 우유</p>
        <p class="recommend">🧘‍♀️ 목/어깨 스트레칭, 손목 돌리기, 허리
