import numpy as np
import matplotlib.pyplot as plt

# 아인슈타인 반지름 계산 함수
def einstein_radius(M, D_lens, D_source):
    """
    M: 렌즈 천체의 질량 (kg)
    D_lens: 렌즈 천체와 관찰자 사이의 거리 (m)
    D_source: 렌즈 천체와 배경 천체 사이의 거리 (m)
    """
    G = 6.67430e-11  # 중력 상수 (m^3 kg^-1 s^-2)
    c = 3.0e8  # 빛의 속도 (m/s)
    
    # 아인슈타인 반지름 계산 (m 단위)
    return np.sqrt((4 * G * M) / (c**2 * D_lens * (D_source - D_lens)))

# 렌즈 천체와 배경 천체 설정
M_lens = 1e30  # 렌즈 천체의 질량 (kg), 예: 태양의 질량 정도
D_lens = 1e21  # 렌즈 천체와 관찰자 사이의 거리 (m), 예: 1kpc
D_source = 1.5e22  # 렌즈 천체와 배경 천체 사이의 거리 (m), 예: 1.5kpc

# 아인슈타인 반지름 계산
R_einstein = einstein_radius(M_lens, D_lens, D_source)
print(f"Einstein radius: {R_einstein:.2e} meters")

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

# 시각화
plt.figure(figsize=(8, 6))
plt.plot(t, brightness, label='밝기 변화 (미세 중력 렌즈)', color='blue')
plt.axhline(1, color='k', linestyle='--', label='원래 밝기')
plt.title("미세 중력 렌즈 효과에 의한 밝기 변화")
plt.xlabel("시간 (렌즈 천체의 위치 변화)")
plt.ylabel("밝기 (Normalized Flux)")
plt.legend()
plt.grid(True)
plt.show()
