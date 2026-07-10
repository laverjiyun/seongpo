import streamlit as st
import pandas as pd

# 1. 페이지 초기 레이아웃 설정
st.set_page_config(page_title="안산 상권 비교 대시보드", layout="wide")

st.title("🗺️ 성포고 청소년은 왜 중앙동으로 갈까?")
st.markdown("#### **[성포고등학교 주변 상권 vs 중앙동 로데오 상권] 빅데이터 비교 분석**")
st.write("학교 앞 동네 상권과 안산 중심 상권의 가격대 및 업종 분포를 모델링하여 10대 유동인구 쏠림 현상의 원인을 경영학적으로 규명합니다.")

# 2. 데이터 불러오기
try:
    df = pd.read_csv("ansan_commercial_comparison_data.csv")
except:
    st.error("ansan_commercial_comparison_data.csv 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요.")

# 3. 사이드바 제어: 10대 고등학생의 경제력 페르소나 설정
st.sidebar.header("💳 청소년 소비 조건 설정")
budget = st.sidebar.slider("한 끼 식사 및 여가 지불 예산 (원)", 1000, 30000, 8000, step=500)

target_10s = st.sidebar.checkbox("주타겟층이 '10-20대' 또는 '10-30대'인 매장만 보기", value=False)

# 데이터 필터링 기초 가공
if target_10s:
    filtered_df = df[df["주타겟층"].str.contains("10-")]
else:
    filtered_df = df.copy()

# 두 상권 분리
seongpo_all = filtered_df[filtered_df["상권분류"] == "성포고주변"]
jungang_all = filtered_df[filtered_df["상권분류"] == "중앙동로데오"]

# 예산 내 진입 가능 매장 연산
seongpo_accessible = seongpo_all[seongpo_all["평균가격"] <= budget]
jungang_accessible = jungang_all[jungang_all["평균가격"] <= budget]

# 4. 상단 대시보드 스코어 비교 (2열 배치)
st.subheader(f"📊 현재 예산 [{budget:,}원] 기준 두 상권 지표 비교")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏫 성포고등학교 주변 상권")
    if len(seongpo_all) > 0:
        sp_rate = (len(seongpo_accessible) / len(seongpo_all)) * 100
        st.metric(label="예산 내 진입 가능 점포 비율", value=f"{sp_rate:.1f}%", delta=f"전체 {len(seongpo_all)}개 중 {len(seongpo_accessible)}개")
    else:
        st.write("해당 조건의 매장이 없습니다.")

with col2:
    st.markdown("### 🛍️ 중앙동 로데오 상권")
    if len(jungang_all) > 0:
        ja_rate = (len(jungang_accessible) / len(jungang_all)) * 100
        st.metric(label="예산 내 진입 가능 점포 비율", value=f"{ja_rate:.1f}%", delta=f"전체 {len(jungang_all)}개 중 {len(jungang_accessible)}개", delta_color="normal")
    else:
        st.write("해당 조건의 매장이 없습니다.")

st.markdown("---")

# 5. 핵심 통계 및 업종다변화 시각화 대조
st.subheader("💡 빅데이터 분석 결과 및 경영학적 해석")

# 예산 8000원 이하 기본 상황 시뮬레이션 멘트 자동화
if budget <= 9000:
    st.warning(f"**📢 탐구 발견 사실:**\n"
               f"학생들의 평균 한 끼 예산인 {budget:,}원 선에서 **중앙동 로데오 상권**은 마라탕, 두끼 뷔페, 코인노래방, 보세 쇼핑몰, 즉석사진관(인생네컷) 등 "
               f"10대 취향의 업종이 조밀하게 밀집해 있어 압도적인 선택지를 제공합니다.\n\n"
               f"반면 **성포고 주변 상권**은 대다수가 가족 외식형 고가 음식점(갈비집, 감자탕)이나 유흥 포차, 성인 타겟 시설에 치우쳐 있어 "
               f"학생들이 진입할 수 있는 곳이 일부 가성비 카페나 편의점으로 제한됩니다. 이 현상을 경영학에서는 **'배후 상권의 공급 미스매치'**라고 부르며, "
               f"정작 소비 욕구가 강한 10대 청소년들이 로컬(성포동)을 이탈해 교통비를 내고 **중앙동 중심상권으로 유출되는 핵심 원인**으로 분석됩니다.")
else:
    st.info("예산이 풍부해질수록 두 상권의 진입 격차는 줄어들지만, 10대 맞춤 인프라(인생네컷, 보세의류, 코인노래방)의 절대적 밀집도는 여전히 중앙동이 우세합니다.")

st.markdown("---")

# 6. 하단 하이라이트: 실제 매장 데이터 리스트 대조 (2열 배치)
st.subheader(f"🛒 {budget:,}원으로 갈 수 있는 상권별 매장 실시간 매칭 리스트")

col3, col4 = st.columns(2)

with col3:
    st.markdown(f"**🏫 성포고 주변 이용 가능 매장 ({len(seongpo_accessible)}개)**")
    if len(seongpo_accessible) > 0:
        st.dataframe(seongpo_accessible[["가게이름", "업종분류", "대표메뉴", "평균가격", "주타겟층"]], use_container_width=True)
    else:
        st.write("😢 이 돈으로 성포고 근처에서 즐길 수 있는 매장이 없습니다.")

with col4:
    st.markdown(f"**🛍️ 중앙동 로데오 이용 가능 매장 ({len(jungang_accessible)}개)**")
    if len(jungang_accessible) > 0:
        st.dataframe(jungang_accessible[["가게이름", "업종분류", "대표메뉴", "평균가격", "주타겟층"]], use_container_width=True)
    else:
        st.write("😢 이 돈으로 중앙동에서 이용 가능한 매장이 없습니다.")
