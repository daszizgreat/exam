import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import os
from pathlib import Path
from io import BytesIO
import pandas as pd

# ----------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Kanban Board",
    page_icon="🐱",
    layout="wide",
)

# ----------------------------------------------------------------------
# MONGODB CONNECTION
# ----------------------------------------------------------------------
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://soumyadeepdas2511:dxRsCQDq7YQSc1vh"
    "@cluster0.zmm4k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)

DB_NAME = "kanban_todo_db"
COLLECTION_NAME = "tasks"


@st.cache_resource
def get_collection():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db[COLLECTION_NAME]


tasks_col = get_collection()

STATUSES = ["Will Do", "Doing", "Done"]
NEXT_STATUS = {"Will Do": "Doing", "Doing": "Done"}
PREV_STATUS = {"Doing": "Will Do", "Done": "Doing"}

# ----------------------------------------------------------------------
# STYLING
# ----------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Quicksand:wght@500;600;700&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Poppins', sans-serif;
        }

        .stApp {
            background: linear-gradient(180deg, #fdf6f0 0%, #f7f2fb 100%);
        }

        .kanban-hero {
            background: linear-gradient(120deg, #b9c9f4 0%, #d9c7ef 35%, #f3c9dd 70%, #294b8f 100%);
            border-radius: 22px;
            padding: 38px 34px 30px 34px;
            margin-bottom: 26px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(80, 60, 120, 0.18);
        }
        .kanban-hero::before {
            content: "✦";
            position: absolute;
            top: 18px; right: 60px;
            font-size: 22px;
            color: #ffd166;
            opacity: 0.9;
        }
        .kanban-hero::after {
            content: "✧";
            position: absolute;
            bottom: 24px; left: 80px;
            font-size: 18px;
            color: #fff;
            opacity: 0.8;
        }
        .kanban-hero h1 {
            color: #3a2e52;
            font-family: 'Quicksand', sans-serif;
            font-weight: 700;
            font-size: 2.1rem;
            margin: 0 0 6px 0;
        }
        .kanban-hero p {
            color: #4a3f66;
            font-size: 0.95rem;
            margin: 0;
            opacity: 0.85;
        }
        .kanban-cat {
            font-size: 2.4rem;
        }

        .quote-banner {
            background: #fdeaf1;
            border-left: 4px solid #e79cc2;
            padding: 10px 16px;
            border-radius: 8px;
            font-size: 0.92rem;
            color: #7a4a63;
            margin-bottom: 22px;
        }

        .col-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 14px;
        }
        .col-badge {
            font-family: 'Quicksand', sans-serif;
            font-weight: 700;
            font-size: 0.95rem;
            padding: 5px 14px;
            border-radius: 20px;
            color: white;
        }
        .badge-will-do { background: linear-gradient(120deg, #a3a8d6, #8f94c9); }
        .badge-doing   { background: linear-gradient(120deg, #7fb8e0, #5f9fd6); }
        .badge-done    { background: linear-gradient(120deg, #7fd6a0, #5fc78a); }

        .col-count {
            background: #f1eef7;
            color: #6b6386;
            font-size: 0.78rem;
            font-weight: 600;
            padding: 2px 10px;
            border-radius: 12px;
        }

        .task-card {
            background: #ffffff;
            border-radius: 14px;
            padding: 14px 16px 10px 16px;
            margin-bottom: 12px;
            box-shadow: 0 3px 10px rgba(120, 100, 160, 0.10);
            border: 1px solid #f0ecf7;
            transition: transform 0.15s ease;
        }
        .task-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(120, 100, 160, 0.18);
        }
        .task-title {
            font-size: 0.95rem;
            color: #3a2e52;
            font-weight: 500;
            margin-bottom: 2px;
            word-wrap: break-word;
        }
        .task-title.done-title {
            text-decoration: line-through;
            color: #9c94b3;
        }
        .task-meta {
            font-size: 0.7rem;
            color: #b1a9c4;
        }

        .empty-col {
            text-align: center;
            color: #c3bcd6;
            font-size: 0.85rem;
            padding: 18px 0;
            font-style: italic;
        }

        div.stButton > button {
            border-radius: 20px;
            border: none;
            font-size: 0.72rem;
            padding: 2px 10px;
            font-weight: 600;
        }

        .add-task-wrap {
            background: #ffffff;
            border-radius: 16px;
            padding: 18px 20px;
            margin-bottom: 24px;
            box-shadow: 0 3px 10px rgba(120, 100, 160, 0.10);
            border: 1px solid #f0ecf7;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# HERO / HEADER
# ----------------------------------------------------------------------
st.markdown(
    """
    <div class="kanban-hero">
        <div class="kanban-cat">🐱✨</div>
        <h1>kanban board °˖✧</h1>
        <p>Discipline is the bridge between goals and accomplishment</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# AUDIO TRIGGER (plays once, right after a task is marked Done)
# ----------------------------------------------------------------------
if st.session_state.get("play_audio"):
    audio_path = Path(__file__).parent / "audio.ogg"  # looks inside pages/, next to this file
    if audio_path.exists():
        with open(audio_path, "rb") as f:
            st.audio(f.read(), format="audio/ogg", autoplay=True)
    else:
        st.warning(
            "🔇 Couldn't find `audio.ogg` next to kaban.py — add your sound file "
            "to hear it play when a task is completed."
        )
    st.session_state.play_audio = False

# ----------------------------------------------------------------------
# ADD NEW TASK
# ----------------------------------------------------------------------
with st.container():
    st.markdown('<div class="add-task-wrap">', unsafe_allow_html=True)
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        new_task = st.text_input(
            "New task", placeholder="Add a new task…", label_visibility="collapsed"
        )
    with col_btn:
        add_clicked = st.button("➕ Add", use_container_width=True)
    if add_clicked and new_task.strip():
        tasks_col.insert_one(
            {
                "title": new_task.strip(),
                "status": "Will Do",
                "created_at": datetime.utcnow(),
                "finished_at": None,
            }
        )
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# EXCEL EXPORT
# ----------------------------------------------------------------------
def build_excel_bytes():
    records = list(tasks_col.find({}).sort("created_at", 1))
    rows = []
    for r in records:
        rows.append(
            {
                "Task": r.get("title", ""),
                "Status": r.get("status", ""),
                "Added": r["created_at"].strftime("%Y-%m-%d %H:%M") if r.get("created_at") else "",
                "Finished": r["finished_at"].strftime("%Y-%m-%d %H:%M") if r.get("finished_at") else "",
            }
        )
    df = pd.DataFrame(rows, columns=["Task", "Status", "Added", "Finished"])

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Tasks")
        sheet = writer.sheets["Tasks"]
        # a little auto-width so columns aren't cramped
        for col_cells in sheet.columns:
            length = max(len(str(c.value)) if c.value is not None else 0 for c in col_cells)
            sheet.column_dimensions[col_cells[0].column_letter].width = max(12, length + 2)
    buffer.seek(0)
    return buffer


dl_col1, dl_col2 = st.columns([5, 1])
with dl_col2:
    st.download_button(
        label="⬇️ Export Excel",
        data=build_excel_bytes(),
        file_name=f"tasks_{datetime.utcnow().strftime('%Y-%m-%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

st.markdown("<div style='margin-bottom: 18px;'></div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# BOARD
# ----------------------------------------------------------------------
columns = st.columns(3)
badge_class = {"Will Do": "badge-will-do", "Doing": "badge-doing", "Done": "badge-done"}

for col, status in zip(columns, STATUSES):
    with col:
        tasks = list(tasks_col.find({"status": status}).sort("created_at", 1))
        st.markdown(
            f"""
            <div class="col-header">
                <span class="col-badge {badge_class[status]}">{status}</span>
                <span class="col-count">{len(tasks)}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not tasks:
            st.markdown('<div class="empty-col">No tasks here yet</div>', unsafe_allow_html=True)

        for task in tasks:
            task_id = str(task["_id"])
            title_class = "task-title done-title" if status == "Done" else "task-title"
            check = "✅" if status == "Done" else "⬜"
            st.markdown(
                f"""
                <div class="task-card">
                    <div class="{title_class}">{check} {task['title']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            btn_cols = st.columns([1, 1, 1])
            with btn_cols[0]:
                if status in PREV_STATUS:
                    if st.button("←", key=f"prev_{task_id}"):
                        update = {"status": PREV_STATUS[status]}
                        if status == "Done":
                            update["finished_at"] = None  # un-completing clears the finish time
                        tasks_col.update_one({"_id": task["_id"]}, {"$set": update})
                        st.rerun()
            with btn_cols[1]:
                if status in NEXT_STATUS:
                    if st.button("→", key=f"next_{task_id}"):
                        target = NEXT_STATUS[status]
                        update = {"status": target}
                        if target == "Done":
                            update["finished_at"] = datetime.utcnow()
                        tasks_col.update_one({"_id": task["_id"]}, {"$set": update})
                        if target == "Done":
                            st.session_state.play_audio = True
                        st.rerun()
            with btn_cols[2]:
                if st.button("🗑", key=f"del_{task_id}"):
                    tasks_col.delete_one({"_id": task["_id"]})
                    st.rerun()