import streamlit as st
import pandas as pd

# 1. 기본 페이지 세팅
st.set_page_config(page_title="안산 상권 비교 탐구 프로젝트", layout="wide")

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

# 3. 사이드바 내비게이션 (페이지 이동 컨트롤러)
st.sidebar.title("📌 프로젝트 목차")
page = st.sidebar.radio(
    "이동할 페이지를 선택하세요",
    ["Page 1. 성포고 주변 상권 현황", 
     "Page 2. 중앙동 로데오 상권 현황", 
     "Page 3. 조건별 맞춤 점포 추천 (예산x연령)", 
     "Page 4. 종합 결론: 10대 이동 원인 규명"]
)

st.sidebar.markdown("---")

# ==========================================
# Page 1. 성포고 주변 상권 현황
# ==========================================
if page == "Page 1. 성포고 주변 상권 현황":
    st.title("🏫 Page 1. 성포고등학교 주변 상권 분석")
    st.markdown("#### **학교 앞 배후 상권의 업종 구성과 특징을 확인합니다.**")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("📊 업종별 점포 수")
        sp_counts = seongpo_df["업종분류"].value_counts()
        st.dataframe(sp_counts.rename("점포 수(개)"))
        
        st.subheader("💰 평균 가격대")
        avg_price = seongpo_df["평균가격"].mean()
        st.metric(label="성포고 상권 전체 평균 가격", value=f"{int(avg_price):,} 원")
        
    with col2:
        st.subheader("🛒 성포고 주변 전체 상점 리스트 (200선)")
        st.dataframe(seongpo_df[["가게이름", "업종분류", "대표메뉴", "평균가격", "주타겟층"]], use_container_width=True, height=450)


# ==========================================
# Page 2. 중앙동 로데오 상권 현황
# ==========================================
elif page == "Page 2. 중앙동 로데오 상권 현황":
    st.title("🛍️ Page 2. 중앙동 로데오 상권 분석")
    st.markdown("#### **안산 최대 중심 거점 상권의 업종 구성과 특징을 확인합니다.**")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("📊 업종별 점포 수")
        ja_counts = jungang_df["업종분류"].value_counts()
        st.dataframe(ja_counts.rename("점포 수(개)"))
        
        st.subheader("💰 평균 가격대")
        avg_price_ja = jungang_df["평균가격"].mean()
        st.metric(label="중앙동 상권 전체 평균 가격", value=f"{int(avg_price_ja):,} 원")
        
    with col2:
        st.subheader("🛒 중앙동 로데오 전체 상점 리스트 (200선)")
        st.dataframe(jungang_df[["가게이름", "업종분류", "대표메뉴", "평균가격", "주타겟층"]], use_container_width=True, height=450)


# ==========================================
# Page 3. 조건별 맞춤 점포 추천 (예산 x 연령 조건 추가)
# ==========================================
elif page == "Page 3. 조건별 맞춤 점포 추천 (예산x연령)":
    st.title("💳 Page 3. 예산 및 연령 맞춤형 상권 시뮬레이터")
    st.markdown("#### **소비자의 지갑 사정(예산)과 연령 조건을 조합하여 이용 가능한 매장을 실시간 필터링합니다.**")
    
    # 상단 조건 입력창
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        user_budget = st.slider("최대 지불 가능한 예산 설정 (원)", 1000, 30000, 8000, step=500)
    with col_input2:
        # 주타겟층 조건 다중 선택 가능하게 설정
        age_options = ["10-20대", "10-30대", "20-40대", "30-50대", "40-60대"]
        user_ages = st.multiselect("원하는 매장의 주 타겟 연령층 선택 (중복 가능)", age_options, default=["10-20대", "10-30대"])

    # 조건 필터링 로직 구동
    def filter_shops(target_df):
        # 1. 가격 필터
        res = target_df[target_df["평균가격"] <= user_budget]
        # 2. 연령 필터 (선택한 연령 리스트 중 하나라도 포함되어 있으면 매칭)
        if user_ages:
            res = res[res["주타겟층"].isin(user_ages)]
        return res

    sp_recommend = filter_shops(seongpo_df)
    ja_recommend = filter_shops(jungang_df)

    # 필터링 결과 매트릭스 시각화
    st.markdown("---")
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.subheader("🏫 성포고 주변 추천 매장")
        st.metric(label="조건 만족 점포 수", value=f"{len(sp_recommend)} 개 / 200개")
        st.dataframe(sp_recommend[["가게이름", "업종분류", "대표메뉴", "평균가격", "주타겟층"]], use_container_width=True)
        
    with col_res2:
        st.subheader("🛍️ 중앙동 로데오 추천 매장")
        st.metric(label="조건 만족 점포 수", value=f"{len(ja_recommend)} 개 / 200개")
        st.dataframe(ja_recommend[["가게이름", "업종분류", "대표메뉴", "평균가격", "주타겟층"]], use_container_width=True)


# ==========================================
# Page 4. 종합 결론: 10대 이동 원인 규명
# ==========================================
elif page == "Page 4. 종합 결론: 10대 이동 원인 규명":
    st.title("💡 Page 4. 왜 10대 학생들은 중앙동으로 갈까?")
    st.markdown("#### **400개 상권 데이터 분석을 통해 도출한 경영·경제학적 최종 리포트**")
    
    # 시각화: 두 상권 업종 구성 비교 차트
    st.subheader("📈 [핵심 증거] 두 상권의 업종 분포 시각화 대조")
    sp_chart = seongpo_df["업종분류"].value_counts().rename("성포고주변")
    ja_chart = jungang_df["업종분류"].value_counts().rename("중앙동로데오")
    total_chart = pd.concat([sp_chart, ja_chart], axis=1).fillna(0)
    st.bar_chart(total_chart)
    
    st.markdown("---")
    
    # 경영학적 인사이트 리포트 내용 작성
    st.subheader("📝 데이터 기반 탐구 결론")
    
    st.markdown("""
    ### 1. 상권 공급의 모순과 '수요-공급 미스매치'
    - **성포고 주변 상권**은 아파트 단지와 학교가 밀집하여 10대 학령인구(수요)가 매우 많음에도 불구하고, 실제 상가 공급은 **고가음식점, 일반음식점, 유흥/성인** 업종의 비율이 높습니다. 이는 구매력이 높은 40-50대 부모 세대를 타겟팅한 결과입니다.
    - 정작 매일 유동인구로 존재하는 10대 학생들은 학교 앞에서 소비할 수 있는 인프라가 극히 제한되는 **상권 소외 현상**을 겪고 있음이 데이터로 입증됩니다.
    
    ### 2. 중앙동의 '원스톱 소비 클러스터(Cluster) 효과'
    - 그래프에서 보듯 **중앙동 로데오 상권**은 **학생편의(네컷사진, 코인노래방, 보드게임방)** 및 **카페/디저트, 패션/쇼핑** 업종이 압도적인 밀집도를 보여줍니다.
    - 10대 학생들은 용돈 예산(주로 8,000원~15,000원 선) 안에서 **[식사 -> 디저트 -> 놀이 -> 쇼핑]**을 한 구역에서 모두 해결할 수 있는 **'원스톱 가성비 소비'** 환경을 누리기 위해 버스비나 교통시간이라는 물리적 비용을 감수하고 중앙동으로 이동하는 것입니다.
    
    ### 3. 합리적 소비자 행동 이론의 증명
    - 결론적으로 청소년들이 중앙동에 몰리는 현상은 단순한 유흥 목적이나 일탈이 아닙니다. 자신들에게 주어진 한정된 자원(용돈 예산) 안에서 효용을 극대화하려는 **'합리적 소비자 행동 이론(Consumer Behavior Theory)'**이 지리적 이동 패턴으로 표출된 결과물입니다.
    """)
