"""
Glassmorphism Pomodoro Clock (Custom Time Menu Added)
-----------------------------------------------------------------
Run:
    streamlit run pages/pomodoro.py
"""

import time
import streamlit as st

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Focus Timer", page_icon="⏱️", layout="centered")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@700;900&display=swap');

    /* ---------- App Background ---------- */
    .stApp {
        background-color: #dd8b9c !important; 
    }

    /* ---------- Glassmorphism Card Container ---------- */
    .block-container {
        padding: 2.5rem 1.5rem !important;
        margin-top: 8vh !important;
        max-width: 420px !important;
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 40px !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08) !important;
    }

    #MainMenu, footer, header {visibility: hidden;}

    /* ---------- Top Toggles ---------- */
    div[role="radiogroup"] {
        background-color: rgba(255, 255, 255, 0.15);
        border-radius: 40px;
        padding: 4px;
        gap: 0;
        display: flex;
        justify-content: space-between;
        margin-bottom: 2rem;
    }
    div[role="radiogroup"] label > div:first-child { display: none !important; }
    
    div[role="radiogroup"] label {
        background: transparent;
        border-radius: 40px;
        padding: 8px 10px;
        color: rgba(255, 255, 255, 0.8);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {
        font-family: 'Nunito', sans-serif !important;
        font-weight: 900;
        font-size: 0.85rem;
        margin: 0;
    }
    div[role="radiogroup"] label[data-checked="true"] {
        background-color: white !important;
        color: #dd8b9c !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    /* ---------- The Editable Clock Text ---------- */
    .timer-text {
        font-family: 'Nunito', sans-serif !important;
        font-size: 5.5rem !important;
        font-weight: 900 !important;
        color: white !important;
        text-align: center !important;
        line-height: 1.1 !important;
        text-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        margin: 1.5rem 0 !important;
    }
    
    /* Only target the main giant text input, not the small number input */
    div[data-testid="stTextInput"] * {
        background-color: transparent !important; 
        border: none !important;
    }
    
    div[data-testid="stTextInput"] input {
        font-family: 'Nunito', sans-serif !important;
        font-size: 5.5rem !important;
        font-weight: 900 !important;
        color: white !important;
        text-align: center !important;
        padding: 0 !important;
        line-height: 1.1 !important;
        box-shadow: none !important;
        text-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        margin: 1.5rem 0 !important;
    }
    
    div[data-testid="stTextInput"] input:focus {
        background-color: rgba(255, 255, 255, 0.15) !important;
        border-radius: 20px !important;
        outline: none !important;
    }
    
    div[data-testid="InputInstructions"] {
        display: none !important;
    }

    /* ---------- Emoji Control Buttons (Glass Effect) ---------- */
    div[data-testid="stButton"] button {
        background-color: rgba(255, 255, 255, 0.2) !important; 
        color: white !important;
        border-radius: 30px !important;
        font-size: 1.5rem !important;
        padding: 0.6rem 0 !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        transition: transform 0.2s ease, background-color 0.2s ease;
        margin-top: 0.5rem !important;
        margin-bottom: 1.5rem !important;
    }
    div[data-testid="stButton"] button:hover {
        background-color: rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-2px);
    }
    div[data-testid="stButton"] button:active {
        transform: translateY(1px);
    }
    
    /* Settings/Expand small icons overrides */
    .icon-row div[data-testid="stButton"] button {
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        padding: 0 !important;
        font-size: 1.2rem !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 auto !important;
    }

    /* ---------- Quick Settings Panel ---------- */
    .settings-panel {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 1.2rem;
        margin-top: 0.5rem;
        text-align: center;
    }
    .settings-title {
        color: white;
        font-family: 'Nunito', sans-serif;
        font-weight: 700;
        font-size: 0.9rem;
        margin-bottom: 0.8rem;
        letter-spacing: 0.5px;
    }
    .settings-panel div[data-testid="stButton"] button {
        margin-bottom: 0 !important;
        font-size: 1rem !important;
        font-weight: bold !important;
        font-family: 'Nunito', sans-serif !important;
    }
    
    /* Glass Style for the Custom Number Input */
    div[data-testid="stNumberInput"] div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.2) !important;
        border: none !important;
        border-radius: 12px !important;
    }
    div[data-testid="stNumberInput"] input {
        color: white !important;
        font-family: 'Nunito', sans-serif !important;
        font-weight: bold !important;
        text-align: center !important;
    }

    /* ---------- Bottom Line ---------- */
    .bottom-line {
        width: 45%;
        height: 6px;
        background-color: white;
        border-radius: 10px;
        margin: 1.5rem auto 0 auto;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Session State & Logic
# ---------------------------------------------------------------------------
if 'time_left' not in st.session_state:
    st.session_state.time_left = 25 * 60  # Default to 25 minutes exactly
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'mode' not in st.session_state:
    st.session_state.mode = "Pomodoro"
if 'show_settings' not in st.session_state:
    st.session_state.show_settings = False

def parse_time(time_str):
    try:
        # Handles user typing "10:00" OR just "10" directly into the clock
        if ":" in str(time_str):
            m, s = str(time_str).split(":", 1)
            return int(m) * 60 + int(s)
        else:
            return int(time_str) * 60
    except ValueError:
        return None

def set_time(minutes):
    st.session_state.time_left = minutes * 60
    st.session_state.is_running = False
    st.session_state.show_settings = False

def on_mode_change():
    mode = st.session_state.mode_selector
    st.session_state.mode = mode
    st.session_state.is_running = False
    if mode == "Pomodoro":
        set_time(25)
    elif mode == "Short Break":
        set_time(5)
    else:
        set_time(15)

def on_time_edit():
    parsed = parse_time(st.session_state.timer_input)
    if parsed is not None:
        st.session_state.time_left = parsed
        st.session_state.is_running = False

def toggle_settings():
    st.session_state.show_settings = not st.session_state.show_settings

# ---------------------------------------------------------------------------
# UI Rendering
# ---------------------------------------------------------------------------

# 1. Top Toggles
st.radio(
    "Mode", 
    ["Pomodoro", "Short Break", "Long Break"], 
    horizontal=True, 
    label_visibility="collapsed", 
    key="mode_selector",
    index=["Pomodoro", "Short Break", "Long Break"].index(st.session_state.mode),
    on_change=on_mode_change
)

# 2. Timer Display
timer_placeholder = st.empty()

def render_clock(time_in_seconds, is_running):
    mins, secs = divmod(time_in_seconds, 60)
    time_str = f"{mins:02d}:{secs:02d}"
    
    if is_running:
        timer_placeholder.markdown(f'<div class="timer-text">{time_str}</div>', unsafe_allow_html=True)
    else:
        # Invisible active text input
        timer_placeholder.text_input(
            "timer", 
            value=time_str, 
            key="timer_input", 
            on_change=on_time_edit, 
            label_visibility="collapsed"
        )

render_clock(st.session_state.time_left, st.session_state.is_running)

# 3. Emoji Control Buttons (Start / Pause / Reset)
ctrl1, ctrl2, ctrl3 = st.columns(3)
with ctrl1:
    if st.button("▶️", use_container_width=True):
        st.session_state.is_running = True
        st.rerun()
with ctrl2:
    if st.button("⏸️", use_container_width=True):
        st.session_state.is_running = False
        st.rerun()
with ctrl3:
    if st.button("🔄", use_container_width=True):
        on_mode_change() 
        st.rerun()

# 4. Small Icons Row (Settings / Expand)
st.markdown('<div class="icon-row">', unsafe_allow_html=True)
ic1, ic2, ic3, ic4, ic5 = st.columns(5) 
with ic3: 
    st.button("⚙️", on_click=toggle_settings, key="settings_btn") 
with ic4: 
    st.button("⛶", key="expand_btn") 
st.markdown('</div>', unsafe_allow_html=True)

# 5. Expandable Quick Settings with Custom Time Option
if st.session_state.show_settings:
    st.markdown('<div class="settings-panel">', unsafe_allow_html=True)
    
    st.markdown('<div class="settings-title">Quick Presets</div>', unsafe_allow_html=True)
    sc1, sc2, sc3, sc4 = st.columns(4)
    if sc1.button("5m", use_container_width=True): set_time(5); st.rerun()
    if sc2.button("10m", use_container_width=True): set_time(10); st.rerun()
    if sc3.button("15m", use_container_width=True): set_time(15); st.rerun()
    if sc4.button("30m", use_container_width=True): set_time(30); st.rerun()
    
    # Custom Time Entry Section
    st.markdown('<div class="settings-title" style="margin-top: 1rem;">Custom Time (Mins)</div>', unsafe_allow_html=True)
    cc1, cc2 = st.columns([3, 1])
    with cc1:
        custom_mins = st.number_input("Custom", min_value=1, max_value=240, value=25, label_visibility="collapsed")
    with cc2:
        if st.button("Set", key="set_custom", use_container_width=True):
            set_time(custom_mins)
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

# 6. Bottom line decoration
st.markdown('<div class="bottom-line"></div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Timer Tick Logic (Flicker-Free)
# ---------------------------------------------------------------------------
if st.session_state.is_running:
    while st.session_state.time_left > 0 and st.session_state.is_running:
        render_clock(st.session_state.time_left, True)
        time.sleep(1)
        st.session_state.time_left -= 1
        
    if st.session_state.time_left == 0:
        st.session_state.is_running = False
        st.balloons()
        st.rerun()