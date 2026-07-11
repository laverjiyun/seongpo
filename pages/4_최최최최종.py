import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# 1. 페이지 레이아웃 및 웹 브라우저 탭 설정 (앱 최상단 고정)
st.set_page_config(page_title="PPDAC 청소년 상권 분석", layout="wide")

# 세련된 데이터 과학 대시보드 테마 CSS
st.markdown("""
    <style>
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1 { color: #1E3A8A; font-weight: 800; }
    h2 { color: #2563EB; font-weight: 700; border-bottom: 2px solid #E5E7EB; padding-bottom: 10px; margin-top: 25px; }
    h3 { color: #1E3A8A; font-weight: 600; margin-top: 15px; }
    div[data-testid="stMetricValue"] { font-size: 32px; font-weight: 700; color: #1D4ED8; }
    
    /* PPDAC 단계별 이정표 스타일 */
    .ppdac-box {
        background-color: #F8FAFC;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 20px;
        line-height: 1.7;
    }
    .conclusion-box {
        background-color: #EFF6FF;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #BFDBFE;
        line-height: 1.8;
    }
    .badge {
        background-color: #3B82F6; color: white; padding: 3px 8px; 
        border-radius: 5px; font-size: 12px; font-weight: bold; vertical-align: middle;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 데이터 안전 로딩 (캐시 충돌 제거 및 물리 복사)
file_name = "ansan_commercial_cleaned_final.csv"

if not os.path.exists(file_name):
    st.error(f"❌ 데이터 파일 `{file_name}`을 찾을 수 없습니다. app.py와 같은 폴더에 넣어주세요.")
    st.stop()

# 매번 안전하게 동적 로딩하여 세션 꼬임 방지
df = pd.read_csv(file_name)

if "상권분류" in df.columns:
    df["상권분류"] = df["상권분류"].astype(str).str.strip()

# 데이터 참조 에러 원천 차단을 위한 .copy() 처리 및 100개 제한
seongpo_df = df[df["상권분류"].str.contains("성포", na=False)].head(100).copy()
jungang_df = df[df["상권분류"].str.contains("중앙", na=False)].head(100).copy()


# 3. PPDAC 기반 사이드바 스토리 내비게이션 (고유 key 적용)
st.sidebar.markdown("# 🧭 PPDAC 프로세스")
page = st.sidebar.radio(
    "통계적 문제해결 단계를 선택하세요",
    ["📍 1. Problem & Plan (문제 및 계획)", 
     "📂 2. Data (데이터 수집 및 정제)", 
     "🧪 3. Analysis (가설 검증 및 분석)", 
     "💡 4. Conclusion (인사이트 및 결론)"],
    key="ppdac_navigation"
)
st.sidebar.markdown("---")
st.sidebar.caption("안산시 청소년 로컬 정책 연구 대시보드 v7.0")


# ==========================================
# Page 1. Problem & Plan (문제 정의 및 계획)
# ==========================================
if page == "📍 1. Problem & Plan (문제 및 계획)":
    st.title("📍 1. Problem & Plan <span class='badge'>Step 1 & 2</span>", unsafe_allow_html=True)
    st.markdown("##### 탐구 질문을 설정하고 이를 통계적으로 검증하기 위한 구체적인 연구 계획을 수립합니다.")
    
    st.markdown("""
    <div class="ppdac-box">
        <h3>❓ 1. 연구 질문 및 가설 설정 (Problem)</h3>
        <ul>
            <li><b>연구 질문:</b> 안산시 주거 밀집 지역(성포동) 청소년들은 왜 하교 후 동네를 벗어나 중심상권(중앙동)으로 이탈할까?</li>
            <li><b>핵심 가설:</b> 성포동 상권의 높은 가격 장벽과 성인 중심 업종 구성이 10대 청소년들을 경제적·문화적으로 소외시키고 있을 것이다.</li>
        </ul>
    </div>
    
    <div class="ppdac-box">
        <h3>📋 2. 통계 분석 및 데이터 수집 설계 (Plan)</h3>
        <ul>
            <li><b>분석 대상 범위:</b> 안산시 성포고 주변 배후 상권 매장 100개 vs 중앙동 로데오거리 매장 100개 (총 200개 실존 점포 대조)</li>
            <li><b>주요 측정 변수:</b> 업종분류(범주형), 평균가격(수치형), 주타겟층(범주형) 간의 관계 및 분포 분석</li>
            <li><b>최종 목적 및 활용 방안:</b> 검증된 데이터를 기반으로 안산시청에 '주거 밀집 지역 내 공공 청소년 쉼터 인프라' 조성을 촉구하는 정책 근거로 활용</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 사이드바에서 '2. Data' 단계를 클릭하여 수집된 데이터의 형태를 확인해 보세요.")


# ==========================================
# Page 2. Data (데이터 수집 및 정제)
# ==========================================
elif page == "📂 2. Data (데이터 수집 및 정제)":
    st.title("📂 2. Data Collection & Cleaning <span class='badge'>Step 3</span>", unsafe_allow_html=True)
    st.markdown("##### 구글 맵 API를 기반으로 정제된 숫자 및 범주형 데이터의 프로필을 확인합니다.")
    
    st.markdown("### 📊 수집 데이터 프레임 샘플 (상위 200개 샘플 중 일부)")
    st.dataframe(df.head(10), use_container_width=True)
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🔢 데이터 변수 속성 정의 (Variable Dictionary)")
        variable_data = pd.DataFrame({
            "변수명": ["가게이름", "상권분류", "업종분류", "평균가격", "주타겟층"],
            "데이터 형태": ["문자형 (Text)", "범주형 (Category)", "범주형 (Category)", "수치형 (Integer)", "범주형 (Category)"],
            "설명": ["매장의 상호명", "성포고주변 / 중앙동로데오", "카페, 고가음식점, 학생편의 등", "매장의 메뉴 평균 단가", "10대, 성인층 등 주 소비층"]
        })
        st.table(variable_data)
        
    with c2:
        st.markdown("### 🛠️ 데이터 정제(Data Cleaning) 프로세스")
        st.markdown("""
        1. **텍스트 노이즈 제거:** 구글 맵 매장 데이터 전처리 과정에서 발생한 문자열 좌우 공백 제거(`str.strip()`).
        2. **수치 데이터 확보:** 메뉴판 크롤링 데이터를 기반으로 결측치를 정제하여 신뢰할 수 있는 `평균가격` 변수 생성.
        3. **타겟층 세분화:** 상권 분석 목적에 맞추어 주 소비 타겟층을 '10대 포함 여부'로 이진 범주화 유도.
        """)


# ==========================================
# Page 3. Analysis (가설 검증 및 분석)
# ==========================================
elif page == "🧪 3. Analysis (가설 검증 및 분석)":
    st.title("🧪 3. Statistical Analysis <span class='badge'>Step 4</span>", unsafe_allow_html=True)
    st.markdown("##### 두 상권의 업종 구성과 가격 데이터를 대조하여 설정한 가설을 통계적으로 검증합니다.")
    
    # 상권 선택 탭 분리
    tab1, tab2 = st.tabs(["📊 상권별 업종 구조 대조", "💰 경제적 예산 수용력 실험"])
    
    with tab1:
        st.markdown("### 두 상권의 근본적인 업종 구성 시각화 대조")
        col_sp, col_ja = st.columns(2)
        
        with col_col1 := col_sp:
            if not seongpo_df.empty:
                sp_c = seongpo_df["업종분류"].value_counts().reset_index()
                sp_c.columns = ["업종분류", "점포수"]
                fig1 = px.pie(sp_c, values='점포수', names='업종분류', hole=0.3, title="🏫 성포동 상권 업종 비율 (100개)")
                st.plotly_chart(fig1, use_container_width=True)
        
        with col_col2 := col_ja:
            if not jungang_df.empty:
                ja_c = jungang_df["업종분류"].value_counts().reset_index()
                ja_c.columns = ["업종분류", "점포수"]
                fig2 = px.pie(ja_c, values='점포수', names='업종분류', hole=0.3, title="🛍️ 중앙동 상권 업종 비율 (100개)")
                st.plotly_chart(fig2, use_container_width=True)
                
        st.info("📊 **통계적 패턴 요약:** 성포동은 고가음식점·일반음식점 등 성인/가족 중심 업종이 과반인 반면, 중앙동은 카페/디저트 및 학생편의 업종이 클러스터를 이루고 있습니다.")

    with tab2:
        st.markdown("### 💵 가설 검증: 학생 지출 예산 한도별 점포 수 시뮬레이션")
        user_budget = st.slider("💰 학생 1인당 지출 예산 한도 설정 (원)", 1000, 30000, 8500, step=500, key="analysis_slider")
        
        # 10대 타겟 + 예산 이하 매장 카운트
        sp_count = len(seongpo_df[(seongpo_df["평균가격"] <= user_budget) & (seongpo_df["주타겟층"].astype(str).str.contains("10"))])
        ja_count = len(jungang_df[(jungang_df["평균가격"] <= user_budget) & (jungang_df["주타겟층"].astype(str).str.contains("10"))])
        
        sim_data = pd.DataFrame({
            "상권": ["성포고 주변 상권", "중앙동 로데오 상권"], 
            "청소년 수용 가능 매장 수": [sp_count, ja_count]
        })
        
        fig_bar = px.bar(sim_data, x="청소년 수용 가능 매장 수", y="상권", orientation='h', color="상권",
                         color_discrete_sequence=["#F59E0B", "#3B82F6"], range_x=[0, 100])
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.warning(f"💡 **가설 검증 결과:** 예산을 청소년 평균 지갑 사정(예: 8,000원 내외)으로 낮출수록 성포동에서 진입 가능한 매장은 급격히 소멸합니다. 이는 성포동의 높은 가격 장벽이 청소년 이탈을 유도한다는 가설을 명백히 증명합니다.")


# ==========================================
# Page 4. Conclusion (인사이트 및 결론)
# ==========================================
elif page == "💡 4. Conclusion (인사이트 및 결론)":
    st.title("💡 4. Conclusion & Action Plan <span class='badge'>Step 5</span>", unsafe_allow_html=True)
    st.markdown("##### 통계적 해석을 바탕으로 도출된 최종 결론과 안산시청을 향한 정책 제언 리포트입니다.")
    
    # 레이더 차트로 종합 요약 시각화
    all_categories = df["업종분류"].unique() if "업종분류" in df.columns else []
    if not seongpo_df.empty and not jungang_df.empty and len(all_categories) > 0:
        sp_v = seongpo_df["업종분류"].value_counts().reindex(all_categories, fill_value=0)
        ja_v = jungang_df["업종분류"].value_counts().reindex(all_categories, fill_value=0)
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=sp_v.values, theta=all_categories, fill='toself', name='성포고 주변 (주거지)'))
        fig_radar.add_trace(go.Scatterpolar(r=ja_v.values, theta=all_categories, fill='toself', name='중앙동 로데오 (중심지)'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True)), title="📊 데이터가 말하는 진실: 상권 인프라 미스매치 종합 대조")
        st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("---")
    
    # 정책 제언 섹션
    st.markdown("## 🏛️ 안산시청 정책 제언: 주거 밀집 지역 내 '공공 청소년 쉼터' 조성 촉구")
    
    st.success("""
    **데이터 분석 결과 기반 최종 정책 리포트**
    
    구글 맵 데이터 분석 결과, 성포동 상권은 높은 평균 단가와 성인 중심 업종으로 인해 10대 청소년들이 갈 만한 공간이 극도로 부족함이 증명되었습니다. 
    학생들이 하교 후 멀리 떨어진 중앙동으로 이탈하는 문제를 해결하기 위해, 안산시청은 성포동 등 주거 밀집 지역 내에 공공 청소년 스터디카페나 문화 쉼터를 즉각 조성해야 합니다. 
    
    이는 청소년들에게 안전하고 저렴한 공간을 제공하는 동시에, 인근 가성비 로컬 점포들과 연계하여 침체된 배후 상권까지 심폐소생할 수 있는 가장 확실하고 실효성 있는 킬러 정책이 될 것입니다.
    """)
    
    st.markdown("""
    <div class="conclusion-box">
        <h3>🎯 분석 요약 및 기대효과 (Action Plan)</h3>
        <ol>
            <li><b>청소년 생활권 보장:</b> 동네 상권에서 소외당하던 10대들에게 안전하고 유익한 방과 후 인프라 제공</li>
            <li><b>지역 경제 선순환:</b> 공공 쉼터 이용 청소년들이 성포동 내 가성비 local 점포(분식, 문구 등) 연계 소비 유도</li>
            <li><b>이동 안전망 구축:</b> 교통 혼잡 및 원거리 이동 중 발생할 수 있는 안전사고 발생 가능성 차단</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
