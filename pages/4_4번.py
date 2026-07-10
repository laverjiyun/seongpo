import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 레이아웃 설정
st.set_page_config(page_title="안산 상권 빅데이터 분석", layout="wide")

# 깔끔하고 세련된 대시보드 테마 CSS (추천 카드용 스타일 추가)
st.markdown("""
    <style>
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1 { color: #1E3A8A; font-weight: 800; }
    h2 { color: #2563EB; font-weight: 700; border-bottom: 2px solid #E5E7EB; padding-bottom: 10px; }
    h3 { color: #1E3A8A; font-weight: 600; margin-bottom: 5px; }
    div[data-testid="stMetricValue"] { font-size: 32px; font-weight: 700; color: #1D4ED8; }
    
    /* 맛집 추천 카드 커스텀 스타일 */
    .shop-card {
        background-color: #F8FAFC;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2563EB;
        margin-bottom: 15px;
    }
    .shop-title { font-size: 18px; font-weight: 700; color: #1E293B; }
    .shop-tag { background-color: #E2E8F0; color: #475569; padding: 2px 8px; border-radius: 5px; font-size: 12px; font-weight: 600; }
    .shop-menu { font-size: 14px; color: #64748B; margin-top: 5px; }
    .shop-price { font-size: 16px; font-weight: 700; color: #EF4444; margin-top: 5px; }
    </style>
""", unsafe_allow_html=True)

# 2. 정제된 파일 불러오기
@st.cache_data
def load_data():
    return pd.read_csv("ansan_commercial_cleaned_final.csv")

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 파일(ansan_commercial_cleaned_final.csv)을 읽는 중 오류가 발생했습니다.")
    st.stop()

seongpo_df = df[df["상권분류"] == "성포고주변"]
jungang_df = df[df["상권분류"] == "중앙동로데오"]

# 3. 사이드바 목차 (5개 페이지로 확장)
st.sidebar.markdown("## 📂 분석 목차")
page = st.sidebar.radio(
    "이동할 페이지를 선택하세요",
    ["🏫 성포고 주변 상권 현황", 
     "🛍️ 중앙동 로데오 상권 현황", 
     "🧪 상권별 청소년 수용력 실험", 
     "🎯 맞춤형 로컬 가게 추천", 
     "💡 종합 결론: 10대 이동 원인"]
)
st.sidebar.markdown("---")
st.sidebar.caption("안산시 청소년 상권 이동 패턴 분석 프로젝트 v5.0")


# ==========================================
# Page 1. 성포고 주변 상권 현황
# ==========================================
if page == "🏫 성포고 주변 상권 현황":
    st.title("🏫 성포고등학교 주변 상권 분석")
    st.markdown("##### 학교 정문 앞 및 배후지 200개 매장의 업종 구성 비율을 그래프로 시각화합니다.")
    
    m1, m2, m3 = st.columns(3)
    with m1: st.metric("총 분석 점포 수", f"{len(seongpo_df)} 개")
    with m2: st.metric("상권 평균 단가", f"{int(seongpo_df['평균가격'].mean()):,} 원")
    with m3: st.metric("가장 밀집된 업종", seongpo_df["업종분류"].value_counts().index[0])
        
    st.markdown("---")
    sp_counts = seongpo_df["업종분류"].value_counts().reset_index()
    sp_counts.columns = ["업종분류", "점포수"]
    
    fig = px.pie(sp_counts, values='점포수', names='업종분류', hole=0.4,
                 title="성포고 주변 상권 업종 구성 비율", color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=False, margin=dict(t=50, b=20, l=20, r=20))
    
    col_chart, col_info = st.columns([2, 1])
    with col_chart: st.plotly_chart(fig, use_container_width=True)
    with col_info:
        st.markdown("### 📋 그래프 주요 특징")
        st.write("- **고가음식점 및 일반음식점**이 상권의 절반 이상을 차지합니다.")
        st.write("- 주거지 배후 상권 특성상 부모 세대 중심의 외식 인프라가 짙게 깔려 있습니다.")


# ==========================================
# Page 2. 중앙동 로데오 상권 현황
# ==========================================
elif page == "🛍️ 중앙동 로데오 상권 현황":
    st.title("🛍️ 중앙동 로데오 상권 분석")
    st.markdown("##### 안산 최대 중심지인 중앙역 로데오거리 200개 매장의 업종 구성 비율을 그래프로 시각화합니다.")
    
    m1, m2, m3 = st.columns(3)
    with m1: st.metric("총 분석 점포 수", f"{len(jungang_df)} 개")
    with m2: st.metric("상권 평균 단가", f"{int(jungang_df['평균가격'].mean()):,} 원")
    with m3: st.metric("가장 밀집된 업종", jungang_df["업종분류"].value_counts().index[0])
        
    st.markdown("---")
    ja_counts = jungang_df["업종분류"].value_counts().reset_index()
    ja_counts.columns = ["업종분류", "점포수"]
    
    fig = px.pie(ja_counts, values='점포수', names='업종분류', hole=0.4,
                 title="중앙동 로데오 상권 업종 구성 비율", color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=False, margin=dict(t=50, b=20, l=20, r=20))
    
    col_chart, col_info = st.columns([2, 1])
    with col_chart: st.plotly_chart(fig, use_container_width=True)
    with col_info:
        st.markdown("### 📋 그래프 주요 특징")
        st.write("- **학생편의 및 카페/디저트, 패션/쇼핑**이 핵심 축을 이룹니다.")
        st.write("- 청소년층이 선호하고 쉽게 소비할 수 있는 문화 및 오락 시설이 집약되어 있습니다.")


# ==========================================
# Page 3. 상권별 청소년 수용력 실험
# ==========================================
elif page == "🧪 상권별 청소년 수용력 실험":
    st.title("🧪 Page 3. 두 상권의 청소년 유효 수요 수용력 대조 실험")
    st.markdown("##### **동일한 예산 조건을 투입했을 때, 각 상권에서 10대가 '생존(진입) 가능한 점포 수'를 그래프로 대조합니다.**")
    
    with st.container(border=True):
        user_budget = st.slider("💰 하교 후 고등학생 페르소나의 현실적 지출 예산 (원)", 1000, 30000, 8500, step=500)
    
    user_ages = ["10-20대", "10-30대"]
    sp_count = len(seongpo_df[(seongpo_df["평균가격"] <= user_budget) & (seongpo_df["주타겟층"].isin(user_ages))])
    ja_count = len(jungang_df[(jungang_df["평균가격"] <= user_budget) & (jungang_df["주타겟층"].isin(user_ages))])
    
    sim_data = pd.DataFrame({"상권분류": ["성포고 주변", "중앙동 로데오"], "진입 가능 매장 수 (개)": [sp_count, ja_count]})
    fig = px.bar(sim_data, x="진입 가능 매장 수 (개)", y="상권분류", orientation='h', text="진입 가능 매장 수 (개)", 
                 title=f"{user_budget:,}원 이하 예산 시 상권별 학생 수용력 비교", color="상권분류", color_discrete_sequence=["#ff9999", "#66b3ff"])
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis=dict(range=[0, 210]), showlegend=False, margin=dict(t=50, b=20, l=20, r=20))
    st.plotly_chart(fig, use_container_width=True)
    st.info(f"💡 **실험 해석:** 슬라이더를 10대 현실 예산 범위로 낮출수록 **성포고 상권 막대 그래프는 급격히 줄어들지만, 중앙동 로데오 그래프는 길게 살아남습니다.**")


# ==========================================
# ★ NEW Page 4. 맞춤형 로컬 가게 추천 (세련된 카드 뷰어 UI 적용)
# ==========================================
elif page == "🎯 맞춤형 로컬 가게 추천":
    st.title("🎯 Page 4. 조건 검색 기반 로컬 매장 큐레이션")
    st.markdown("##### 안산 상권 빅데이터에서 설정한 예산과 연령 타겟층에 맞는 매장을 감각적인 디자인 카드로 추천합니다.")
    
    # 1. 상단 깔끔한 검색 조건 필터바
    with st.container(border=True):
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            select_loc = st.selectbox("📍 분석 지역 선택", ["전체 상권 보기", "🏫 성포고 주변", "🛍️ 중앙동 로데오"])
        with col_f2:
            select_budget = st.slider("💰 최대 지출 가능 예산 (원)", 1000, 35000, 12000, step=1000)
        with col_f3:
            age_opts = ["10-20대", "10-30대", "20-40대", "30-50대", "40-60대"]
            select_age = st.selectbox("👥 주 소비 연령대 선택", age_opts, index=0)

    # 데이터 필터링 로직
    target_df = df.copy()
    if select_loc == "🏫 성포고 주변":
        target_df = target_df[target_df["상권분류"] == "성포고주변"]
    elif select_loc == "🛍️ 중앙동 로데오":
        target_df = target_df[target_df["상권분류"] == "중앙동로데오"]
        
    filtered_shops = target_df[(target_df["평균가격"] <= select_budget) & (target_df["주타겟층"] == select_age)]
    
    # 상단 요약 배너
    st.markdown(f"### 🔍 검색 결과 : 총 **{len(filtered_shops)}개**의 맞춤형 점포 매칭 성공")
    
    # 2. 결과 출력 영역 (2열 카드 뷰 구조로 배치)
    if len(filtered_shops) > 0:
        # 최대 12개만 격자형 카드로 깔끔하게 노출
        display_shops = filtered_shops.head(12)
        
        # 좌우 2개의 컬럼으로 카드를 나누어 배치
        col_left, col_right = st.columns(2)
        
        for idx, row in enumerate(display_shops.itertuples()):
            # 카드 내부 커스텀 HTML 문자열 작성
            card_html = f"""
            <div class="shop-card">
                <span class="shop-tag">📍 {row.상권분류}</span> &nbsp;
                <span class="shop-tag">📂 {row.업종분류}</span>
                <div class="shop-title" style="margin-top:8px;">✨ {row.가게이름}</div>
                <div class="shop-menu">🍽️ 대표메뉴: {row.대표메뉴} (주타겟: {row.주타겟층})</div>
                <div class="shop-price">💳 평균 가격대: {row.평균가격:,}원</div>
            </div>
            """
            
            if idx % 2 == 0:
                with col_left: st.markdown(card_html, unsafe_allow_html=True)
            else:
                with col_right: st.markdown(card_html, unsafe_allow_html=True)
                
        if len(filtered_shops) > 12:
            st.caption(f"※ 데이터 가독성을 위해 매칭된 {len(filtered_shops)}개 점포 중 상위 12개 매장만 추천 카드로 표시 중입니다.")
    else:
        st.warning("⚠️ 설정하신 조건(지역/예산/나이)을 동시에 만족하는 점포가 상권 데이터 세트에 존재하지 않습니다. 조건을 조금 더 여유롭게 조정해 보세요.")


# ==========================================
# Page 5. 종합 결론 (기존 4번 페이지를 이동)
# ==========================================
elif page == "💡 종합 결론: 10대 이동 원인":
    st.title("💡 Page 5. 데이터로 입증된 청소년 유동인구 이탈 원인")
    st.markdown("##### 400개 실제 매장 데이터를 대조하여 도출한 최종 학술 리포트")
    
    st.markdown("<h2>📈 두 상권의 업종 분포 비교 (세로 막대 그래프)</h2>", unsafe_allow_html=True)
    sp_chart = seongpo_df["업종분류"].value_counts().rename("성포고 주변")
    ja_chart = jungang_df["업종분류"].value_counts().rename("중앙동 로데오")
    total_chart = pd.concat([sp_chart, ja_chart], axis=1).fillna(0)
    
    st.bar_chart(total_chart)
    
    st.markdown("---")
    st.markdown("## 📝 빅데이터 분석 최종 결론")
    
    col_doc1, col_doc2 = st.columns(2)
    with col_doc1:
        with st.container(border=True):
            st.markdown("### ❌ 성포고 배후 상권의 '수요-공급 미스매치'")
            st.markdown("""
            * **인프라 구성의 한계**: 성포고 주변은 학령인구 수요가 두텁지만, 데이터 그래프가 보여주듯 **고가 식당 및 성인 타겟 업종**에 편중되어 있습니다.
            * **지불 능력의 장벽**: 부모 세대의 지갑을 노린 상권 구조로 인해 정작 고등학생들의 예산을 수용하지 못하는 **'로컬 상권 소외 현상'**이 발생합니다.
            """)
            
    with col_doc2:
        with st.container(border=True):
            st.markdown("### ⭕ 중앙동의 '원스톱 가성비 클러스터 효과'")
            st.markdown("""
            * **10대 맞춤 인프라의 집중**: 중앙동 로데오는 **'학생편의(코노, 네컷사진)'**, **'카페/디저트'** 업종이 조밀하게 뭉쳐 상권 그래프의 우위를 점합니다.
            * **한정된 예산의 효용 극대화**: 청소년들은 한 공간에서 식사와 문화 활동을 끊김 없이 저렴하게 해결할 수 있는 **'가성비 클러스터'**를 향해 합리적인 지리적 이동을 선택하는 것입니다.
            """)
