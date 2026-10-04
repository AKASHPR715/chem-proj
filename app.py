"""
Periodic Table Quiz — A Streamlit app for 9th-grade Chemistry students.
=======================================================================
Loads questions from questions.csv, presents randomised multiple-choice
questions with hints, immediate feedback, and a live score dashboard.
"""

import random
import pathlib

import pandas as pd
import streamlit as st

# ──────────────────────────────────────────────
# 1. Page configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="⚗️ Periodic Table Quiz",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# 2. Custom CSS — vibrant, student-friendly theme
# ──────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ---------- Google Font ---------- */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    /* ---------- Root variables ---------- */
    :root {
        --primary:    #6C63FF;
        --primary-lt: #A29BFE;
        --accent:     #00D2FF;
        --success:    #00E676;
        --danger:     #FF5252;
        --bg-dark:    #0E1117;
        --card-bg:    rgba(30, 34, 46, 0.85);
        --text:       #F0F2F6;
        --text-muted: #8B8FA3;
    }

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }

    /* ---------- Glassmorphism cards ---------- */
    div[data-testid="stExpander"],
    section[data-testid="stSidebar"] > div {
        backdrop-filter: blur(12px);
    }

    /* ---------- Hero banner gradient ---------- */
    .hero-banner {
        background: linear-gradient(135deg, #6C63FF 0%, #00D2FF 50%, #00E676 100%);
        border-radius: 18px;
        padding: 2.2rem 2rem;
        margin-bottom: 1.8rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(108, 99, 255, 0.35);
        animation: fadeSlideIn 0.7s ease-out;
    }
    .hero-banner h1 {
        color: #fff;
        font-weight: 800;
        font-size: 2.2rem;
        margin: 0;
        text-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .hero-banner p {
        color: rgba(255,255,255,0.9);
        font-size: 1.08rem;
        margin: 0.5rem 0 0;
    }

    /* ---------- Score cards ---------- */
    .score-card {
        background: var(--card-bg);
        border: 1px solid rgba(108,99,255,0.25);
        border-radius: 14px;
        padding: 1.1rem 0.8rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .score-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 28px rgba(108,99,255,0.3);
    }
    .score-card .label {
        font-size: 0.82rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 4px;
    }
    .score-card .value {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* ---------- Question card ---------- */
    .question-card {
        background: var(--card-bg);
        border: 1px solid rgba(108,99,255,0.2);
        border-radius: 16px;
        padding: 1.8rem 1.6rem;
        margin: 1.2rem 0;
        box-shadow: 0 4px 24px rgba(0,0,0,0.2);
        animation: fadeSlideIn 0.5s ease-out;
    }
    .question-card .q-number {
        display: inline-block;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        color: #fff;
        font-weight: 700;
        font-size: 0.78rem;
        padding: 4px 14px;
        border-radius: 20px;
        margin-bottom: 0.8rem;
        letter-spacing: 0.5px;
    }
    .question-card .q-text {
        font-size: 1.22rem;
        font-weight: 600;
        color: var(--text);
        line-height: 1.55;
    }

    /* ---------- Feedback banners ---------- */
    .feedback {
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
        font-size: 1rem;
        animation: fadeSlideIn 0.45s ease-out;
    }
    .feedback.correct {
        background: rgba(0,230,118,0.12);
        border: 1px solid rgba(0,230,118,0.4);
        color: #A5D6A7;
    }
    .feedback.incorrect {
        background: rgba(255,82,82,0.12);
        border: 1px solid rgba(255,82,82,0.4);
        color: #EF9A9A;
    }
    .feedback strong { font-weight: 700; }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #12141C 0%, #1A1D2B 100%);
    }
    section[data-testid="stSidebar"] h2 {
        background: linear-gradient(135deg, var(--primary), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }

    /* ---------- Keyframes ---------- */
    @keyframes fadeSlideIn {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ---------- Button overrides ---------- */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        font-family: 'Outfit', sans-serif;
        transition: all 0.25s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(108,99,255,0.35);
    }

    /* ---------- Progress bar ---------- */
    .progress-wrap {
        background: rgba(255,255,255,0.06);
        border-radius: 10px;
        overflow: hidden;
        height: 10px;
        margin: 0.4rem 0 1rem;
    }
    .progress-fill {
        height: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        transition: width 0.5s ease;
    }

    /* ---------- Footer ---------- */
    .footer {
        text-align: center;
        color: var(--text-muted);
        font-size: 0.8rem;
        margin-top: 3rem;
        padding: 1rem 0;
        border-top: 1px solid rgba(255,255,255,0.06);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
# 3. Data loading
# ──────────────────────────────────────────────
CSV_PATH = pathlib.Path(__file__).parent / "questions.csv"

@st.cache_data
def load_questions() -> pd.DataFrame:
    """Load and validate the question bank from CSV."""
    df = pd.read_csv(CSV_PATH)
    required = {
        "id", "question", "option_a", "option_b",
        "option_c", "option_d", "correct_option", "hint", "explanation",
    }
    if not required.issubset(df.columns):
        st.error(f"CSV is missing columns: {required - set(df.columns)}")
        st.stop()
    return df


QUESTIONS = load_questions()
OPTION_MAP = {"A": "option_a", "B": "option_b", "C": "option_c", "D": "option_d"}

# ──────────────────────────────────────────────
# 4. Session-state initialisation
# ──────────────────────────────────────────────
DEFAULTS = {
    "score": 0,
    "attempted": 0,
    "current_q": None,      # current question row as dict
    "answered": False,
    "selected_option": None,
    "is_correct": None,
    "quiz_started": False,  # True once the user clicks Start
    "quiz_pool": [],        # shuffled list of question IDs for this round
    "num_questions": 10,    # how many questions the user chose
}

for key, val in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val if not isinstance(val, list) else list(val)


def _build_pool(n: int) -> list:
    """Return a shuffled list of `n` question IDs from the full bank."""
    all_ids = QUESTIONS["id"].tolist()
    random.shuffle(all_ids)
    return all_ids[:n]


def _pick_question() -> dict | None:
    """Pop the next question from the pre-shuffled pool, or None if done."""
    pool = st.session_state.quiz_pool
    if not pool:
        return None
    next_id = pool.pop(0)
    st.session_state.quiz_pool = pool  # persist the shortened list
    row = QUESTIONS[QUESTIONS["id"] == next_id].iloc[0]
    return row.to_dict()


def _start_quiz():
    """Initialise a new quiz round with the selected question count."""
    n = st.session_state.num_questions
    st.session_state.quiz_pool = _build_pool(n)
    st.session_state.score = 0
    st.session_state.attempted = 0
    st.session_state.answered = False
    st.session_state.selected_option = None
    st.session_state.is_correct = None
    st.session_state.quiz_started = True
    st.session_state.current_q = _pick_question()


def restart_quiz():
    """Reset state and go back to the setup screen."""
    for key, val in DEFAULTS.items():
        st.session_state[key] = val if not isinstance(val, list) else list(val)
    st.session_state.current_q = None


def next_question():
    """Move to the next question in the shuffled pool."""
    st.session_state.answered = False
    st.session_state.selected_option = None
    st.session_state.is_correct = None
    st.session_state.current_q = _pick_question()

# ──────────────────────────────────────────────
# 5. Hero banner
# ──────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-banner">
        <h1>⚗️ Periodic Table Quiz</h1>
        <p>Test your chemistry knowledge — one element at a time!</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
# 6. Sidebar — Score dashboard
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Score Dashboard")
    st.markdown("---")

    if not st.session_state.quiz_started:
        # ── Setup screen: choose number of questions ──
        total_available = len(QUESTIONS)
        st.markdown("**⚙️ Quiz Settings**")
        num_q = st.slider(
            "Number of questions",
            min_value=5,
            max_value=total_available,
            value=st.session_state.num_questions,
            step=1,
            key="_num_q_slider",
        )
        st.session_state.num_questions = num_q

        st.button(
            "🚀 Start Quiz",
            on_click=_start_quiz,
            use_container_width=True,
        )
        st.markdown("---")
        st.markdown(
            "**How to play**\n"
            "1. Choose how many questions\n"
            "2. Click **Start Quiz**\n"
            "3. Pick your answer & submit\n"
            "4. Review the explanation\n"
            "5. Click **Next Question ➜**"
        )
    else:
        # ── In-game dashboard ──
        accuracy = (
            round(st.session_state.score / st.session_state.attempted * 100, 1)
            if st.session_state.attempted > 0
            else 0
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                f'<div class="score-card"><div class="label">Score</div>'
                f'<div class="value">{st.session_state.score}</div></div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f'<div class="score-card"><div class="label">Attempted</div>'
                f'<div class="value">{st.session_state.attempted}</div></div>',
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                f'<div class="score-card"><div class="label">Accuracy</div>'
                f'<div class="value">{accuracy}%</div></div>',
                unsafe_allow_html=True,
            )

        # Accuracy progress bar
        st.markdown(
            f"""
            <div class="progress-wrap">
                <div class="progress-fill" style="width:{accuracy}%"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        chosen_total = st.session_state.num_questions
        remaining = len(st.session_state.quiz_pool)
        # remaining in pool doesn't include the current question being shown
        answered_count = st.session_state.attempted
        st.markdown(
            f"**Progress:** {answered_count} / {chosen_total} answered"
        )

        st.markdown("---")
        st.button("🔄 Restart Quiz", on_click=restart_quiz, use_container_width=True)

        st.markdown("---")
        st.markdown(
            "**How to play**\n"
            "1. Read the question\n"
            "2. Pick your answer\n"
            "3. Click **Submit Answer**\n"
            "4. Check the explanation\n"
            "5. Click **Next Question ➜**"
        )

# ──────────────────────────────────────────────
# 7. Main quiz area
# ──────────────────────────────────────────────
if not st.session_state.quiz_started:
    # Show a welcome prompt before the quiz begins
    st.markdown(
        """
        <div class="question-card" style="text-align:center;">
            <h2 style="color:#A29BFE;">👋 Welcome!</h2>
            <p style="font-size:1.1rem; color:#F0F2F6;">
                Choose how many questions you'd like in the <strong>sidebar</strong>,
                then hit <strong>Start Quiz</strong> to begin.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    q = st.session_state.current_q

    accuracy = (
        round(st.session_state.score / st.session_state.attempted * 100, 1)
        if st.session_state.attempted > 0
        else 0
    )

    if q is None:
        # All questions exhausted
        st.balloons()
        st.markdown("---")
        st.markdown(
            f"""
            <div class="question-card" style="text-align:center;">
                <h2 style="color:#00E676;">🎉 Congratulations!</h2>
                <p style="font-size:1.1rem; color:#F0F2F6;">
                    You've completed all <strong>{st.session_state.num_questions}</strong> questions!<br>
                    Final score: <strong>{st.session_state.score}</strong> / <strong>{st.session_state.attempted}</strong>
                    ({accuracy}% accuracy)
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button("🔄 Play Again", on_click=restart_quiz, use_container_width=True)
    else:
        # ------ Question card ------
        q_index = st.session_state.attempted + 1 if not st.session_state.answered else st.session_state.attempted
        st.markdown(
            f"""
            <div class="question-card">
                <span class="q-number">QUESTION {q_index} / {st.session_state.num_questions}</span>
                <div class="q-text">{q["question"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ------ Hint expander ------
        with st.expander("💡 Need a Hint?"):
            st.info(q["hint"])

        # ------ Answer options ------
        options = {
            f"A) {q['option_a']}": "A",
            f"B) {q['option_b']}": "B",
            f"C) {q['option_c']}": "C",
            f"D) {q['option_d']}": "D",
        }

        if not st.session_state.answered:
            selected_label = st.radio(
                "Choose your answer:",
                list(options.keys()),
                index=None,
                key=f"radio_{q['id']}",
            )

            # ------ Submit button ------
            if st.button("✅ Submit Answer", use_container_width=True):
                if selected_label is None:
                    st.warning("Please select an option first!")
                else:
                    chosen_letter = options[selected_label]
                    correct_letter = q["correct_option"].strip().upper()
                    is_correct = chosen_letter == correct_letter

                    # Update session state
                    st.session_state.answered = True
                    st.session_state.selected_option = chosen_letter
                    st.session_state.is_correct = is_correct
                    st.session_state.attempted += 1
                    if is_correct:
                        st.session_state.score += 1

                    st.rerun()
        else:
            # Show the previously selected option (disabled state)
            chosen = st.session_state.selected_option
            correct = q["correct_option"].strip().upper()
            correct_col = OPTION_MAP[correct]
            correct_text = q[correct_col]

            # Feedback banner
            if st.session_state.is_correct:
                st.markdown(
                    f"""
                    <div class="feedback correct">
                        <strong>✅ Correct!</strong>  Great job! 🎉
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class="feedback incorrect">
                        <strong>❌ Incorrect.</strong>  The correct answer was
                        <strong>{correct}) {correct_text}</strong>.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Explanation
            with st.expander("📖 Explanation", expanded=True):
                st.markdown(q["explanation"])

            # Next question button
            st.button("Next Question ➜", on_click=next_question, use_container_width=True)

# ──────────────────────────────────────────────
# 8. Footer
# ──────────────────────────────────────────────
st.markdown(
    """
    <div class="footer">
        &nbsp;·&nbsp;
        Powered by <strong>Streamlit</strong>
    </div>
    """,
    unsafe_allow_html=True,
)
