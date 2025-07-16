import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# 실시간 데이터 시뮬레이션 (예: 랜덤 값 생성)
def generate_data():
    return np.random.randn(100)

# Streamlit UI
st.title("실시간 업데이트되는 그래프")

# 빈 공간 만들기
graph_placeholder = st.empty()

# 실시간으로 그래프 업데이트
for _ in range(100):  # 100번 업데이트
    # 새로운 데이터 생성
    data = generate_data()
    
    # 그래프 그리기
    fig, ax = plt.subplots()
    ax.plot(data)
    ax.set_title("실시간 데이터 그래프")
    
    # Streamlit에서 그래프 업데이트
    graph_placeholder.pyplot(fig)
    
    # 0.5초마다 그래프를 업데이트
    time.sleep(0.5)
