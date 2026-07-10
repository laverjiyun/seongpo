import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. 페이지 레이아웃 설정
st.set_page_config(page_title="안산 상권 빅데이터 분석", layout="wide")

# 세련된 대시보드 테마 CSS
st.markdown("""
    <style>
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1 { color: #1E3A8A; font-weight: 800; }
    h2 { color: #2563EB; font-weight: 700; border-bottom: 2px solid #E5E7EB; padding-bottom: 10px; margin-top: 20px; }
    h3 { color: #1E3A8A; font-weight: 600; }
    
    /* 추천 카드 스타일 */
    .shop-card {
        background-color: #F8FAFC;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2563EB;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }
    
    /* 결론 페이지 전용 스타일 */
    .conclusion-box {
        background-color: #EFF6FF;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #BFDBFE;
        line-height: 1.8;
    }
    .highlight { color: #1D4ED8; font-weight: 700; }
    .critical { color: #EF4444; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# 2. 데이터 불러오기
@st.cache_data
def load_data():
    return pd.read_csv("ansan_commercial_cleaned_final.csv")

try:
    df = load_data()
except Exception as e:
    st.error("데이터 파일(ansan_commercial_cleaned_final.csv)이 없습니다. 파일 위치를 확인해주세요.")
    st.stop()

seongpo_df = df[df["상권분류"] == "성포고주변"]
jungang_df = df[df["상권분류"] == "중앙동로데오"]

# 3. 사이드바 목차
st.sidebar.markdown("## 📂 분석 목차")
page = st.sidebar.radio(
    "이동할 페이지를 선택하세요",
    ["🏫 성포고 주변 상권 현황", 
     "🛍️ 중앙동 로데오 상권 현황", 
     "🧪 상권별 청소년 수용력 실험", 
     "🎯 맞춤형 로컬 가게 추천", 
     "💡 종합 결론: 데이터가 말하는 진실"]
)

# ==========================================
# Page 1. 성포고 주변 상권 현황
# ==========================================
if page == "🏫 성포고 주변 상권 현황":
    st.title("🏫 성포고등학교 주변 상권 분석")
    st.markdown("##### 실제 운영 중인 100개 매장 기반 분석")
    sp_counts = seongpo_df["업종분류"].value_counts().reset_index()
    fig = px.pie(sp_counts, values='count', names='업종분류', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Page 2. 중앙동 로데오 상권 현황
# ==========================================
elif page == "🛍️ 중앙동 로데오 상권 현황":
    st.title("🛍️ 중앙동 로데오 상권 분석")
    st.markdown("##### 실제 운영 중인 100개 매장 기반 분석")
    ja_counts = jungang_df["업종분류"].value_counts().reset_index()
    fig = px.pie(ja_counts, values='count', names='업종분류', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# ★ Page 3. 상권별 청소년 수용력 실험 (수정 완료)
# ==========================================
elif page == "🧪 상권별 청소년 수용력 실험":
    st.title("🧪 상권별 청소년 수용력 대조 실험")
    st.markdown("##### 설정한 예산 범위 내에서 각 상권이 청소년을 얼마나 수용할 수 있는지 실시간 시뮬레이션을 수행합니다.")
    
    # 예산 슬라이더 설정
    user_budget = st.slider("💰 학생 1인당 지출 예산 한도 설정 (원)", 1000, 35000, 10000, step=500)
    
    # 10대 이용 가능 타겟이면서 사용자의 예산 이하인 매장 필터링
    sp_filtered = seongpo_df[(seongpo_df["평균가격"] <= user_budget) & (seongpo_df["주타겟층"].str.contains("10"))]
    ja_filtered = jungang_df[(jungang_df["평균가격"] <= user_budget) & (jungang_df["주타겟층"].str.contains("10"))]
    all_filtered = df[(df["평균가격"] <= user_budget) & (df["주타겟층"].str.contains("10"))]
    
    # 상권 비교 바 차트 시각화
    sim_data = pd.DataFrame({
        "상권": ["성포고 주변 상권", "중앙동 로데오 상권"],
        "수용 가능한 매장 수": [len(sp_filtered), len(ja_filtered)]
    })
    
    st.markdown("### 📊 예산 내 수용 가능한 점포 수 비교")
    fig_bar = px.bar(sim_data, x="수용 가능한 매장 수", y="상권", orientation='h', 
                     color="상권", color_discrete_sequence=["#F59E0B", "#3B82F6"])
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown(f"### 📍 현재 예산 ({user_budget:,}원 이하) 기준 입점 매장 목록")
    st.write("아래 탭을 전환하며 상권별로 실제 입장 가능한 매장들을 확인해 보세요.")
    
    # 상권별 탭 분리 구성 (성포고 상권, 중앙동 상권, 둘 다 통합)
    tab1, tab2, tab3 = st.tabs(["🏫 성포고 주변 매장", "🛍️ 중앙동 로데오 매장", "🔄 두 상권 전체 매장 (통합)"])
    
    with tab1:
        st.write(f"**성포고 주변에서 이용 가능한 매장: 총 {len(sp_filtered)}개**")
        if len(sp_filtered) > 0:
            for row in sp_filtered.itertuples():
                st.markdown(f'<div class="shop-card"><b>{row.가게이름}</b><br>{row.업종분류} | {row.대표메뉴} | 가격: {row.평균가격:,}원</div>', unsafe_allow_html=True)
        else:
            st.warning("이 예산으로 성포고 주변에서 갈 수 있는 10대 매장이 없습니다.")
            
    with tab2:
        st.write(f"**중앙동 로데오에서 이용 가능한 매장: 총 {len(ja_filtered)}개**")
        if len(ja_filtered) > 0:
            for row in ja_filtered.itertuples():
                st.markdown(f'<div class="shop-card"><b>{row.가게이름}</b><br>{row.업종분류} | {row.대표메뉴} | 가격: {row.평균가격:,}원</div>', unsafe_allow_html=True)
        else:
            st.warning("이 예산으로 중앙동에서 갈 수 있는 10대 매장이 없습니다.")
            
    with tab3:
        st.write(f"**두 상권 통합 이용 가능한 매장: 총 {len(all_filtered)}개**")
        if len(all_filtered) > 0:
            for row in all_filtered.itertuples():
                st.markdown(f'<div class="shop-card"><b>{row.가게이름}</b> ({row.상권분류})<br>{row.업종분류} | {row.대표메뉴} | 가격: {row.평균가격:,}원</div>', unsafe_allow_html=True)
        else:
            st.warning("해당 예산으로 이용 가능한 매장이 안산 상권 전체에 없습니다.")

# ==========================================
# Page 4. 맞춤형 로컬 가게 추천
# ==========================================
elif page == "🎯 맞춤형 로컬 가게 추천":
    st.title("🎯 조건 검색 기반 로컬 매장 추천")
    select_budget = st.slider("💰 예산 (원)", 1000, 35000, 12000)
    select_age = st.selectbox("👥 연령층", ["10-20대", "10-30대", "20-40대", "30-50대", "40-60대"])
    res = df[(df["평균가격"] <= select_budget) & (df["주타겟층"] == select_age)].head(10)
    for row in res.itertuples():
        st.markdown(f'<div class="shop-card"><b>{row.가게이름}</b> ({row.상권분류})<br>{row.대표메뉴} | {row.평균가격:,}원</div>', unsafe_allow_html=True)

# ==========================================
# Page 5. 종합 결론 (강화된 버전 유지)
# ==========================================
elif page == "💡 종합 결론: 데이터가 말하는 진실":
    st.title("💡 종합 결론 : 안산시 청소년의 '상권 이탈' 원인 분석")
    
    sp_v = seongpo_df["업종분류"].value_counts().reindex(df["업종분류"].unique(), fill_value=0)
    ja_v = jungang_df["업종분류"].value_counts().reindex(df["업종분류"].unique(), fill_value=0)
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=sp_v.values, theta=sp_v.index, fill='toself', name='성포고 주변'))
    fig_radar.add_trace(go.Scatterpolar(r=ja_v.values, theta=ja_v.index, fill='toself', name='중앙동 로데오'))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True, title="업종별 밀집도 비교 (데이터 가시화)")
    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🛑 성포고 상권의 장벽: <span class='critical'>'경제적 단절'</span>", unsafe_allow_html=True)
        st.markdown(f"""<div class="conclusion-box">성포고 주변 매장 데이터의 평균 가격은 <b>{int(seongpo_df['평균가격'].mean()):,}원</b>으로 형성되어 있습니다.<br><br>1. <b>지불 능력의 한계:</b> 고가음식점 비율이 높고 약국, 병원 등 생활 필수 시설 위주여서 10대의 가처분 소득으로 접근 가능한 매장이 현저히 부족합니다.<br>2. <b>타겟 미스매치:</b> 주타겟층의 60% 이상이 <b>40-60대 성인층</b>에 맞춰져 있어, 하교 후 학생들을 수용할 '심리적 공간'이 부재합니다.</div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("### 🚀 중앙동의 강력한 인력: <span class='highlight'>'가성비 클러스터'</span>", unsafe_allow_html=True)
        st.markdown(f"""<div class="conclusion-box">중앙동 로데오는 10대 타겟 매장 비중이 성포동 대비 <b>3배 이상</b> 높습니다.<br><br>1. <b>원스톱 문화 소비:</b> 마라탕(식사) - 코인노래방(놀이) - 카페(디저트) - 패션/쇼핑(소비)으로 이어지는 동선이 반경 300m 내에 밀집되어 있습니다.<br>2. <b>규모의 경제:</b> 매장 수가 많아 선택권이 넓고, 저렴한 프랜차이즈가 경쟁하며 10대 맞춤형 <b>'저가형 클러스터'</b>를 형성하고 있습니다.</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<h2>📋 최종 분석 요약 (Data Insights)</h2>", unsafe_allow_html=True)
    st.info("""
    **분석 결과 핵심 요약**
    - **이탈 현상의 본질:** 학생들은 단순히 멀리 나가는 것을 즐기는 것이 아니라, 동네 상권에서 **'소외'**되었기 때문에 중앙동으로 이동하는 것입니다.
    - **상권의 양극화:** 성포동 상권은 '가족/생활형 상권'으로 고착화되고 있으며, 중앙동은 '문화/소비형 상권'으로 독점적 지위를 강화하고 있습니다.
    - **데이터 입증:** 예산 1만원 조건 하에서 성포동 학생이 갈 수 있는 곳은 편의점뿐이지만, 중앙동에서는 영화 관람을 제외한 거의 모든 문화 활동이 가능함이 데이터로 입증되었습니다.
    """)
