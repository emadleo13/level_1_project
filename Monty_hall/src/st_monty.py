import streamlit as st
import time

from monty import simulate_games


st.image("src/Images/banner.png", width=350)



num_games = st.number_input("Enter the number of games to simulate:", min_value= 1, value= 1000, step= 100)

wins_no_switch = 0
wins_switch = 0

col1 , col2 = st.columns(2)
col1.subheader("win percentage when without switching")
chart1 = col1.line_chart(x=None, y=None, width=400, height=400)
col2.subheader("win percentage when with switching")
chart2 = col2.line_chart(x=None, y=None, width=400, height=400)


for i in range(num_games):
    num_wins_without_switching, num_wins_with_switching = simulate_games(1)
    
    wins_no_switch += num_wins_without_switching
    wins_switch += num_wins_with_switching
    
    chart1.add_rows([wins_no_switch / (i + 1)])
    chart2.add_rows([wins_switch / (i + 1)])
    
    
    time.sleep(0.01)
