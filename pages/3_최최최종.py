import streamlit as st
import pandas as pd

# 1. 대시보드 레이아웃 설정 (Wide 모드 및 테마 일관성 유지)
st.set_page_config(page_title="안산 상권 분석 빅데이터 시스템", layout="wide")

# 깔끔한 CSS 스타일 적용 (표 가독성 및 여백 조정)
st.markdown("""
    <style>
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1 { color: #1E3A8A; font-weight: 800; }
    h2 { color: #2563EB; font-weight: 700; border-bottom: 2px solid #E5E7EB; padding-bottom: 10px; }
    h3 { color: #374151; font-weight: 600; }
    div[data-testid="stMetricValue"] { font-size: 32px; font-weight: 700; color: #1D4ED8; }
    </style>
""", unsafe_allow_html=True)

# 2. 데이터 불러오기 함수
@st.cache_data
def load_data():
    return pd.read_csv("ansan_dual_commercial_400.csv")

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 파일(ansan_dual_commercial_400.csv)을 읽는 중 오류가 발생했습니다: {e}")
    st.stop()

# 상권 데이터 분리
seongpo_df = df[df["상권분류"] == "성포고주변"]
jungang_df = df[df["상권분류"] == "중앙동로데오"]

# 3. 사이드바 내비게이션 (깔끔하고 직관적으로 정돈)
st.sidebar.markdown("## 📂 분석 목차")
page = st.sidebar.radio(
    "이동할 페이지를 선택하세요",
    ["🏫 성포고 주변 상권 현황", 
     "🛍️ 중앙동 로데오 상권 현황", 
     "💳 예산 및 연령 맞춤형 추천", 
     "💡 종합 결론: 10대 이동 원인"]
)
st.sidebar.markdown("---")
st.sidebar.caption("안산시 청소년 상권 이동 패턴 분석 프로젝트 v2.0")

# ==========================================
# Page 1. 성포고 주변 상권 현황
# ==========================================
if page == "🏫 성포고 주변 상권 현황":
    st.title("🏫 성포고등학교 주변 상권 분석")
    st.markdown("##### 학교 앞 주거 배후 상권의 업종 구성과 전체 상점 데이터를 시각화합니다.")
    
    # 상단 요약 지표 리포트
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("총 분석 점포 수", f"{len(seongpo_df)} 개")
    with m2:
        st.metric("평균 단가(가격대)", f"{int(seongpo_df['평균가격'].mean()):,} 원")
    with m3:
        st.metric("가장 많은 업종", seongpo_df["업종분류"].value_counts().index[0])
        
    st.markdown("### 📊 데이터 상세 보기")
    tab1, tab2 = st.tabs(["📂 업종별 통계 요약", "📄 상점 원본 데이터 (200선)"])
    
    with tab1:
        sp_counts = seongpo_df["업종분류"].value_counts().reset_index()
        sp_counts.columns = ["업종분류", "점포 수(개)"]
        st.dataframe(sp_counts, use_container_width=True, hide_index=True)
        
    with tab2:
        # 데이터프레임 높이를 조절하고 index를 숨겨 깔끔하게 처리
        st.dataframe(seongpo_df[["가게이름", "업종분류", "대표메뉴", "평균가격", "주타겟층"]], 
                     use_container_width=True, height=400, hide_index=True)


# ==========================================
# Page 2. 중앙동 로데오 상권 현황
# ==========================================
elif page == "🛍️ 중앙동 로데오 상권 현황":
    st.title("🛍️ 중앙동 로데오 상권 분석")
    st.markdown("##### 안산 최대 거점 중심 상권의 업종 구성과 전체 상점 데이터를 시각화합니다.")
    
    # 상단 요약 지표 리포트
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("총 분석 점포 수", f"{len(jungang_df)} 개")
    with m2:
        st.metric("평균 단가(가격대)", f"{int(jungang_df['평균가격'].mean()):,} 원")
    with m3:
        st.metric("가장 많은 업종", jungang_df["업종분류"].value_counts().index[0])
        
    st.markdown("### 📊 데이터 상세 보기")
    tab1, tab2 = st.tabs(["📂 업종별 통계 요약", "📄 상점 원본 데이터 (200선)"])
    
    with tab1:
        ja_counts = jungang_df["업종분류"].value_counts().reset_index()
        ja_counts.columns = ["업종분류", "점포 수(개)"]
        st.dataframe(ja_counts, use_container_width=True, hide_index=True)
        
    with tab2:
        st.dataframe(jungang_df[["가게이름", "업종분류", "대표메뉴", "평균가격", "주타겟층"]], 
                     use_container_width=True, height=400, hide_index=True)


# ==========================================
# Page 3. 조건별 맞춤 점포 추천 (예산 x 연령)
# ==========================================
elif page == "💳 예산 및 연령 맞춤형 추천":
    st.title("💳 소비자 조건별 상권 시뮬레이터")
    st.markdown("##### 지갑 사정(예산)과 연령 조건을 설정하여 각 상권에서 진입 가능한 매장을 비교합니다.")
    
    # 입력 필터를 깔끔한 박스 형태로 상단에 배치
    with st.container(border=True):
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            user_budget = st.slider("💰 지불 가능한 최대 예산 설정 (원)", 1000, 30000, 8000, step=500)
        with col_in2:
            age_options = ["10-20대", "10-30대", "20-40대", "30-50대", "40-60대"]
            user_ages = st.multiselect("👥 선호하는 매장의 주 타겟층 선택", age_options, default=["10-20대", "10-30대"])

    # 조건 필터링 로직
    def filter_shops(target_df):
        res = target_df[target_df["평균가격"] <= user_budget]
        if user_ages:
            res = res[res["주타겟층"].isin(user_ages)]
        return res

    sp_recommend = filter_shops(seongpo_df)
    ja_recommend = filter_shops(jungang_df)

    # 결과 지표 대조
    st.markdown("### 📊 조건 매칭 결과 비교")
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric("🏫 성포고 주변 추천 점포", f"{len(sp_recommend)} 개 / 200개")
    with res_col2:
        st.metric("🛍️ 중앙동 로데오 추천 점포", f"{len(ja_recommend)} 개 / 200개")

    # 결과 표를 좌우 2열로 배치하고 index를 숨겨 조잡함을 제거
    st.markdown("---")
    col_table1, col_table2 = st.columns(2)
    with col_table1:
        st.markdown("**🏫 성포고 주변 매장 리스트**")
        if len(sp_recommend) > 0:
            st.dataframe(sp_recommend[["가게이름", "업종분류", "대표메뉴", "평균가격"]], use_container_width=True, height=350, hide_index=True)
        else:
            st.info("조건에 만족하는 매장이 이 지역에 없습니다.")
            
    with col_table2:
        st.markdown("**🛍️ 중앙동 로데오 매장 리스트**")
        if len(ja_recommend) > 0:
            st.dataframe(ja_recommend[["가게이름", "업종분류", "대표메뉴", "평균가격"]], use_container_width=True, height=350, hide_index=True)
        else:
            st.info("조건에 만족하는 매장이 이 지역에 없습니다.")


# ==========================================
# Page 4. 종합 결론: 10
