import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from microlensing_simulation import simulate_microlensing_lightcurve # 위에서 만든 시뮬레이션 함수 임포트

st.set_page_config(layout="wide")

st.title("외계행성 미세 중력 관측 시뮬레이션")
st.markdown("""
이 앱은 미세 중력 렌즈 현상(Microlensing)을 시뮬레이션하여 외계행성 탐색 원리를 시각적으로 보여줍니다.
""")

st.sidebar.header("시뮬레이션 매개변수 설정")

# 사용자 입력 매개변수
t_0 = st.sidebar.slider("최대 밝기 시간 (t_0)", -5.0, 5.0, 0.0, 0.1)
u_0 = st.sidebar.slider("최소 접근 거리 (u_0)", 0.01, 2.0, 0.1, 0.01)
t_E = st.sidebar.slider("아인슈타인 시간 (t_E)", 1.0, 20.0, 5.0, 0.1)
num_points = st.sidebar.slider("데이터 포인트 수", 50, 500, 200, 10)

st.sidebar.markdown("---")
st.sidebar.info(
    "**매개변수 설명:**\n\n"
    "- **t_0:** 배경별이 렌즈에 가장 가까이 접근하는 시간입니다. 광도곡선의 피크 위치를 결정합니다.\n"
    "- **u_0:** 렌즈 중심으로부터 배경별까지의 최소 거리입니다. 아인슈타인 반지름(Einstein Radius) 단위로, 작을수록 렌즈 효과가 강해집니다.\n"
    "- **t_E:** 아인슈타인 시간입니다. 아인슈타인 반지름을 배경별이 가로지르는 시간으로, 광도곡선의 폭을 결정합니다."
)

# 시뮬레이션 실행
t_start = t_0 - 3 * t_E
t_end = t_0 + 3 * t_E
times, magnifications = simulate_microlensing_lightcurve(t_start, t_end, num_points, t_0, u_0, t_E)

st.header("시뮬레이션 결과: 광도 곡선")

# Plotting with Matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(times, magnifications, color='skyblue', linewidth=2)
ax.set_xlabel("시간 (Time, Normalized)", fontsize=12)
ax.set_ylabel("밝기 확대율 (Magnification)", fontsize=12)
ax.set_title("미세 중력 렌즈 광도 곡선", fontsize=14)
ax.grid(True, linestyle='--', alpha=0.7)
ax.set_ylim(bottom=0.9, top=max(magnifications) * 1.1 + 0.1) # Y축 범위 조정
st.pyplot(fig)

st.subheader("결과 해석")
st.write(
    f"설정된 매개변수 (t_0={t_0}, u_0={u_0}, t_E={t_E})에 따라 시뮬레이션된 광도 곡선입니다. "
    f"u_0 값이 작을수록 밝기 확대율이 커지며, t_E 값이 클수록 이벤트 지속 시간이 길어집니다. "
    f"이러한 광도 곡선은 실제 천문 관측에서 외계행성의 존재를 간접적으로 확인하는 데 사용됩니다."
)
st.markdown("---")
st.markdown("Made with ❤️ by [Your Name or Organization]")
