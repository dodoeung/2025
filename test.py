# streamlit 앱: 학생 건강 진단서 생성기
import streamlit as st

st.set_page_config(page_title="스터디 업 건강 업 병원", page_icon="💉", layout="centered")

# 세션 상태 초기화
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# 질문 목록
def get_questions():
    return [
        {
            'key': 'study_time',
            'question': '하루에 얼마나 공부하나요? 📚⏰',
            'options': ['1시간 이하 💤', '1~3시간 🙂', '3~5시간 😅', '5시간 이상 🔥']
        },
        {
            'key': 'exercise',
            'question': '어떤 운동을 하나요? 🏃‍♂️🏋️‍♀️🧘‍♂️',
            'options': ['달리기 🏃‍♀️', '헬스 💪', '요가 🧘‍♀️', '운동 안 함 🙅‍♂️']
        },
        {
            'key': 'diet',
            'question': '주로 어떤 식사를 하나요? 🍚🥐🍜',
            'options': ['밥 🍚', '빵 🥐', '면 🍜', '간식 위주 🍫']
        },
        {
            'key': 'posture',
            'question': '공부할 때 어떤 자세인가요? 💺🪑',
            'options': ['바른 자세 👍', '구부정한 자세 😓', '누워서 😴']
        },
        {
            'key': 'symptoms',
            'question': '요즘 어떤 증상이 있나요? 🩺',
            'options': ['손목 저림 ✋', '어깨 결림 🧍‍♂️', '종아리 붓기 🦵', '눈 피로 👀', '두통 🤯', '허리통증 🧍‍♀️']
        },
    ]

questions = get_questions()

# 0단계: 유저 정보 입력
if st.session_state.step == 0:
    st.markdown("""
        <div style='text-align:center;'>
            <h1>🎉 스터디 업 건강 업 병원에 온 걸 환영해요! 🎉</h1>
            <p style='font-size:18px;'>건강 상태를 진단하고 맞춤 피드백을 받아보세요!</p>
        </div>
    """, unsafe_allow_html=True)

    with st.form("user_info_form"):
        name = st.text_input("이름")
        age = st.number_input("나이", min_value=6, max_value=25, step=1)
        grade = st.selectbox("학년", ['초등학생', '중학생', '고등학생'])
        gender = st.radio("성별", ['여자', '남자'])
        submitted = st.form_submit_button("진단 시작하기 🚀")

        if submitted:
            st.session_state.user_info = {
                'name': name,
                'age': age,
                'grade': grade,
                'gender': gender
            }
            st.session_state.step = 1
            st.rerun()

# 1~N단계: 질문 순차적으로 표시
elif 1 <= st.session_state.step <= len(questions):
    q = questions[st.session_state.step - 1]
    st.markdown(f"## ❓ {q['question']}")
    for opt in q['options']:
        if st.button(f"❤️ {opt}"):
            st.session_state.answers[q['key']] = opt
            st.session_state.step += 1
            st.rerun()

# 결과 출력
elif st.session_state.step == len(questions) + 1:
    name = st.session_state.user_info['name']
    st.markdown(f"""
    <div style='background-color:#FFF0F5;padding:20px;border-radius:10px;'>
        <h2 style='text-align:center;'>💬 {name}님의 건강 상태 진단 결과 💬</h2>
    </div>
    """, unsafe_allow_html=True)

    # 간단한 결과 요약
    result = []
    if '손목' in st.session_state.answers['symptoms']:
        result.append("📌 손목 스트레칭을 자주 해주세요.")
    if '구부정' in st.session_state.answers['posture']:
        result.append("📌 의자에 깊숙이 앉고 허리를 펴주세요.")
    if '간식' in st.session_state.answers['diet']:
        result.append("📌 식사는 균형 있게 챙기도록 해요!")

    for r in result:
        st.markdown(f"<div style='font-size:20px;'>💡 {r}</div>", unsafe_allow_html=True)

    if st.button("📄 진단서 확인하기"):
        st.session_state.step += 1
        st.rerun()

# 진단서 페이지
elif st.session_state.step == len(questions) + 2:
    user = st.session_state.user_info
    answers = st.session_state.answers

    st.markdown("""
    <div style='background-color:#fffef0;padding:30px;border:3px dashed #aaa;'>
        <h1 style='text-align:center;'>🩺 {}님의 건강 보충 진단서 🩺</h1>
        <hr>
        <pre style='font-family:"Courier New", monospace; font-size:16px;'>
이름: {name}
나이: {age}
학년: {grade}
성별: {gender}

[ 📚 생활 습관 요약 ]
- 공부 시간: {study_time}
- 운동: {exercise}
- 식사 습관: {diet}
- 공부 자세: {posture}
- 증상: {symptoms}

[ 💡 보충 팁 ]
{tips}

[ 🥕 추천 음식 & 스트레칭 ]
🍌 바나나, 🥦 브로콜리, 🥛 우유
🧘‍♀️ 목/어깨 스트레칭, 손목 돌리기

[ 🧑‍⚕️ 건강 조언 ]
- 너무 오래 앉아 있지 말고 자주 일어나세요
- 올바른 자세로 집중하면 더 효율이 올라가요!
- 항상 수분 섭취도 잊지 마세요 💧

도장: ✅ 진단 완료  
        </pre>
    </div>
    """.format(
        name=user['name'], age=user['age'], grade=user['grade'], gender=user['gender'],
        study_time=answers['study_time'],
        exercise=answers['exercise'],
        diet=answers['diet'],
        posture=answers['posture'],
        symptoms=answers['symptoms'],
        tips='\n'.join(result)
    ), unsafe_allow_html=True)

    st.success("🎉 진단이 완료되었습니다! 건강하게 공부하세요!")
    if st.button("🔁 다시 시작하기"):
        for key in ['step', 'user_info', 'answers']:
            del st.session_state[key]
        st.rerun()
