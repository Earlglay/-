
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 아인슈타인 반지름 계산 함수
def einstein_radius(M, D_lens, D_source):
    G = 6.67430e-11  # 중력 상수 (m^3 kg^-1 s^-2)
    c = 3.0e8  # 빛의 속도 (m/s)
    
    # 아인슈타인 반지름 계산 (m 단위)
    return np.sqrt((4 * G * M) / (c**2 * D_lens * (D_source - D_lens)))

# 렌즈 천체와 배경 천체 설정
M_lens = st.slider("렌즈 천체의 질량 (kg)", min_value=int(1e28), max_value=int(1e32), value=int(1e30), step=int(1e28))
D_lens = st.slider("렌즈 천체와 관찰자 사이의 거리 (m)", min_value=int(1e20), max_value=int(1e22), value=int(1e21), step=int(1e20))
D_source = st.slider("렌즈 천체와 배경 천체 사이의 거리 (m)", min_value=int(1e22), max_value=int(1e24), value=int(1.5e22), step=int(1e22))

# 아인슈타인 반지름 계산
R_einstein = einstein_radius(M_lens, D_lens, D_source)

# 시뮬레이션 파라미터
num_points = 1000  # 시간에 따른 시뮬레이션 포인트 수
t = np.linspace(-1, 1, num_points)  # 시간 변수 (렌즈 천체가 이동하는 것처럼 보이게)

# 렌즈 천체의 위치 변화 (단순한 선형 이동 모델)
r_t = R_einstein * np.sqrt(1 + t**2)  # 렌즈 천체가 이동하는 거리

# 미세 중력 렌즈 효과에 의한 밝기 변화 계산
def micro_lensing_brightness(r_t, R_einstein):
    """
    미세 중력 렌즈 효과로 인한 밝기 변화 계산
    r_t: 렌즈 천체와 배경 천체 사이의 거리 (시간에 따라 변화)
    R_einstein: 아인슈타인 반지름
    """
    return 1 / (1 - (R_einstein / r_t)**2)

# 밝기 계산
brightness = micro_lensing_brightness(r_t, R_einstein)

# Streamlit 앱에서 시각화
st.title("미세 중력 렌즈 효과 시뮬레이션")

st.write(f"계산된 아인슈타인 반지름: {R_einstein:.2e} meters")

# 밝기 변화 그래프
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(t, brightness, label='밝기 변화 (미세 중력 렌즈)', color='blue')
ax.axhline(1, color='k', linestyle='--', label='원래 밝기')
ax.set_title("미세 중력 렌즈 효과에 의한 밝기 변화")
ax.set_xlabel("시간 (렌즈 천체의 위치 변화)")
ax.set_ylabel("밝기 (Normalized Flux)")
ax.legend()
ax.grid(True)

st.pyplot(fig)

