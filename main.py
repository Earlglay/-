import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time
import math
import matplotlib.pyplot as plt

# --- 페이지 설정 ---
st.set_page_config(layout="wide") # 넓은 레이아웃 사용

st.title("원형 광원과 가림막 원 시뮬레이션")

st.markdown("""
이 앱은 원형 광원이 있고, 다른 원이 그 광원 앞을 지나갈 때 빛의 밝기가 어떻게 변하는지 실시간으로 보여줍니다.
가림막 원이 광원을 가리는 면적에 따라 빛의 밝기(그래프)가 변화합니다.
""")

# --- 두 원의 교차 면적 계산 함수 ---
# 출처: https://stackoverflow.com/questions/42436329/area-of-intersection-of-two-circles
def calculate_circle_intersection_area(d, r1, r2):
    """
    두 원의 교차 면적을 계산합니다.
    d: 두 원의 중심 간 거리
    r1: 첫 번째 원의 반지름
    r2: 두 번째 원의 반지름
    """
    if d >= r1 + r2:  # 원들이 완전히 떨어져 있을 때
        return 0.0
    if d <= abs(r1 - r2):  # 한 원이 다른 원 안에 완전히 포함될 때
        return math.pi * min(r1, r2)**2

    # 일반적인 교차 상황
    a = r1**2
    b = r2**2
    x = (a - b + d**2) / (2 * d)
    # y는 0보다 작을 수 없으므로, math.sqrt에 넣기 전에 조건 확인
    y = math.sqrt(a - x**2) if a >= x**2 else 0

    area = a * math.acos(x / r1) + b * math.acos((d - x) / r2) - d * y
    return area

# --- 사이드바: 시뮬레이션 파라미터 설정 ---
with st.sidebar:
    st.header("시뮬레이션 설정")
    light_source_radius = st.slider("광원 반지름 (px)", 10, 100, 50)
    occluder_radius = st.slider("가림막 원 반지름 (px)", 10, 100, 40)
    occluder_speed = st.slider("가림막 원 이동 속도", 0.1, 5.0, 1.0)
    initial_light_intensity = st.slider("초기 빛 강도 (최대 밝기)", 100, 1000, 500)
    simulation_duration = st.slider("시뮬레이션 지속 시간 (초)", 10, 60, 30)

    start_button = st.button("시뮬레이션 시작")
    stop_button = st.button("시뮬레이션 정지")

# --- 메인 콘텐츠 영역 준비 ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("원 시각화")
    # Matplotlib으로 원을 그릴 준비
    # figsize는 Streamlit에 표시될 때의 비율에 영향을 줍니다.
    fig_circles, ax_circles = plt.subplots(figsize=(6, 6))
    ax_circles.set_xlim(-200, 200) # X축 범위 고정
    ax_circles.set_ylim(-200, 200) # Y축 범위 고정
    ax_circles.set_aspect('equal', adjustable='box') # X, Y축 비율을 같게
    ax_circles.grid(True) # 그리드 표시
    circle_plot_placeholder = st.pyplot(fig_circles) # Matplotlib 그래프를 위한 플레이스홀더

with col2:
    st.subheader("빛의 밝기 그래프")
    # Plotly 그래프를 담을 빈 컨테이너 생성
    brightness_chart_placeholder = st.empty()

# --- 시뮬레이션 실행 로직 ---
# 세션 상태를 사용하여 시뮬레이션 실행 여부를 관리
if 'run_simulation' not in st.session_state:
    st.session_state.run_simulation = False

if start_button:
    st.session_state.run_simulation = True
    # 그래프 데이터 초기화
    brightness_history = []
    time_points = []
    start_time = time.time() # 시뮬레이션 시작 시간 기록
    current_time = 0

    # 광원 원 (고정 위치)
    light_source_x, light_source_y = 0, 0
    light_source_area = math.pi * light_source_radius**2 # 광원 전체 면적 계산

    # 가림막 원 초기 위치 (왼쪽 화면 밖에서 시작)
    occluder_x = -200 - occluder_radius
    occluder_y = 0 # Y축은 고정

    # 시뮬레이션 상태 메시지 표시를 위한 플레이스홀더
    status_text = st.empty()

    # 시뮬레이션 루프
    while st.session_state.run_simulation and current_time < simulation_duration:
        elapsed_time = time.time() - start_time
        current_time = elapsed_time

        # 가림막 원의 X 위치 업데이트 (이동 속도 적용)
        # 속도에 2를 곱하여 시뮬레이션마다 이동하는 거리 조정
        occluder_x += occluder_speed * 2
        
        # 가림막 원이 화면 오른쪽 밖으로 나가면 다시 왼쪽 밖으로 이동
        if occluder_x > 200 + occluder_radius:
            occluder_x = -200 - occluder_radius

        # 두 원의 중심 간 거리 계산
        distance = math.sqrt((occluder_x - light_source_x)**2 + (occluder_y - light_source_y)**2)

        # 교차 면적 계산
        intersect_area = calculate_circle_intersection_area(distance, light_source_radius, occluder_radius)

        # 가려지지 않은 면적 = 광원 전체 면적 - 교차 면적
        unobscured_area = light_source_area - intersect_area

        # 현재 밝기 계산 (가려지지 않은 면적에 비례)
        # 광원 면적이 0이 아닐 경우에만 계산하여 ZeroDivisionError 방지
        if light_source_area > 0:
            current_brightness = (unobscured_area / light_source_area) * initial_light_intensity
        else:
            current_brightness = 0 # 광원 면적이 0이면 밝기도 0

        # 데이터 저장
        brightness_history.append(current_brightness)
        time_points.append(current_time)

        # --- 원 시각화 업데이트 (Matplotlib) ---
        ax_circles.clear() # 이전 그림 지우기
        ax_circles.set_xlim(-200, 200) # 축 범위 다시 설정 (clear() 때문에 초기화됨)
        ax_circles.set_ylim(-200, 200)
        ax_circles.set_aspect('equal', adjustable='box')
        ax_circles.grid(True)

        # 광원 원 그리기 (주황색, 반투명)
        light_source_circle = plt.Circle((light_source_x, light_source_y), light_source_radius,
                                         color='orange', alpha=0.7, ec='black', lw=2)
        ax_circles.add_patch(light_source_circle)

        # 가림막 원 그리기 (파란색, 반투명)
        occluder_circle = plt.Circle((occluder_x, occluder_y), occluder_radius,
                                     color='blue', alpha=0.5, ec='black', lw=2)
        ax_circles.add_patch(occluder_circle)

        ax_circles.set
