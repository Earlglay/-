import numpy as np
import matplotlib.pyplot as plt

# 중력 렌즈 시뮬레이션 파라미터
def einstein_radius(M, D, D_lens, D_source):
    """
    M: 렌즈 천체의 질량 (kg)
    D: 관찰자와 배경 천체(출발점) 사이의 거리 (m)
    D_lens: 렌즈 천체와 관찰자 사이의 거리 (m)
    D_source: 렌즈 천체와 배경 천체 사이의 거리 (m)
    """
    G = 6.67430e-11  # 중력 상수 (m^3 kg^-1 s^-2)
    c = 3.0e8  # 빛의 속도 (m/s)
    
    # 아인슈타인 반지름 계산 (m 단위)
    return np.sqrt((4 * G * M) / (c**2 * D_lens * (D_source - D_lens)))

# 렌즈 천체와 배경 천체 설정
M_lens = 1e15  # 렌즈 천체의 질량 (kg)
D_lens = 1e22  # 렌즈 천체와 관찰자 사이의 거리 (m)
D_source = 1.5e22  # 렌즈 천체와 배경 천체 사이의 거리 (m)

# 아인슈타인 반지름 계산
R_einstein = einstein_radius(M_lens, D_lens, D_lens, D_source)
print(f"Einstein radius: {R_einstein:.2e} meters")

# 시뮬레이션 설정
num_points = 1000  # 배경 천체의 위치를 나타내는 점의 개수
theta = np.linspace(-5 * R_einstein, 5 * R_einstein, num_points)  # 배경 천체의 x좌표
y = np.zeros_like(theta)  # 배경 천체의 y좌표 (렌즈는 2D 평면에서 시뮬레이션)

# 중력 렌즈 효과 계산
def lensing_effect(x, y, R_einstein):
    """
    중력 렌즈 효과를 시뮬레이션하여 빛이 휘어지는 정도를 계산합니다.
    """
    r = np.sqrt(x**2 + y**2)
    deflection_angle = R_einstein**2 / r**2  # 굴절 각도 계산
    x_deflected = x * (1 + deflection_angle)
    y_deflected = y * (1 + deflection_angle)
    return x_deflected, y_deflected

# 배경 천체의 빛 경로를 휘게 하여 시뮬레이션
x_deflected, y_deflected = lensing_effect(theta, y, R_einstein)

# 시각화
plt.figure(figsize=(6, 6))
plt.plot(theta, y, 'b.', label='배경 천체')
plt.plot(x_deflected, y_deflected, 'r.', label='왜곡된 경로 (중력 렌즈)')
plt.axvline(x=0, color='k', linestyle='--', label='렌즈 천체')  # 렌즈 천체 위치 표시
plt.title("중력 렌즈 시뮬레이션")
plt.xlabel("X 위치 (m)")
plt.ylabel("Y 위치 (m)")
plt.legend()
plt.grid(True)
plt.show()

