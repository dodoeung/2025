import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io, textwrap, random, datetime

# --------- 초기 설정 ----------
st.set_page_config(page_title="학생 건강 진단 & 보충 플랜카드 💖", page_icon="🩺", layout="wide")

# --------- 스타일 ----------
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg,#FFF0F6 0%,#E7F5FF 55%,#FFF9DB 100%);}
.glass {background: rgba(255,255,255,0.65); backdrop-filter: blur(8px); border: 1px solid rgba(255,255,255,0.6); box-shadow:0 8px 30px rgba(0,0,0,0.08); border-radius:24px; padding:1.2rem 1.4rem;}
.tag {display:inline-block;padding:.25rem .6rem;margin:.15rem .25rem;border-radius:999px;font-size:.85rem;background:#fff;border:1px solid rgba(0,0,0,.06);}
.pill {background:#09090b; color:#fff; border-radius:999px; padding:.35rem .7rem; font-size:.8rem;}
.title-emoji { font-size:2rem; }
</style>
""", unsafe_allow_html=True)

def section_card(title, body, emoji="✨"):
    st.markdown(f"""
    <div class='glass'>
        <div style="display:flex;align-items:center;gap:.5rem;margin-bottom:.35rem;">
            <span class="title-emoji">{emoji}</span>
            <h4 style="margin:0">{title}</h4>
        </div>
        <div style="font-size:1rem;line-height:1.5">{body}</div>
    </div>
    """, unsafe_allow_html=True)

# --------- 세션 초기화 ----------
if "step" not in st.session_state: st.session_state.step = 1

# --------- 데이터 ----------
EX_TYPES = ["🏃 달리기", "🏋️ 헬스", "🧘 요가/스트레칭", "🚴‍♂️ 자전거", "🏊 수영", "⚽ 구기", "⛰️ 등산", "💃 댄스", "기타"]
SYMPTOMS = ["✋ 손목 저림","🦵 종아리 붓기","👀 눈의 피로","🧠 두통","🪑 허리 통증","💪 어깨 결림","🦵 무릎 통증","🖐 손발 저림","😴 불면","😣 집중력 저하","피로감 지속","없음"]
MEAL_PATTERNS = ["불규칙(1끼 이하)","하루 2끼","하루 3끼","간식 위주","인스턴트/패스트푸드"]

FEEDBACK_POOLS = {
    "✋ 손목 저림": ["손목 스트레칭 1~2시간마다 1분","타이핑/필기 45~50분 쉬기","손목 보호대 고려","손목/팔꿈치 높이 맞추기"],
    "🦵 종아리 붓기": ["다리 벽에 10분 올리기","수분 섭취","1시간마다 걷기/까치발","종아리 마사지/스트레칭"],
    "👀 눈의 피로": ["20-20-20 규칙","화면 밝기/거리/각도 조절","블루라이트 차단","눈 마사지/인공눈물"],
    "🧠 두통": ["수분 섭취 늘리기","조명·소음 조절","목/어깨 스트레칭","카페인 줄이기"],
    "💪 어깨 결림": ["어깨 돌리기/승모근 스트레칭","책상 높이·모니터 위치 재조정","찜질로 근육 완화","탄력 밴드 운동"],
    "🪑 허리 통증": ["등받이에 등을 붙이고 앉기","1시간마다 후방 신전 스트레칭","허리 쿠션 사용","복부 코어 강화 운동"],
    "🦵 무릎 통증": ["계단·점프 줄이기","충격 흡수 신발","벽 스쿼트 깊이 낮추기","얼음찜질"],
    "😣 집중력 저하": ["포모도로(25분 집중+5분 휴식)","장소·시간대 변경","수분 섭취 늘리기","운동으로 혈류 올리기"],
    "😴 불면": ["취침 1시간 전 화면 줄이기","수면 루틴 일정","카페인 오후 피하기","저강도 스트레칭/명상"],
    "피로감 지속": ["수면 7~8시간 확보","단백질·채소 섭취 늘리기","공부 블록 나누기","가벼운 유산소 운동"],
    "🪶 목 통증": ["화면 눈높이 50~70cm","턱 당기기/측굴 스트레칭","스마트폰 고개 숙임 줄이기","찜질"],
    "🖐 손발 저림": ["자세 교정","스트레칭/손 쥐기·펴기","조이는 신발/밴드 피하기","수분·전해질 유지"]
}

def pick_feedback(symptom_list,k_each=2,max_total=8):
    tips=[]
    for s in symptom_list:
        if s in FEEDBACK_POOLS:
            pool=FEEDBACK_POOLS[s][:]
            random.shuffle(pool)
            tips.extend(pool[:k_each])
    dedup=[]
    for t in tips:
        if t not in dedup: dedup.append(t)
    return dedup[:max_total]

def compute_score(answers):
    score=100
    stime=answers["study_time"]
    if stime=="9시간 이상": score-=15
    elif stime=="2시간 이하": score-=5
    if answers["exercise_freq"]=="전혀 안 함": score-=15
    elif answers["exercise_freq"]=="가끔(주1~2회)": score-=5
    meals=answers["meals"]
    if meals=="불규칙(1끼 이하)": score-=15
    elif meals=="하루 2끼": score-=5
    if "간식 위주" in answers["diet_flags"]: score-=5
    if "인스턴트/패스트푸드" in answers["diet_flags"]: score-=8
    if answers["posture"] in ["허리 굽힘","고개 숙임","다리 꼬고 앉음"]: score-=10
    syms=answers["symptoms"]
    penalties={"🧠 두통":10,"👀 눈의 피로":10,"🪑 허리 통증":10,"✋ 손목 저림":10,"🦵 무릎 통증":8,"🪶 목 통증":7,"💪 어깨 결림":6,"🦵 종아리 붓기":6,"😣 집중력 저하":5,"😴 불면":7,"피로감 지속":7,"🖐 손발 저림":6}
    for s in syms: score-=penalties.get(s,0)
    score=max(0,min(100,score))
    if score>=80: cat="매우 좋음"
    elif score>=60: cat="보통"
    else: cat="주의 필요"
    return score,cat

# --------- STEP 1: 처음 화면 ----------
if st.session_state.step==1:
    st.markdown("""
    <h1 style='text-align:center; font-size:2.2rem;'>📚 스터디 업, 건강 업 🏥<br>병원에 온 걸 환영해요! 🎉</h1>
    <p style='text-align:center; font-size:1.1rem;'>여러분의 건강 상태를 체크하고, 나만의 보충 플랜을 만들어 볼까요? 🧸🍎🏃‍♂️</p>
    """, unsafe_allow_html=True)
    if st.button("✨ 진단 시작하기 ✨", use_container_width=True):
        st.session_state.step=2

# --------- STEP 2: 정보/습관/증상 입력 ----------
elif st.session_state.step==2:
    st.markdown("### 👤 기본 정보 입력")
    col1,col2=st.columns([1.2,1])
    with col1:
        name=st.text_input("이름",placeholder="이름을 입력하세요")
        age=st.number_input("나이",10,30,16)
        gender=st.radio("성별",["남","여","선택 안 함"],horizontal=True)
        grade=st.selectbox("학년",["중학생","고등학생","대학생"])
    with col2:
        section_card("Tip","솔직하게 입력하면 더 정확해요! 😄","💡")
    st.markdown("---")
    if st.button("다음 단계 ▶",use_container_width=True):
        st.session_state.name=name.strip() if name else "익명"
        st.session_state.age=age
        st.session_state.gender=gender
        st.session_state.grade=grade
        st.session_state.step=3

# --------- STEP 3: 생활습관 & 증상 ----------
elif st.session_state.step==3:
    st.markdown("### 📋 생활 습관 & 증상 선택")
    c1,c2=st.columns(2)
    with c1:
        study_time=st.radio("오늘 공부 시간은?", ["2시간 이하","3~5시간","6~8시간","9시간 이상"])
        exercise_freq=st.radio("운동 빈도는?",["전혀 안 함","가끔(주1~2회)","자주(주3회 이상)"])
        exercise_types=st.multiselect("주로 하는 운동",EX_TYPES)
        meals=st.radio("식사 습관",MEAL_PATTERNS[:3])
        diet_flags=st.multiselect("추가 식습관",MEAL_PATTERNS[3:])
    with c2:
        posture=st.radio("공부 자세",["바른 자세","허리 굽힘","고개 숙임","다리 꼬고 앉음","자주 움직임"])
        symptoms=st.multiselect("공부 중/후 느끼는 이상",SYMPTOMS,default=[])
    st.markdown("---")
    if st.button("🔍 결과 확인하기",use_container_width=True):
        st.session_state.answers={"study_time":study_time,"exercise_freq":exercise_freq,"exercise_types":exercise_types,"meals":meals,"diet_flags":diet_flags,"posture":posture,"symptoms":[s for s in symptoms if s!="없음"]}
        st.session_state.step=4

# --------- STEP 4: 결과 + 진단서 생성 ----------
elif st.session_state.step==4:
    answers=st.session_state.answers
    score,category=compute_score(answers)
    emoji="😍" if category=="매우 좋음" else "🙂" if category=="보통" else "😥"
    st.markdown(f"<h2 style='text-align:center;'>🩺 {st.session_state.name}의 보충 진단서 ({emoji})</h2>",unsafe_allow_html=True)
    st.markdown(f"**점수/상태:** {score}점 / {category}")
    tips=pick_feedback(answers["symptoms"]) if answers["symptoms"] else ["수분 섭취","수면 루틴","가벼운 운동"]
    st.markdown("### 맞춤 조언/충고 📝")
    for t in tips: st.markdown(f"• {t}")

    # PNG 다운로드
    def render_certificate_png():
        W,H=900,1300
        img=Image.new("RGB",(W,H),(255,252,248))
        draw=ImageDraw.Draw(img)
        card_pad=40
        draw.rounded_rectangle([card_pad,card_pad,W-card_pad,H-card_pad],radius=36,fill=(255,255,255),outline=(230,230,230),width=3)
        title=ImageFont.load_default()
        body=ImageFont.load_default()
        y=70
        draw.text((60,y),f"{st.session_state.name}의 보충 진단서 ({datetime.date.today()})",font=title,fill=(30,30,30))
        y+=30; draw.line([(60,y),(W-60,y)],fill=(230,230,230),width=2); y+=20
        draw.text((60,y),f"점수/상태: {score}점 / {category}",font=body,fill=(40,40,40))
        y+=32
        summary=[f"공부: {answers['study_time']}",f"운동: {answers['exercise_freq']} / {', '.join(answers['exercise_types']) if answers['exercise_types'] else '선택 없음'}",f"식사: {answers['meals']} {', '.join(answers['diet_flags']) if answers['diet_flags'] else ''}",f"자세: {answers['posture']}",f"증상: {', '.join(answers['symptoms']) if answers['symptoms'] else '없음'}"]
        for line in summary: draw.text((60,y),line,font=body,fill=(50,50,50)); y+=22
        y+=12; draw.line([(60,y),(W-60,y)],fill=(235,235,235),width=1); y+=18
        rec_food="추천 음식: 단백질, 채소/과일, 통곡물, 견과류, 물 자주"
        rec_ex="추천 운동: 걷기·스트레칭 10~15분/일, 주 2~3회 가벼운 근력·유산소 혼합"
        for para in [rec_food,rec_ex]:
            for t in textwrap.wrap(para,48):
                draw.text((60,y),t,font=body,fill=(60,60,60)); y+=22
            y+=6
        y+=6; draw.text((60,y),"맞춤 조언/충고:",font=title,fill=(30,30,30)); y+=26
        for tip in tips:
            for t in textwrap.wrap("• "+tip,54): draw.text((80,y),t,font=body,fill=(55,55,55)); y+=22
            y+=2
        bio=io.BytesIO(); img.save(bio,format="PNG"); bio.seek(0); return bio

    png_bytes=render_certificate_png()
    st.download_button("🖼️ 진단서 PNG 다운로드",data=png_bytes,file_name="my_health_plan_card.png",mime="image/png",use_container_width=True)

    st.markdown("---")
    c1,c2=st.columns(2)
    with c1: 
        if st.button("⬅️ 결과 수정하기"): st.session_state.step=3
    with c2: 
        if st.button("🔄 처음으로"): st.session_state.step=1
