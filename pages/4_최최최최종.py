import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# 1. 페이지 레이아웃 및 웹 브라우저 탭 설정 (앱 최상단 고정)
st.set_page_config(page_title="성포동 상권 10대 활성화 전략", layout="wide")

# 세련된 데이터 과학 대시보드 테마 CSS
st.markdown("""
    <style>
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1 { color: #1E3A8A; font-weight: 800; }
    h2 { color: #2563EB; font-weight: 700; border-bottom: 2px solid #E5E7EB; padding-bottom: 10px; margin-top: 25px; }
    h3 { color: #1E3A8A; font-weight: 600; margin-top: 15px; }
    div[data-testid="stMetricValue"] { font-size: 32px; font-weight: 700; color: #1D4ED8; }
    
    .ppdac-box {
        background-color: #F8FAFC;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 20px;
        line-height: 1.7;
    }
    .conclusion-box {
        background-color: #FFFBEB;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #FDE68A;
        line-height: 1.8;
    }
    .badge {
        background-color: #2563EB; color: white; padding: 3px 8px; 
        border-radius: 5px; font-size: 12px; font-weight: bold; vertical-align: middle;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 데이터 인코딩 에러 우회 및 안전 로딩
file_name = "진짜 최최종.csv"

if not os.path.exists(file_name):
    if os.path.exists(f"../{file_name}"):
        file_name = f"../{file_name}"
    else:
        st.error(f"❌ 데이터 파일 `{file_name}`을 찾을 수 없습니다.")
        st.stop()

try:
    df = pd.read_csv(file_name, encoding='utf-8')
except UnicodeDecodeError:
    try:
        df = pd.read_csv(file_name, encoding='cp949')
    except Exception:
        df = pd.read_csv(file_name, encoding='utf-8-sig')

# 전처리
df.columns = df.columns.str.strip()
target_col = "상권분류" if "상권분류" in df.columns else df.columns[0]
df[target_col] = df[target_col].astype(str).str.strip()

seongpo_df = df[df[target_col].str.contains("성포", na=False)].head(100).copy()
jungang_df = df[df[target_col].str.contains("중앙", na=False)].head(100).copy()

# 3. PPDAC 기반 사이드바 스토리 내비게이션
st.sidebar.markdown("# 🧭 PPDAC 프로세스")
page = st.sidebar.radio(
    "통계적 문제해결 단계를 선택하세요",
    ["📍 1. Problem & Plan (문제 및 계획)", 
     "📂 2. Data (데이터 수집 및 정제)", 
     "🧪 3. Analysis (가설 검증 및 분석)", 
     "💡 4. Conclusion (비즈니스 활성화 전략)"],
    key="ppdac_navigation_business"
)
st.sidebar.markdown("---")
st.sidebar.caption("성포동 상권 타겟 확장 탐구 v8.0")


# ==========================================
# Page 1. Problem & Plan (문제 정의 및 계획)
# ==========================================
if page == "📍 1. Problem & Plan (문제 및 계획)":
    st.markdown("<h1>📍 1. Problem & Plan <span class='badge'>Step 1 & 2</span></h1>", unsafe_allow_html=True)
    st.markdown("##### 성포동 상권의 청소년 타겟 확장을 위한 탐구 배경과 가설을 설정합니다.")
    
    st.markdown("""
    <div class="ppdac-box">
        <h3>❓ 1. 연구 질문 및 가설 설정 (Problem)</h3>
        <ul>
            <li><b>연구 질문:</b> 성포동 상권이 하교 후 중앙동으로 유출되는 10대 청소년 고객층을 붙잡고, 이들을 새로운 타겟층으로 유입시킬 수 있는 방법은 무엇일까?</li>
            <li><b>핵심 가설:</b> 성포동 상권 매장들의 주타겟층과 가격 구조가 10대의 지불 능력과 맞지 않아 외면받고 있을 것이며, 적정 가성비 서브 메뉴 도입과 업종 다변화 전략을 통해 10대 수요를 확보할 수 있을 것이다.</li>
        </ul>
    </div>
    
    <div class="ppdac-box">
        <h3>📋 2. 통계 분석 및 데이터 수집 설계 (Plan)</h3>
        <ul>
            <li><b>분석 대상 범위:</b> `진짜 최최종.csv` 데이터를 기반으로 성포동과 중앙동 매장의 가격 분포 및 주타겟층 구성 정밀 대조</li>
            <li><b>주요 측정 변수:</b> 업종별 평균가격(수치형), 주타겟층(범주형) 분포 분석을 통한 가격 장벽 도출</li>
            <li><b>최종 목적 및 활용 방안:</b> 성포동 소상공인 및 상인회에 10대 소비층 유치를 위한 적정 가격 가이드라인과 청소년 친화 마케팅 전략 제안</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# Page 2. Data (데이터 수집 및 정제)
# ==========================================
elif page == "📂 2. Data (데이터 수집 및 정제)":
    st.markdown("<h1>📂 2. Data Collection & Cleaning <span class='badge'>Step 3</span></h1>", unsafe_allow_html=True)
    st.markdown("##### 상권 분석의 기초가 되는 변수와 데이터셋 구성을 검증합니다.")
    
    st.markdown(f"### 📊 분석 데이터 원본 확인 (총 {len(df)}개 점포 표본)")
    st.dataframe(df, use_container_width=True)
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🔢 데이터 변수 정의")
        variable_data = pd.DataFrame({
            "변수명": ["가게이름", "상권분류", "업종분류", "평균가격", "주타겟층"],
            "역할": ["식별자", "대조 집단", "인프라 분석", "진입 장벽 분석", "시장 확장성 분석"]
        })
        st.table(variable_data)
        
    with c2:
        st.markdown("### 🛠️ 데이터 정제 프로세스")
        st.markdown("""
        * **10대 수용력 분석 전처리:** 주타겟층 데이터 내에 '10대' 텍스트 포함 여부를 기준으로 매장의 청소년 접근성을 필터링할 수 있도록 텍스트 표준화 완료.
        * **상권 균형화:** 성포동과 중앙동에서 각각 100개씩의 균등 표본을 추출하여 데이터 집계 오류 방지.
        """)


# ==========================================
# Page 3. Analysis (가설 검증 및 분석)
# ==========================================
elif page == "🧪 3. Analysis (가설 검증 및 분석)":
    st.markdown("<h1>🧪 3. Statistical Analysis <span class='badge'>Step 4</span></h1>", unsafe_allow_html=True)
    st.markdown("##### 성포동 상권이 10대를 흡수하기 위해 극복해야 할 경제적/구조적 장벽을 분석합니다.")
    
    tab1, tab2 = st.tabs(["📊 상권별 업종 구조 대조", "💰 10대 유치 가능한 적정 가격대 실험"])
    
    with tab1:
        st.markdown("### 상권 업종 다변화를 위한 구성 비율 분석")
        col_sp, col_ja = st.columns(2)
        
        with col_sp:
            if not seongpo_df.empty and "업종분류" in seongpo_df.columns:
                sp_c = seongpo_df["업종분류"].value_counts().reset_index()
                sp_c.columns = ["업종분류", "점포수"]
                fig1 = px.pie(sp_c, values='점포수', names='업종분류', hole=0.3, title="🏫 성포동 상권 현황 (고가외식/성인 중심)")
                st.plotly_chart(fig1, use_container_width=True)
        
        with col_ja:
            if not jungang_df.empty and "업종분류" in jungang_df.columns:
                ja_c = jungang_df["업종분류"].value_counts().reset_index()
                ja_c.columns = ["업종분류", "점포수"]
                fig2 = px.pie(ja_c, values='점포수', names='업종분류', hole=0.3, title="🛍 ...중앙동 상권 현황 (학생편의/카페 중심)")
                st.plotly_chart(fig2, use_container_width=True)
                
        st.info("💡 **인사이트:** 성포동 상권은 가족·직장인 타겟 점포가 밀집되어 있어 10대들이 방과 후 소비할 매장 자체가 부족합니다. 상권 내 '학생편의' 및 '저가 디저트' 업종의 전략적 유치가 필요함을 시사합니다.")

    with tab2:
        st.markdown("### 💵 비즈니스 시뮬레이션: 가격 조정에 따른 10대 고객 수용력 변화")
        user_budget = st.slider("💰 성포동 매장의 10대 타겟 메뉴 가격 가이드라인 설정 (원)", 1000, 30000, 8500, step=500, key="business_slider")
        
        sp_count = len(seongpo_df[(seongpo_df["평균가격"] <= user_budget) & (seongpo_df["주타겟층"].astype(str).str.contains("10"))])
        ja_count = len(jungang_df[(jungang_df["평균가격"] <= user_budget) & (jungang_df["주타겟층"].astype(str).str.contains("10"))])
        
        sim_data = pd.DataFrame({
            "상권": ["성포고 주변 상권", "중앙동 로데오 상권"], 
            "10대 수용 가능 매장 수": [sp_count, ja_count]
        })
        
        fig_bar = px.bar(sim_data, x="10대 수용 가능 매장 수", y="상권", orientation='h', color="상권",
                         color_discrete_sequence=["#F59E0B", "#3B82F6"], range_x=[0, 100])
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.warning(f"📈 **분석 결과:** 현재 성포동은 메뉴 단가를 **{user_budget:,}원** 이하로 설정하고 10대를 타겟팅하는 매장이 {sp_count}개에 불과합니다. 성포동 매장들이 10대 신규 고객을 유치하려면 지갑 사정이 가벼운 청소년층을 위한 '만원 이하의 서브/사이드 메뉴' 구성이 필수적입니다.")


# ==========================================
# Page 4. Conclusion (비즈니스 활성화 전략)
# ==========================================
elif page == "💡 4. Conclusion (비즈니스 활성화 전략)":
    st.markdown("<h1>💡 4. Conclusion & Business Plan <span class='badge'>Step 5</span></h1>", unsafe_allow_html=True)
    st.markdown("##### 데이터 기반의 분석 결과를 종합하여 성포동 상권의 10대 타겟 확장 전략을 제안합니다.")
    
    all_categories = df["업종분류"].unique() if "업종분류" in df.columns else []
    if not seongpo_df.empty and not jungang_df.empty and len(all_categories) > 0:
        sp_v = seongpo_df["업종분류"].value_counts().reindex(all_categories, fill_value=0)
        ja_v = jungang_df["업종분류"].value_counts().reindex(all_categories, fill_value=0)
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=sp_v.values, theta=all_categories, fill='toself', name='성포고 주변 (보완 필요)'))
        fig_radar.add_trace(go.Scatterpolar(r=ja_v.values, theta=all_categories, fill='toself', name='중앙동 로데오 (벤치마킹)'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True)), title="📊 성포동 상권의 업종 갭(Gap) 및 벤치마킹 포인트")
        st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("---")
    
    st.markdown("<h2>📈 성포동 상권 활성화 솔루션: 10대 고객층 락인(Lock-in) 방안</h2>", unsafe_allow_html=True)
    
    st.success("""
    **최종 비즈니스 제언 리포트**
    
    빅데이터 분석 결과, 성포동 상권이 청소년을 놓치고 있는 핵심 원인은 **'높은 가격 장벽'**과 **'10대 전용 상품의 부재'**에 있습니다. 중앙동으로 빠져나가는 학생 인구를 붙잡고 상권의 활력을 높이기 위해, 성포동 소상공인과 상인회는 기존 성인 중심의 비즈니스 모델에 **청소년 타겟 전략을 결합하는 '하이브리드 상권'**으로 전환해야 합니다.
    """)
    
    st.markdown("""
    <div class="conclusion-box">
        <h3>🎯 성포동 소상공인을 위한 3대 핵심 실천 전략 (Action Plan)</h3>
        <ol>
            <li><b>청소년 특화 '가성비 서브 메뉴' 출시:</b> 기존 고가 음식점이나 카페에서 하교 시간(15시~18시) 한정으로 10대들이 부담 없이 결제할 수 있는 5,000원~8,000원 사이의 미니 메뉴나 세트 상품을 개발합니다.</li>
            <li><b>업종의 청소년 친화적 다변화 유도:</b> 상권 내 비어있는 공실이나 신규 창업 시, 데이터상 결핍 요소로 나타난 코인노래방, 팬시/문구, 저가 프랜차이즈 디저트 업종의 입점을 적극 권장합니다.</li>
            <li><b>로컬 학생 연계 마케팅 및 쿠폰제 도입:</b> 인근 성포고 등 학교 학생증 인증 시 가격을 할인해 주는 '청소년 우대 매장' 인증제를 도입하고, 학원가와 연계된 동네 상권 전용 모바일 스탬프 제도를 활성화합니다.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
