"""
IBPS Countdown & Welcome Dashboard (standalone, no database)
-----------------------------------------------------------------
Shows:
  1. "Good morning, mam" + today's date
  2. Quick navigation buttons to Focus Timer and Task Board
  3. Days left until upcoming Institute of Banking Personnel Selection (IBPS) exams
  4. A welcome/motivational message that auto-cycles every few hours

Dates sourced from the official IBPS Calendar 2026-27 (ibps.in). IBPS marks its
calendar "tentative" and can revise dates before the official notification —
double-check against ibps.in closer to each exam.

Run:
    pip install streamlit
    streamlit run app.py
"""

from datetime import datetime, date
import streamlit as st

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

CYCLE_SECONDS = 7200  # how often the welcome message rotates (2 hours)

WELCOME_MESSAGES = [
    "Good morning! Every day of prep brings you closer to your goal.",
    "Rise and shine — today is another step toward IBPS success!",
    "Consistency beats intensity. Small daily effort wins the exam.",
    "You've got this, mam! One more focused day, one step closer.",
    "Discipline today, results tomorrow. Let's go!",
    "Believe in the work you put in — it always shows up on exam day.",
    "One topic at a time. One mock test at a time. You're getting there.",
    "Good morning, mam! A fresh day, a fresh chance to get closer to your IBPS dream.",

"Wake up with determination — every question you solve is a step toward success.",

"Your hard work today is building the confidence you'll carry into the exam hall.",

"Keep going, mam! Progress may feel slow, but every focused hour counts.",

"Today's preparation is tomorrow's achievement. Stay consistent and keep believing.",

"One more day of dedication, one more step toward your banking career.",

"Don't wait for motivation — build your success with discipline, one day at a time.",

"Good morning, mam! Trust your preparation, stay focused, and make today count.",

"Every mock, every revision, every effort brings you closer to that IBPS selection.",

"Your dream is worth the effort. Keep studying, keep improving, and keep moving forward!",
"Good morning, mam! Your dream job is waiting for the hard work you put in today.",

"Rise and shine, mam! Every chapter completed is another victory on your journey to IBPS success.",

"Start your day with confidence — you are capable of achieving great things.",

"Small steps every day, mam. Big results are built through consistent preparation.",

"Your dedication today will become your confidence on exam day. Keep going!",

"Good morning! Focus on progress, not perfection. You've got this, mam!",

"Every question you practice is making you stronger and more prepared for IBPS.",

"Believe in yourself, mam! Your efforts are creating the future you dream of.",

"Another beautiful day to learn, revise, and move one step closer to your goal.",

"Stay patient, stay disciplined, and trust the process. Success takes time.",

"Good morning, mam! Let your determination be stronger than any challenge today.",

"One focused study session can make a big difference. Start today with purpose!",

"Your consistency is your superpower, mam. Keep showing up and keep improving.",

"Every sunrise is a reminder that you have another chance to make your dreams happen.",

"Don't count the hours, make the hours count. Your IBPS journey is worth it!",

"Good morning! Stay calm, study smart, and let your hard work speak for itself.",

"Today's revision is tomorrow's confidence. Keep building your success, mam!",

"Your goal is closer than it was yesterday. Keep working and keep believing.",

"Challenges are part of the journey, but your determination can take you through them.",

"Good morning, mam! Stay focused, stay positive, and make today another step toward IBPS success.",
]

# Source: IBPS Calendar 2026-27, released 16 Jan 2026 (official: ibps.in)
EXAM_DATES = {
    "IBPS Clerk Prelims": {"date": datetime(2026, 10, 10), "official": True},
    "IBPS RRB PO Prelims": {"date": datetime(2026, 11, 21), "official": True},
    "IBPS Clerk Mains": {"date": datetime(2026, 12, 27), "official": True},
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def days_left(target: datetime) -> int:
    return (target.date() - date.today()).days


def render_autorefresh(seconds: int):
    st.markdown(f"<meta http-equiv='refresh' content='{seconds}'>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(page_title="IBPS Countdown", page_icon="🌸", layout="centered")

render_autorefresh(CYCLE_SECONDS)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=Nunito:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    .stApp {
        background: linear-gradient(160deg, #fdf6f0 0%, #f6f2fb 45%, #f0f7f5 100%);
    }

    #MainMenu, footer, header {visibility: hidden;}

    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 720px;
    }

    /* ---------- Greeting ---------- */
    .hero {
        text-align: center;
        margin-bottom: 1.2rem;
    }
    .hero .emoji {
        font-size: 2.2rem;
        margin-bottom: 0.2rem;
    }
    .hero .greeting {
        font-family: 'Quicksand', sans-serif;
        font-size: 2.1rem;
        font-weight: 700;
        color: #4a4266;
        margin: 0;
        letter-spacing: 0.2px;
    }
    .hero .today {
        font-size: 1rem;
        color: #9691a8;
        margin-top: 0.35rem;
        font-weight: 600;
    }

    /* ---------- Navigation Buttons ---------- */
    div.stButton > button {
        background-color: #ffffff;
        color: #5c5570;
        border: 1px solid #e0c7e8;
        border-radius: 14px;
        font-family: 'Quicksand', sans-serif;
        font-weight: 700;
        font-size: 0.95rem;
        transition: all 0.25s ease;
        width: 100%;
        padding: 0.55rem 0.5rem;
    }
    div.stButton > button:hover {
        border-color: #a78bd4;
        color: #a78bd4;
        box-shadow: 0 4px 12px rgba(150, 130, 180, 0.15);
        transform: translateY(-1px);
    }
    div.stButton > button:active {
        background-color: #f6f2fb;
    }

    /* ---------- Section labels ---------- */
    .section-label {
        font-family: 'Quicksand', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        color: #6b6483;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin: 2rem 0 0.8rem 0;
        text-align: center;
    }

    /* ---------- Countdown cards ---------- */
    .countdown-row {
        display: flex;
        gap: 0.9rem;
        flex-wrap: wrap;
        justify-content: center;
    }
    .countdown-card {
        flex: 1;
        min-width: 200px;
        background: #ffffff;
        border-radius: 20px;
        padding: 1.4rem 1.2rem;
        text-align: center;
        box-shadow: 0 6px 20px rgba(150, 130, 180, 0.12);
        border: 1px solid #f1ecf7;
    }
    .countdown-number {
        font-family: 'Quicksand', sans-serif;
        font-size: 2.6rem;
        font-weight: 700;
        background: linear-gradient(135deg, #e08fa0, #a78bd4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
    }
    .countdown-name {
        font-size: 0.95rem;
        font-weight: 700;
        color: #5c5570;
        margin-top: 0.2rem;
    }
    .countdown-sub {
        font-size: 0.78rem;
        color: #aca6bd;
        margin-top: 0.3rem;
    }
    .unofficial-pill {
        display: inline-block;
        margin-top: 0.55rem;
        font-size: 0.68rem;
        font-weight: 700;
        color: #b3762f;
        background: #fdf0dd;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
    }

    /* ---------- Welcome message ---------- */
    .welcome-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 1.6rem 1.5rem;
        text-align: center;
        box-shadow: 0 6px 20px rgba(150, 130, 180, 0.12);
        border: 1px solid #f1ecf7;
        position: relative;
    }
    .welcome-card .quote-mark {
        font-size: 1.6rem;
        color: #e0c7e8;
        line-height: 0;
    }
    .welcome-card .msg {
        font-size: 1.15rem;
        font-weight: 600;
        color: #5c5570;
        margin-top: 0.4rem;
        line-height: 1.5;
    }
    .welcome-footer {
        text-align: center;
        font-size: 0.75rem;
        color: #bcb6cc;
        margin-top: 0.7rem;
    }
    .source-footer {
        text-align: center;
        font-size: 0.72rem;
        color: #c2bcd1;
        margin-top: 1.4rem;
    }
    .source-footer a {
        color: #a78bd4;
        text-decoration: none;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Greeting
# ---------------------------------------------------------------------------
today = date.today()
hero_html = (
    '<div class="hero">'
    '<div class="emoji">🌷</div>'
    '<p class="greeting">Good morning, Madam baby!</p>'
    f'<p class="today">{today.strftime("%A, %d %B %Y")}</p>'
    "</div>"
)
st.markdown(hero_html, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Quick Navigation Buttons (Centered Side-by-Side)
# ---------------------------------------------------------------------------
_, btn_col1, btn_col2, _ = st.columns([0.4, 1.2, 1.2, 0.4])

with btn_col1:
    if st.button("⏱️ Focus Timer", use_container_width=True):
        st.switch_page("pages/pomodoro.py")

with btn_col2:
    if st.button("📋 Task Board", use_container_width=True):
        st.switch_page("pages/kaban.py")

# ---------------------------------------------------------------------------
# Countdowns
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">Countdown to IBPS</div>', unsafe_allow_html=True)

card_parts = []
for name, info in EXAM_DATES.items():
    remaining = days_left(info["date"])
    if remaining >= 0:
        number_html = f'<div class="countdown-number">{remaining}</div>'
        sub_html = '<div class="countdown-sub">days to go</div>'
    else:
        number_html = f'<div class="countdown-number">Day {abs(remaining)}</div>'
        sub_html = '<div class="countdown-sub">since it started</div>'

    pill_html = (
        '<div class="unofficial-pill">⚠ estimated date</div>'
        if not info.get("official", True)
        else ""
    )

    card_parts.append(
        '<div class="countdown-card">'
        + number_html
        + f'<div class="countdown-name">{name}</div>'
        + sub_html
        + f'<div class="countdown-sub">{info["date"].strftime("%d %b %Y")}</div>'
        + pill_html
        + "</div>"
    )

cards_html = '<div class="countdown-row">' + "".join(card_parts) + "</div>"
st.markdown(cards_html, unsafe_allow_html=True)

st.markdown(
    '<div class="source-footer">Dates per the IBPS Calendar 2026-27 — tentative, '
    'confirm on <a href="https://www.ibps.in/" target="_blank">ibps.in</a></div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Cycling welcome message
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">A little cheer for you</div>', unsafe_allow_html=True)

idx = int(datetime.now().timestamp() // CYCLE_SECONDS) % len(WELCOME_MESSAGES)
welcome_html = (
    '<div class="welcome-card">'
    '<div class="quote-mark">❝</div>'
    f'<div class="msg">{WELCOME_MESSAGES[idx]}</div>'
    "</div>"
    f'<div class="welcome-footer">message {idx + 1} of {len(WELCOME_MESSAGES)} · refreshes every 2 hours</div>'
)
st.markdown(welcome_html, unsafe_allow_html=True)