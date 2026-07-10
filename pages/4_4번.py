import sys
!{sys.executable} -m pip install streamlit
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 레이아웃 설정
st.set_page_config(page_title="안산 상권 빅데이터 분석", layout="wide")

# 깔끔한 대시보드 테마 CSS
st.markdown("""
    <style>
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1 { color: #1E3A8A; font-weight: 800; }
    h2 { color: #2563EB; font-weight: 700; border-bottom: 2px solid #E5E7EB; padding-bottom: 10px; }
    div[data-testid="stMetricValue"] { font-size: 32px; font-weight: 700; color: #1D4ED8; }
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

# 3. 사이드바 목차
st.sidebar.markdown("## 📂 분석 목차")
page = st.sidebar.radio(
    "이동할 페이지를 선택하세요",
    ["🏫 성포고 주변 상권 현황",
     "🛍️ 중앙동 로데오 상권 현황",
     "🧪 상권별 청소년 수용력 실험",
     "💡 종합 결론: 10대 이동 원인"]
)
st.sidebar.markdown("---")
st.sidebar.caption("안산시 청소년 상권 이동 패턴 분석 프로젝트 v4.1")

# ==========================================
# Page 1. 성포고 주변 상권 현황 (Plotly 내장 도넛 차트)
# ==========================================
if page == "🏫 성포고 주변 상권 현황":
    st.title("🏫 성포고등학교 주변 상권 분석")
    st.markdown("##### 학교 정문 앞 및 배후지 200개 매장의 업종 구성 비율을 그래프로 시각화합니다.")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("총 분석 점포 수", f"{len(seongpo_df)} 개")
    with m2:
        st.metric("상권 평균 단가", f"{int(seongpo_df['평균가격'].mean()):,} 원")
    with m3:
        st.metric("가장 밀집된 업종", seongpo_df["업종분류"].value_counts().index[0])

    st.markdown("---")

    # 폰트 에러 없는 Plotly 도넛 차트
    sp_counts = seongpo_df["업종분류"].value_counts().reset_index()
    sp_counts.columns = ["업종분류", "점포수"]

    fig = px.pie(sp_counts, values='점포수', names='업종분류', hole=0.4,
                 title="성포고 주변 상권 업종 구성 비율",
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=False, margin=dict(t=50, b=20, l=20, r=20))

    col_chart, col_info = st.columns([2, 1])
    with col_chart:
        st.plotly_chart(fig, use_container_width=True)
    with col_info:
        st.markdown("### 📋 그래프 주요 특징")
        st.write("- **고가음식점 및 일반음식점**이 상권의 절반 이상을 차지합니다.")
        st.write("- 주거지 배후 상권 특성상 부모 세대 중심의 외식 인프라가 짙게 깔려 있습니다.")


# ==========================================
# Page 2. 중앙동 로데오 상권 현황 (Plotly 내장 도넛 차트)
# ==========================================
elif page == "🛍️ 중앙동 로데오 상권 현황":
    st.title("🛍️ 중앙동 로데오 상권 분석")
    st.markdown("##### 안산 최대 중심지인 중앙역 로데오거리 200개 매장의 업종 구성 비율을 그래프로 시각화합니다.")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("총 분석 점포 수", f"{len(jungang_df)} 개")
    with m2:
        st.metric("상권 평균 단가", f"{int(jungang_df['평균가격'].mean()):,} 원")
    with m3:
        st.metric("가장 밀집된 업종", jungang_df["업종분류"].value_counts().index[0])

    st.markdown("---")

    # 폰트 에러 없는 Plotly 도넛 차트
    ja_counts = jungang_df["업종분류"].value_counts().reset_index()
    ja_counts.columns = ["업종분류", "점포수"]

    fig = px.pie(ja_counts, values='점포수', names='업종분류', hole=0.4,
                 title="중앙동 로데오 상권 업종 구성 비율",
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=False, margin=dict(t=50, b=20, l=20, r=20))

    col_chart, col_info = st.columns([2, 1])
    with col_chart:
        st.plotly_chart(fig, use_container_width=True)
    with col_info:
        st.markdown("### 📋 그래프 주요 특징")
        st.write("- **학생편의 및 카페/디저트, 패션/쇼핑**이 핵심 축을 이룹니다.")
        st.write("- 청소년층이 선호하고 쉽게 소비할 수 있는 문화 및 오락 시설이 집약되어 있습니다.")


# ==========================================
# Page 3. 상권별 청소년 수용력 실험 (Plotly 내장 가로 막대 그래프)
# ==========================================
elif page == "🧪 상권별 청소년 수용력 실험":
    st.title("🧪 Page 3. 두 상권의 청소년 유효 수요 수용력 대조 실험")
    st.markdown("##### **동일한 예산 조건을 투입했을 때, 각 상권에서 10대가 '생존(진입) 가능한 점포 수'를 그래프로 대조합니다.**")

    with st.container(border=True):
        user_budget = st.slider("💰 하교 후 고등학생 페르소나의 현실적 지출 예산 (원)", 1000, 30000, 8500, step=500)

    user_ages = ["10-20대", "10-30대"]

    # 필터링 및 카운트
    sp_count = len(seongpo_df[(seongpo_df["평균가격"] <= user_budget) & (seongpo_df["주타겟층"].isin(user_ages))])
    ja_count = len(jungang_df[(jungang_df["평균가격"] <= user_budget) & (jungang_df["주타겟층"].isin(user_ages))])

    # 폰트 에러 없는 Plotly 가로 막대 그래프
    sim_data = pd.DataFrame({
        "상권분류": ["성포고 주변", "중앙동 로데오"],
        "진입 가능 매장 수 (개)": [sp_count, ja_count]
    })

    fig = px.bar(sim_data, x="진입 가능 매장 수 (개)", y="상권분류", orientation='h',
                 text="진입 가능 매장 수 (개)",
                 title=f"{user_budget:,}원 이하 예산 시 상권별 학생 수용력 비교",
                 color="상권분류", color_discrete_sequence=["#ff9999", "#66b3ff"])

    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis=dict(range=[0, 210]), showlegend=False, margin=dict(t=50, b=20, l=20, r=20))

    st.plotly_chart(fig, use_container_width=True)

    st.info(f"💡 **실험 해석:** 슬라이더를 10대 현실 예산 범위로 낮출수록 **성포고 상권 막대 그래프는 급격히 줄어들지만, 중앙동 로데오 그래프는 길게 살아남습니다.** 학생들이 동네에서 갈 곳을 잃어 중앙동으로 밀려나고 있음을 증명하는 정량적 지표입니다.")


# ==========================================
# Page 4. 종합 결론
# ==========================================
elif page == "💡 종합 결론: 10대 이동 원인":
    st.title("💡 Page 4. 데이터로 입증된 청소년 유동인구 이탈 원인")
    st.markdown("##### 400개 실제 매장 데이터를 대조하여 도출한 최종 학술 리포트")

    st.markdown("<h2>📈 두 상권의 업종 분포 비교 (세로 막대 그래프)</h2>", unsafe_allow_html=True)
    sp_chart = seongpo_df["업종분류"].value_counts().rename("성포고 주변")
    ja_chart = jungang_df["업종분류"].value_counts().rename("중앙동 로데오")
    total_chart = pd.concat([sp_chart, ja_chart], axis=1).fillna(0)

    # 스트림릿 내장 기본 차트 (절대 깨지지 않음)
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
