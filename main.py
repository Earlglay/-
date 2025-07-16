import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time
import pandas as pd

# --- 페이지 설정 ---
st.set_page_config(layout="wide")

st.title("미세 중력 시뮬레이션: 상호 작용하는 구체들")

st.markdown("""
이 시뮬레이션은 여러 개의 작은 구(Ball)들이 미세 중력 환경에서 서로에게 약한 중력을 행사하며 움직이는 모습을 보여줍니다.
각 구는 질량에 비례하는 인력으로 서로를 끌어당기며, 벽에 닿으면 튕겨 나옵니다.
""")

# --- 시뮬레이션 파라미터 설정 ---
with st.sidebar:
    st.header("시뮬레이션 설정")
    num_balls = st.slider("구의 개수", 2, 10, 5)
    simulation_duration = st.slider("시뮬레이션 지속 시간 (초)", 10, 60, 30)
    gravity_constant = st.slider("중력 상수 (G)", 0.01, 0.5, 0.05, 0.01)
    ball_mass_range = st.slider("구 질량 범위", 1, 10, (2, 8)) # (최소, 최대)
    ball_radius_multiplier = st.slider("구 반지름 배수", 0.1, 1.0, 0.5, 0.1) # 반지름 = 질량 * 배수

    start_button = st.button("시뮬레이션 시작")
    stop_button = st.button("시뮬레이션 정지")

# --- 구체 클래스 정의 ---
class Ball:
    def __init__(self, x, y, mass, radius, color):
        self.x = x
        self.y = y
        self.vx = (np.random.rand() - 0.5) * 5 # 초기 속도 (랜덤)
        self.vy = (np.random.rand() - 0.5) * 5
        self.mass = mass
        self.radius = radius
        self.color = color

    def update_position(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def apply_force(self, fx, fy, dt):
        # F = ma -> a = F/m
        ax = fx / self.mass
        ay = fy / self.mass
        self.vx += ax * dt
        self.vy += ay * dt

    def check_boundary_collision(self, min_x, max_x, min_y, max_y):
        # X축 경계 충돌
        if self.x - self.radius < min_x:
            self.x = min_x + self.radius
            self.vx *= -1 * 0.9 # 속도 반전 및 약간의 에너지 손실
        elif self.x + self.radius > max_x:
            self.x = max_x - self.radius
            self.vx *= -1 * 0.9

        # Y축 경계 충돌
        if self.y - self.radius < min_y:
            self.y = min_y + self.radius
            self.vy *= -1 * 0.9
        elif self.y + self.radius > max_y:
            self.y = max_y - self.radius
            self.vy *= -1 * 0.9

# --- 메인 콘텐츠 영역 준비 ---
col1, col2 = st.columns([2, 1]) # 시각화 영역을 더 넓게

with col1:
    st.subheader("미세 중력 시뮬레이션")
    # Plotly 그래프를 담을 빈 컨테이너 생성
    # 2D 산점도 그래프로 구체들의 위치를 표시
    simulation_plot_placeholder = st.empty()

with col2:
    st.subheader("시뮬레이션 정보")
    info_text = st.empty() # 시뮬레이션 정보 텍스트를 위한 플레이스홀더
    st.subheader("밝기 변화 그래프 (예시 - 현재는 구 구현에 집중)")
    # 밝기 변화 그래프는 이 시뮬레이션의 기본 목적이 아니므로,
    # 여기서는 "구의 평균 속도 변화" 그래프로 대체하거나 비활성화합니다.
    # 만약 각 구가 '광원'이라면 그에 따른 '밝기'를 정의해야 합니다.
    # 현재는 '미세 중력' 자체에 집중하겠습니다.
    avg_speed_chart_placeholder = st.empty() # 평균 속도 그래프 플레이스홀더

# --- 시뮬레이션 실행 로직 ---
if 'run_simulation' not in st.session_state:
    st.session_state.run_simulation = False

if start_button:
    st.session_state.run_simulation = True
    
    # 구체 초기화
    balls = []
    colors = plt.cm.get_cmap('hsv', num_balls) # 구의 개수만큼 색상 생성
    for i in range(num_balls):
        mass = np.random.uniform(ball_mass_range[0], ball_mass_range[1])
        radius = mass * ball_radius_multiplier
        x = np.random.uniform(-100 + radius, 100 - radius) # 초기 위치 랜덤
        y = np.random.uniform(-100 + radius, 100 - radius)
        balls.append(Ball(x, y, mass, radius, colors(i)))

    start_time = time.time()
    current_time = 0
    dt = 0.1 # 시간 간격 (Time step)

    # 그래프 데이터 초기화
    avg_speeds_history = []
    time_points_history = []

    # 시뮬레이션 루프
    while st.session_state.run_simulation and current_time < simulation_duration:
        elapsed_time = time.time() - start_time
        current_time = elapsed_time

        # --- 중력 계산 및 힘 적용 ---
        for i, ball1 in enumerate(balls):
            fx = 0
            fy = 0
            for j, ball2 in enumerate(balls):
                if i != j: # 자기 자신에게는 힘을 가하지 않음
                    dx = ball2.x - ball1.x
                    dy = ball2.y - ball1.y
                    distance = math.sqrt(dx**2 + dy**2)

                    if distance < ball1.radius + ball2.radius: # 구체 간 충돌 처리 (간단하게 튕겨나가게)
                        # 충돌 시 속도 반전 (매우 단순화된 모델)
                        angle = math.atan2(dy, dx)
                        total_velocity_x = ball1.vx + ball2.vx
                        total_velocity_y = ball1.vy + ball2.vy

                        # 서로 밀어내기
                        overlap = (ball1.radius + ball2.radius) - distance
                        ball1.x -= overlap * np.cos(angle) / 2
                        ball1.y -= overlap * np.sin(angle) / 2
                        ball2.x += overlap * np.cos(angle) / 2
                        ball2.y += overlap * np.sin(angle) / 2

                        # 속도 교환 (단순화된 탄성 충돌)
                        v1_n = ball1.vx * np.cos(angle) + ball1.vy * np.sin(angle)
                        v1_t = -ball1.vx * np.sin(angle) + ball1.vy * np.cos(angle)
                        v2_n = ball2.vx * np.cos(angle) + ball2.vy * np.sin(angle)
                        v2_t = -ball2.vx * np.sin(angle) + ball2.vy * np.cos(angle)

                        # 1D 충돌 공식 (질량 고려)
                        new_v1_n = ((ball1.mass - ball2.mass) * v1_n + 2 * ball2.mass * v2_n) / (ball1.mass + ball2.mass)
                        new_v2_n = ((ball2.mass - ball1.mass) * v2_n + 2 * ball1.mass * v1_n) / (ball1.mass + ball2.mass)
                        
                        ball1.vx = new_v1_n * np.cos(angle) - v1_t * np.sin(angle)
                        ball1.vy = new_v1_n * np.sin(angle) + v1_t * np.cos(angle)
                        ball2.vx = new_v2_n * np.cos(angle) - v2_t * np.sin(angle)
                        ball2.vy = new_v2_n * np.sin(angle) + v2_t * np.cos(angle)


                    # 거리가 0이 되는 것을 방지 (중력 공식에 사용)
                    if distance == 0:
                        continue
                    
                    # 중력 법칙 F = G * (m1 * m2) / r^2
                    force_magnitude = (gravity_constant * ball1.mass * ball2.mass) / (distance**2)

                    # 힘의 방향 벡터
                    force_x = force_magnitude * (dx / distance)
                    force_y = force_magnitude * (dy / distance)

                    fx += force_x
                    fy += force_y
            
            ball1.apply_force(fx, fy, dt) # 계산된 힘 적용
            ball1.update_position(dt) # 위치 업데이트
            ball1.check_boundary_collision(-150, 150, -150, 150) # 경계 충돌 확인 (시뮬레이션 공간)

        # --- 시각화 업데이트 (Plotly) ---
        traces = []
        avg_speed = 0
        for ball in balls:
            traces.append(
                go.Scatter(
                    x=[ball.x],
                    y=[ball.y],
                    mode='markers',
                    marker=dict(
                        size=ball.radius * 2, # 반지름 * 2 = 지름
                        color=ball.color,
                        opacity=0.8,
                        line=dict(width=1, color='Black')
                    ),
                    name=f'Mass: {ball.mass:.1f}',
                    showlegend=True
                )
            )
            avg_speed += math.sqrt(ball.vx**2 + ball.vy**2)
        
        avg_speed /= len(balls)
        avg_speeds_history.append(avg_speed)
        time_points_history.append(current_time)

        fig_sim = go.Figure(data=traces)
        fig_sim.update_layout(
            title=f"시간: {current_time:.2f} 초",
            xaxis_title="X 위치",
            yaxis_title="Y 위치",
            xaxis_range=[-150, 150], # 시뮬레이션 공간 범위 고정
            yaxis_range=[-150, 150],
            width=700, # 그래프 너비
            height=700, # 그래프 높이
            showlegend=True,
            hovermode="closest"
        )
        simulation_plot_placeholder.plotly_chart(fig_sim, use_container_width=False) # 고정 크기 사용

        # --- 정보 텍스트 업데이트 ---
        info_text.markdown(f"""
            **진행 시간:** {current_time:.2f} 초 / {simulation_duration} 초
            **평균 구 속도:** {avg_speed:.2f}
            ---
            **구 정보:**
            """)
        for i, ball in enumerate(balls):
            info_text.markdown(f"""
                - **구 {i+1}**: 질량={ball.mass:.1f}, 속도=({ball.vx:.1f}, {ball.vy:.1f})
                """)

        # --- 평균 속도 그래프 업데이트 ---
        fig_avg_speed = go.Figure(data=go.Scatter(x=list(time_points_history), y=list(avg_speeds_history),
                                                  mode='lines', name='평균 속도', line=dict(color='purple', width=2)))
        fig_avg_speed.update_layout(
            title="시간에 따른 구의 평균 속도 변화",
            xaxis_title="시간 (초)",
            yaxis_title="평균 속도",
            height=300
        )
        avg_speed_chart_placeholder.plotly_chart(fig_avg_speed, use_container_width=True)

        time.sleep(0.01) # 업데이트 간격 조절 (짧을수록 부드럽지만 CPU 사용량 증가)

    # 시뮬레이션 종료 후 메시지
    if st.session_state.run_simulation: # 사용자가 중지 버튼을 누르지 않고 시간이 다 된 경우
        info_text.success("시뮬레이션이 완료되었습니다.")
    st.session_state.run_simulation = False # 시뮬레이션 종료 상태로 변경

if stop_button:
    st.session_state.run_simulation = False
    st.info("시뮬레이션이 중지되었습니다.")

# 초기 상태 메시지
if not st.session_state.run_simulation and 'start_time' not in st.session_state:
    st.info("시뮬레이션 시작 버튼을 눌러주세요.")
