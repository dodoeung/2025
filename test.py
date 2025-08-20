# app.py
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io, textwrap, random, datetime

# --------- 초기 설정 ----------
st.set_page_config(page_title="학생 건강 진단 & 보충 플랜카드 💖", page_icon="🩺", layout="wide")

# --------- 스타일 유틸 ----------
def set_background_by_category(category:str):
    # 결과 상태에 따라 배경(그라디언트 & 패턴) 바꾸기
    if category == "매우 좋음":
        grad = "linear-gradient(135deg, #FFE8F3 0%, #E7F5FF 55%, #FFF9DB 100%)"
        deco = """
            radial-gradient(#ffd6e7 2px, transparent 2px),
            radial-gradient(#d6f4ff 2px, transparent 2px),
            radial-gradient(#fff1b8 2px, transparent 2px)
        """
    elif category == "보통":
        grad = "linear-gradient(135deg, #EDE7FF 0%, #EAF7F1 55%, #FFF1E6 100%)"
        deco = """
            radial-gradient(#cdbdff 2px, transparent 2px),
            radial-gradient(#b9f7d0 2px, transparent 2px),
            radial-gradient(#ffd8b2 2px, transparent 2px)
        """
    else:  # 주의 필요
        grad = "linear-gradient(135deg, #FFE3E3 0%, #FFF0F6 55%, #FFF7E6 100%)"
        deco = """
            radial-gradient(#ffa8a8 2px, transparent 2px),
            radial-gradient(#ffc9de 2px, transparent 2px),
            radial-gradient(#ffd8a8 2px, transparent 2px)
        """
    st.markdown(f"""
    <style>
    .stApp {{
        background: {deco}, {grad};
        background-size: 24px 24px, 28px 28px, 32px 32px, cover;
        background-attachment: fixed;
    }}
    .glass {{
        background: rgba(255,255,255,0.65);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.6);
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        border-radius: 24px;
        padding: 1.2rem 1.4rem;
    }}
    .tag {{
        display:inline-block;padding:.25rem .6rem;margin:.15rem .25rem;border-radius:999px;
        font-size:.85rem;background:#fff;border:1px solid rgba(0,0,0,.06)
    }}
    .pill {{
        background:#09090b; color:#fff; border-radius:999px; padding:.35rem .7rem; font-size:.8rem;
    }}
    .title-emoji {{ font-size: 2rem; }}
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

# --------- 세션 스텝 ----------
if "step" not in st.session_state:
    st.session_state.step = 1

# --------- 데이터 사전 ----------
EX_TYPES = ["달리기", "헬스(근력)", "요가/스트레칭", "자전거", "수영", "구기(축구/농구)", "등산", "댄스", "기타"]
SYMPTOMS = [
    "어깨 결림","목 통증","두통","눈의 피로","집중력 저하","허리 통증",
    "손목 저림","종아리 붓기","무릎 통증","손발 저림","불면","피로감 지속","없음"
]
MEAL_PATTERNS = ["불규칙(하루 1끼 이하)","하루 2끼","하루 3끼 규칙적","간식 위주","인스턴트/패스트푸드가 많음"]

# 증상별 피드백 풀(다양성)
FEEDBACK_POOLS = {
    "손목 저림": [
        "손목 스트레칭을 1~2시간마다 1분씩 해주세요.",
        "타이핑/필기 45~50분마다 손목을 쉬게 하세요.",
        "손목 보호대 착용을 고려해보세요.",
        "손목과 팔꿈치의 높이를 맞추고 손목 꺾임을 줄여주세요."
    ],
    "종아리 붓기": [
        "잠깐 누워 다리를 벽에 10분 올려보세요.",
        "물을 조금씩 자주 마시면 순환에 도움돼요.",
        "1시간마다 3~5분 걷거나 까치발 들기 운동을 해보세요.",
        "종아리 마사지와 종아리 스트레칭을 해보세요."
    ],
    "눈의 피로": [
        "20-20-20 규칙(20분마다 20초간 먼 곳 보기)을 실천하세요.",
        "화면 밝기/거리/각도를 조정하세요.",
        "블루라이트 차단 기능을 활용해보세요.",
        "눈꺼풀 마사지와 인공눈물을 고려해보세요."
    ],
    "두통": [
        "수분 섭취를 늘리고 조용한 공간에서 10분 쉬어보세요.",
        "조명 밝기와 소음을 조절하세요.",
        "목/어깨 스트레칭으로 긴장을 풀어주세요.",
        "카페인 과다 섭취를 줄여보세요."
    ],
    "어깨 결림": [
        "어깨 돌리기·승모근 스트레칭을 수시로 하세요.",
        "책상 높이와 모니터 위치를 재조정하세요.",
        "따뜻한 찜질로 근육 긴장을 완화하세요.",
        "가벼운 탄력 밴드 운동을 해보세요."
    ],
    "허리 통증": [
        "등받이에 등을 붙이고 허리를 세워 앉으세요.",
        "1시간마다 일어나서 후방 신전 스트레칭을 하세요.",
        "허리 쿠션(요추 지지)을 사용해보세요.",
        "복부 코어 강화 운동을 주 3회 해보세요."
    ],
    "무릎 통증": [
        "계단·점프는 줄이고, 준비운동/마무리 스트레칭을 강화하세요.",
        "런닝 시 충격 흡수 되는 신발을 사용하세요.",
        "벽에 기대어 스쿼트는 깊이 낮춰 가볍게 시행하세요.",
        "얼음찜질로 염증을 관리하세요."
    ],
    "집중력 저하": [
        "포모도로(25분 집중 + 5분 휴식)를 사용해보세요.",
        "공부 장소·시간대를 바꿔 자극을 전환해보세요.",
        "수분 섭취를 늘리고 과한 당분은 줄여보세요.",
        "운동으로 뇌 혈류를 올려보세요(걷기 10분도 좋아요)."
    ],
    "불면": [
        "취침 1시간 전 화면 사용을 줄이세요.",
        "수면 시간·기상 시간을 규칙적으로 유지하세요.",
        "카페인을 오후엔 피하세요.",
        "저강도 스트레칭/명상으로 긴장을 낮추세요."
    ],
    "피로감 지속": [
        "수면 시간이 7~8시간 되는지 점검해보세요.",
        "단백질과 채소 섭취를 늘리세요.",
        "학습 시간을 블록으로 쪼개 휴식 밀도를 높이세요.",
        "가벼운 유산소로 컨디션을 끌어올리세요."
    ],
    "목 통증": [
        "화면을 눈높이로 올리고 거리를 50~70cm 유지하세요.",
        "턱 당기기·목 측굴 스트레칭을 해보세요.",
        "장시간 스마트폰 고개 숙임을 줄이세요.",
        "따뜻한 샤워/찜질로 긴장을 완화하세요."
    ],
    "손발 저림": [
        "자세 교정으로 신경 압박을 줄이세요.",
        "스트레칭과 순환 개선을 위해 가볍게 흔들기·쥐었다 펴기.",
        "너무 조이는 신발/손목밴드는 피하세요.",
        "수분과 전해질 균형을 유지하세요."
    ]
}

def pick_feedback(symptom_list, k_each=2, max_total=8):
    tips = []
    for s in symptom_list:
        if s in FEEDBACK_POOLS:
            pool = FEEDBACK_POOLS[s][:]
            random.shuffle(pool)
            tips.extend(pool[:k_each])
    # 중복 제거 & 상한
    dedup = []
    for t in tips:
        if t not in dedup:
            dedup.append(t)
    return dedup[:max_total]

# --------- 점수 계산 ----------
def compute_score(answers):
    score = 100
    # 공부 시간
    stime = answers["study_time"]
    if stime == "9시간 이상":
        score -= 15
    elif stime == "2시간 이하":
        score -= 5
    # 운동 빈도
    if answers["exercise_freq"] == "전혀 안 함":
        score -= 15
    elif answers["exercise_freq"] == "가끔(주 1~2회)":
        score -= 5
    # 식사
    meals = answers["meals"]
    if meals == "불규칙(하루 1끼 이하)":
        score -= 15
    elif meals == "하루 2끼":
        score -= 5
    # 식사 추가 패턴
    diet_flags = answers["diet_flags"]
    if "간식 위주" in diet_flags: score -= 5
    if "인스턴트/패스트푸드가 많음" in diet_flags: score -= 8
    # 자세
    posture = answers["posture"]
    if posture in ["허리 굽힘", "고개 숙임", "다리 꼬고 앉음"]:
        score -= 10
    # 증상
    syms = answers["symptoms"]
    penalties = {
        "두통":10, "눈의 피로":10, "허리 통증":10, "손목 저림":10,
        "무릎 통증":8, "목 통증":7,"어깨 결림":6,"종아리 붓기":6,
        "집중력 저하":5,"불면":7,"피로감 지속":7,"손발 저림":6
    }
    for s in syms:
        score -= penalties.get(s, 0)
    score = max(0, min(100, score))
    if score >= 80: cat = "매우 좋음"
    elif score >= 60: cat = "보통"
    else: cat = "주의 필요"
    return score, cat

# --------- 헤더 ----------
st.markdown("<h1 style='margin-bottom:.4rem;'>📚 학생 건강 진단 & 보충 플랜카드 💪</h1>", unsafe_allow_html=True)
st.caption("입력 → 결과 → ✨진단서 만들기✨ 까지 한 번에!")

# --------- STEP 1: 기본 정보 ----------
if st.session_state.step == 1:
    with st.container():
        col1, col2 = st.columns([1.1,1])
        with col1:
            st.markdown("### 👤 기본 정보 입력")
            name = st.text_input("이름", placeholder="이름을 입력하세요")
            age = st.number_input("나이", min_value=10, max_value=30, step=1, value=16)
            gender = st.radio("성별", ["남","여","선택 안 함"], horizontal=True)
            grade = st.selectbox("학년", ["중학생","고등학생","대학생"])
        with col2:
            section_card("Tip", "기본 정보를 바탕으로 **언어/톤/추천 강도**가 살짝 달라져요. 솔직하게 입력하면 더 좋아요 😄", "💡")

    st.markdown("---")
    if st.button("✅ 진단 시작하기", use_container_width=True):
        st.session_state.name = name.strip() if name else "익명"
        st.session_state.age = age
        st.session_state.gender = gender
        st.session_state.grade = grade
        st.session_state.step = 2

# --------- STEP 2: 생활 습관 & 증상 ----------
elif st.session_state.step == 2:
    st.markdown("### 📋 생활 습관 & 증상 선택 (클릭으로 간편하게!)")
    c1, c2 = st.columns(2)
    with c1:
        study_time = st.radio("오늘 공부 시간은?", ["2시간 이하","3~5시간","6~8시간","9시간 이상"], horizontal=True)
        exercise_freq = st.radio("운동 빈도는?", ["전혀 안 함","가끔(주 1~2회)","자주(주 3회 이상)"], horizontal=True)
        exercise_types = st.multiselect("주로 하는 운동 (복수 선택)", EX_TYPES, default=[])
        meals = st.radio("식사 습관은?", MEAL_PATTERNS[:3], horizontal=False)
        diet_flags = st.multiselect("추가 식습관 체크", MEAL_PATTERNS[3:], default=[])
    with c2:
        posture = st.radio("공부할 때 주로 어떤 자세인가요?", ["바른 자세","허리 굽힘","고개 숙임","다리 꼬고 앉음","자주 일어나서 움직임"], horizontal=False)
        symptoms = st.multiselect("공부 중/후 느끼는 몸의 이상 (복수 선택)", SYMPTOMS, default=[])

        chips = "".join([f"<span class='tag'>{t}</span>" for t in symptoms])
        st.markdown(f"<div class='glass'><b>선택한 증상:</b> {chips if chips else '없음'}</div>", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🔍 결과 확인하기", use_container_width=True):
        st.session_state.answers = {
            "study_time":study_time,
            "exercise_freq":exercise_freq,
            "exercise_types":exercise_types,
            "meals":meals,
            "diet_flags":diet_flags,
            "posture":posture,
            "symptoms":[s for s in symptoms if s != "없음"]
        }
        st.session_state.step = 3

# --------- STEP 3: 결과 ----------
elif st.session_state.step == 3:
    answers = st.session_state.answers
    score, category = compute_score(answers)
    set_background_by_category(category)

    # 상단 요약 배너
    st.markdown(f"""
    <div class='glass' style="display:flex;align-items:center;justify-content:space-between;gap:1rem;">
        <div>
            <div class='pill'>결과</div>
            <h2 style="margin:.3rem 0 0 0;">{st.session_state.name}님의 오늘 건강 점수: <b>{score}점</b> · 상태: <b>{category}</b> {'😍' if category=='매우 좋음' else '🙂' if category=='보통' else '😥'}</h2>
            <div style="opacity:.8">학년: {st.session_state.grade} · 나이: {st.session_state.age} · 성별: {st.session_state.gender}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 요인별 피드백
    cols = st.columns(3)
    with cols[0]:
        bullets = []
        stime = answers["study_time"]
        if stime=="9시간 이상": bullets.append("공부 시간이 길어요. **50분 집중 + 10분 휴식**으로 분절하세요 ⏰")
        elif stime=="2시간 이하": bullets.append("공부 시간이 짧아요. **작게 자주** 공부 블록을 늘려보세요 📖")
        if answers["posture"] in ["허리 굽힘","고개 숙임","다리 꼬고 앉음"]:
            bullets.append("자세 교정 필요! **모니터 눈높이·허리 지지** 세팅 🪑")
        section_card("공부·자세", "<br>".join([f"• {b}" for b in bullets]) or "안정적이에요! 지금 페이스 유지!", "📖")

    with cols[1]:
        bullets = []
        if answers["exercise_freq"]=="전혀 안 함":
            bullets.append("하루 **10분 스트레칭/걷기**부터 시작해요 🏃")
        if answers["exercise_types"]:
            bullets.append("운동: " + ", ".join(answers["exercise_types"]))
        section_card("운동", "<br>".join([f"• {b}" for b in bullets]) or "꾸준함이 최고! 오늘도 가볍게 움직여요.", "💪")

    with cols[2]:
        bullets = []
        if answers["meals"]=="불규칙(하루 1끼 이하)":
            bullets.append("하루 **3끼 리듬**을 회복해요 🍱")
        elif answers["meals"]=="하루 2끼":
            bullets.append("**아침 소량**이라도 추가 추천 🍌🥛")
        if "간식 위주" in answers["diet_flags"]:
            bullets.append("간식은 **과일/견과**로 대체해보세요 🍎")
        if "인스턴트/패스트푸드가 많음" in answers["diet_flags"]:
            bullets.append("가공식품 빈도를 줄이고 **단백질+채소** 중심으로 🥗")
        section_card("식사", "<br>".join([f"• {b}" for b in bullets]) or "균형 잘 잡혀 있어요! 👍", "🍽️")

    # 증상 맞춤 팁
    syms = answers["symptoms"]
    if syms:
        tips = pick_feedback(syms, k_each=2, max_total=8)
        section_card("증상 맞춤 팁", "<br>".join([f"• {t}" for t in tips]), "🩺")
        st.session_state.tips = tips
    else:
        section_card("증상 맞춤 팁", "특이 증상이 없어요. 컨디션 유지를 위해 **수면·수분·가벼운 운동**을 지속해요 🌙💧", "🩺")
        st.session_state.tips = ["수분 섭취를 규칙적으로 하세요.", "수면 루틴을 일정하게 유지하세요.", "가벼운 유산소 운동으로 컨디션을 올려보세요."]

    st.markdown("---")
    c1, c2, c3 = st.columns([1.2,1,1])
    with c1:
        if st.button("🎴 나의 보충 플랜카드 진단서 만들기", use_container_width=True):
            st.session_state.score = score
            st.session_state.category = category
            st.session_state.step = 4
    with c2:
        if st.button("⬅️ 수정하기", use_container_width=True):
            st.session_state.step = 2
    with c3:
        if st.button("🔄 처음으로", use_container_width=True):
            st.session_state.step = 1

# --------- STEP 4: 진단서(카드) + 다운로드 ----------
elif st.session_state.step == 4:
    answers = st.session_state.answers
    score = st.session_state.score
    category = st.session_state.category
    set_background_by_category(category)

    # 예쁜 카드(화면 표시용)
    emoji = "🌈" if category=="매우 좋음" else "🌤️" if category=="보통" else "🌧️"
    today = datetime.date.today().strftime("%Y-%m-%d")
    card_html = f"""
    <div class='glass' style="border-radius:28px;padding:1.4rem 1.6rem;">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <div style="display:flex;align-items:center;gap:.6rem">
            <span style="font-size:2rem">{emoji}</span>
            <h2 style="margin:0">나의 보충 플랜카드 · 진단서</h2>
        </div>
        <div class="pill">{today}</div>
      </div>
      <hr style="border:none;height:1px;background:rgba(0,0,0,.07);margin:.8rem 0 .6rem 0"/>
      <div style="display:grid;grid-template-columns:1.2fr 1fr;gap:1rem;">
        <div>
            <div><b>이름</b> : {st.session_state.name}</div>
            <div><b>학년</b> : {st.session_state.grade} · <b>나이</b>: {st.session_state.age} · <b>성별</b>: {st.session_state.gender}</div>
            <div style="margin-top:.4rem"><b>점수/상태</b> : <span class="tag">{score}점</span> <span class="tag">{category}</span></div>
            <div style="margin-top:.6rem">
                <b>핵심 요약</b><br/>
                • 공부: {answers['study_time']}<br/>
                • 운동: {answers['exercise_freq']} / {", ".join(answers['exercise_types']) if answers['exercise_types'] else "선택 없음"}<br/>
                • 식사: {answers['meals']} {(" · " + ", ".join(answers['diet_flags'])) if answers['diet_flags'] else ""}<br/>
                • 자세: {answers['posture']}<br/>
                • 증상: {", ".join(answers['symptoms']) if answers['symptoms'] else "없음"}
            </div>
        </div>
        <div class='glass' style="border-radius:20px;">
            <div style="font-size:.95rem;line-height:1.55">
                <b>추천 음식 🍎</b><br/>단백질(계란/두부/닭가슴살), 채소/과일, 통곡물, 견과류, 물 자주 마시기<br/><br/>
                <b>추천 운동 🧘</b><br/>걷기·스트레칭 10~15분/일, 주 2~3회 가벼운 근력·유산소 혼합
            </div>
        </div>
      </div>
      <div style="margin-top:.8rem">
        <b>맞춤 조언/충고 📝</b>
        <ul style="margin:.4rem 0 0 1rem;">
            {''.join([f'<li>{t}</li>' for t in st.session_state.tips])}
        </ul>
      </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

    # ---- PNG 생성(PIL) & 다운로드 ----
    def render_certificate_png():
        W, H = 900, 1300
        img = Image.new("RGB", (W, H), (255, 252, 248))
        draw = ImageDraw.Draw(img)
        # 카드 배경
        card_pad = 40
        rect = [card_pad, card_pad, W-card_pad, H-card_pad]
        draw.rounded_rectangle(rect, radius=36, fill=(255,255,255), outline=(230,230,230), width=3)

        # 폰트 (시스템 기본)
        title = ImageFont.load_default()
        body = ImageFont.load_default()

        def tw(text, width):
            return textwrap.wrap(text, width=width)

        y = 70
        # 헤더
        draw.text((60,y), f"나의 보충 플랜카드 · 진단서 ({datetime.date.today().isoformat()})", font=title, fill=(30,30,30))
        y += 30
        draw.line([(60,y),(W-60,y)], fill=(230,230,230), width=2)
        y += 20

        # 기본 정보
        draw.text((60,y), f"이름: {st.session_state.name}   학년: {st.session_state.grade}   나이: {st.session_state.age}   성별: {st.session_state.gender}", font=body, fill=(40,40,40))
        y += 24
        draw.text((60,y), f"점수/상태: {score}점 · {category}", font=body, fill=(40,40,40))
        y += 32

        # 요약
        summary = [
            f"공부: {answers['study_time']}",
            f"운동: {answers['exercise_freq']} / {', '.join(answers['exercise_types']) if answers['exercise_types'] else '선택 없음'}",
            f"식사: {answers['meals']} {' · ' + ', '.join(answers['diet_flags']) if answers['diet_flags'] else ''}",
            f"자세: {answers['posture']}",
            f"증상: {', '.join(answers['symptoms']) if answers['symptoms'] else '없음'}"
        ]
        for line in summary:
            draw.text((60, y), line, font=body, fill=(50,50,50))
            y += 22

        y += 12
        draw.line([(60,y),(W-60,y)], fill=(235,235,235), width=1)
        y += 18

        # 추천 섹션
        rec_food = "추천 음식: 단백질(계란·두부·닭가슴살), 채소/과일, 통곡물, 견과류, 물 자주 마시기"
        rec_ex = "추천 운동: 걷기·스트레칭 10~15분/일, 주 2~3회 가벼운 근력·유산소 혼합"
        for para in [rec_food, rec_ex]:
            for t in tw(para, 48):
                draw.text((60,y), t, font=body, fill=(60,60,60))
                y += 22
            y += 6

        y += 6
        draw.text((60,y), "맞춤 조언/충고:", font=title, fill=(30,30,30))
        y += 26

        tips = st.session_state.tips
        for tip in tips:
            for t in tw("• " + tip, 54):
                draw.text((80,y), t, font=body, fill=(55,55,55))
                y += 22
            y += 2

        bio = io.BytesIO()
        img.save(bio, format="PNG")
        bio.seek(0)
        return bio

    png_bytes = render_certificate_png()
    st.download_button("🖼️ 진단서 PNG 다운로드", data=png_bytes, file_name="my_health_plan_card.png", mime="image/png", use_container_width=True)

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ 결과로 돌아가기", use_container_width=True):
            st.session_state.step = 3
    with c2:
        if st.button("🔄 처음으로", use_container_width=True):
            st.session_state.step = 1

