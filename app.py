"""
Steady Step - DEMO artefact (Streamlit)
INFOMGMT 399 Group 2 (The Big 4) - Proposal 2: Student Dropout Risk

Core journey:  synthetic data -> day-21 indicators -> flag + reason (adviser)
               -> adviser decision -> student sees own status -> books adviser -> confirmation
Run:  streamlit run app.py
"""

import inspect
from datetime import date, timedelta

import streamlit as st

import rules
import ui
from booking import ADVISERS, TIME_SLOTS, make_booking
from scenarios import run_all

st.set_page_config(page_title="Steady Step - Group 2", page_icon="🌱", layout="wide")
ui.inject_css()


# ---------------- 1. DATA (input) ----------------
@st.cache_data
def get_data():
    with st.spinner("Preparing synthetic dataset (first run only)..."):
        data = rules.load_data()
    return data, rules.build_checkpoint_features(data)


data, features = get_data()
st.session_state.setdefault("bookings", [])          # simulated storage (this session only)
st.session_state.setdefault("decisions", {})

# ---------------- Sidebar: test accounts + navigation ----------------
st.sidebar.markdown("## 🌱 Steady Step")
st.sidebar.caption("Group 2 · The Big 4  \nProposal 2: Student Dropout Risk")
role = st.sidebar.radio("Signed in as", ["Adviser", "Student"], horizontal=True)

if role == "Adviser":
    page = st.sidebar.radio("Go to", ["1. Learners to check in with", "2. Data & logic",
                                      "3. Test scenarios", "4. Status"])
    st.sidebar.markdown("---\n**⚙️ Rule settings** (adviser input)")
    pct = st.sidebar.slider("Low activity = bottom X% of course", 10, 50, 25, 5)
    min_ind = st.sidebar.slider("Flag when at least N indicators", 1, 3, 2)
else:
    learner_id = st.sidebar.selectbox("Test learner account", features.learner_id)
    page, pct, min_ind = "Student", 25, 2
st.sidebar.markdown("---")
st.sidebar.caption("Checkpoint: end of Week 3 (day 21)  \nSynthetic data · test accounts only")

# ---------------- 2. PROCESSING (re-runs on every input change) ----------------
results = rules.apply_rules(features, activity_percentile=pct, min_indicators=min_ind)


def booking_form(learner, key):
    with st.form(key, clear_on_submit=True):
        adviser = st.selectbox("Choose an adviser", list(ADVISERS))
        c1, c2 = st.columns(2)
        day = c1.date_input("Date", value=date.today() + timedelta(days=1), min_value=date.today())
        time = c2.selectbox("Time", TIME_SLOTS)
        if st.form_submit_button("Book conversation", type="primary"):
            ok, msg = make_booking(st.session_state.bookings, learner, adviser, day, time)
            if ok:
                st.session_state[f"{key}_done"] = msg
                st.rerun()                      # refresh so the new booking shows everywhere
            st.error(msg)
    done = st.session_state.pop(f"{key}_done", None)
    if done:
        st.success("✅ " + done)
        st.caption("📧 Simulated: a confirmation email would be sent.")


# ---------------- 3. OUTPUT ----------------
if role == "Student":
    me = results[results.learner_id == learner_id].iloc[0]       # own record only
    ui.hero("Kia ora 👋", f"Here's how your first three weeks in {me.course_code} are going.",
            [f"Account {learner_id}", "Only you can see this page"])

    left, right = st.columns([3, 2])
    with left:
        st.markdown(f'<div class="ss-card"><div class="ss-kpi-label">Your status</div>'
                    f'<div style="margin:10px 0 6px 0">{ui.pill(me.status)}</div></div>',
                    unsafe_allow_html=True)
        if me.student_reasons:
            ui.reasons(me.student_reasons)
            st.caption("Lots of students go through this - a short conversation can help.")
        else:
            st.markdown('<div class="ss-reason">You\'re engaging well so far - keep it up! 🎉</div>',
                        unsafe_allow_html=True)
    with right:
        st.markdown("#### 📅 Upcoming conversations")
        ui.sessions([b for b in st.session_state.bookings if b["learner_id"] == learner_id])

    st.write("")
    c1, c2, c3 = st.columns(3)
    ui.kpi(c1, "Canvas interactions", int(me.interactions_to_day21), "🖱️")
    ui.kpi(c2, "Active days", int(me.active_days_to_day21), "📆")
    ui.kpi(c3, "First quiz", me.first_quiz_status.capitalize(), "📝")

    st.markdown("### 💬 Meet an Advisor")
    st.caption("Asking early is a strength. It's free, confidential - and you decide whether to book.")
    ui.adviser_cards(ADVISERS)
    st.write("")
    booking_form(learner_id, "student_booking")

elif page.startswith("1."):
    ui.hero("Learners to check in with",
            "Suggestions at the end of Week 3. You decide what happens next.",
            ["Checkpoint: day 21", f"Low activity ≤ {pct}th percentile", f"Flag at {min_ind}+ indicators",
             "Protected attributes not used"])
    c1, c2, c3, c4 = st.columns(4)
    ui.kpi(c1, "Learners", len(results), "👥")
    ui.kpi(c2, "Suggested check-in", int(results.flagged.sum()), "🟠")
    ui.kpi(c3, "Keep an eye on", int((results.status == "Worth keeping an eye on").sum()), "🟡")
    ui.kpi(c4, "Flag rate", f"{100 * results.flagged.mean():.1f}%", "📊")

    st.markdown("### Suggested check-ins")
    flagged = results[results.flagged].copy()
    flagged["decision"] = flagged.learner_id.map(st.session_state.decisions).fillna("Not reviewed")
    edited = st.data_editor(
        flagged[["learner_id", "course_code", "indicator_count", "reasons", "decision"]],
        column_config={
            "learner_id": "Learner", "course_code": "Course",
            "indicator_count": st.column_config.ProgressColumn("Indicators", min_value=0, max_value=3,
                                                               format="%d / 3"),
            "reasons": st.column_config.TextColumn("Reason", width="large"),
            "decision": st.column_config.SelectboxColumn(
                "Your decision", options=["Not reviewed", "Contact learner", "Monitor", "No action"])},
        disabled=["learner_id", "course_code", "indicator_count", "reasons"],
        hide_index=True, width="stretch", height=320, key="editor")
    st.session_state.decisions.update(dict(zip(edited.learner_id, edited.decision)))
    reviewed = sum(v != "Not reviewed" for v in st.session_state.decisions.values())
    st.caption(f"Reviewed {reviewed} of {len(flagged)} suggestions")

    st.markdown("### Learner detail")
    pick = st.selectbox("Choose a learner", results.learner_id)
    row = results[results.learner_id == pick].iloc[0]
    st.markdown(f"**{pick}** · {row.course_code} &nbsp; {ui.pill(row.status)}", unsafe_allow_html=True)
    st.write("")
    i1, i2, i3 = st.columns(3)
    ui.indicator(i1, "Low Canvas activity",
                 f"Percentile {row.activity_percentile} · {row.interactions_to_day21} interactions",
                 row.low_activity)
    ui.indicator(i2, "First quiz late / missing", f"Status: {row.first_quiz_status}", row.first_quiz_issue)
    ui.indicator(i3, "Late registration", f"Registered on day {int(row.registration_day)}",
                 row.late_registration)
    st.write("")
    with st.expander("📅 Book a conversation for this learner"):
        booking_form(pick, "adviser_booking")
    st.markdown("### Booked conversations")
    ui.sessions(st.session_state.bookings)

elif page.startswith("2."):
    ui.hero("Data & logic", "How a learner goes from raw data to a suggestion with a reason.",
            ["Input → processing → output", "Rule-based, explainable"])
    st.markdown("### Architecture")
    st.graphviz_chart("""
digraph {
  rankdir=TB; bgcolor="transparent";
  node [shape=box style="rounded,filled" fillcolor="#F3EEFF" color="#7C4DFF" fontname="Helvetica" fontsize=16];
  edge [fontname="Helvetica" fontsize=13 color="#4A2BA8"];
  csv  [label="Synthetic CSVs\\n(generate_data.py)" fillcolor="#E3F7EC" color="#2BB673"];
  feat [label="build_checkpoint_features\\nkeep data <= day 21"];
  set  [label="Adviser sliders" shape=note fillcolor="#FFF4D6" color="#F5A524"];
  rule [label="apply_rules\\n3 indicators -> flag + reason"];
  ui   [label="Adviser / Student views" fillcolor="#FFE7DF" color="#F26B4F"];
  book [label="make_booking -> confirmation" fillcolor="#FFE7DF" color="#F26B4F"];
  csv -> feat [label="activity, quiz, registration"];
  feat -> rule [label="1 row per learner"];
  set -> rule [label="X%, N"];
  rule -> ui [label="status + reasons"];
  ui -> book [label="booking request"];
}""")
    st.markdown("### Data source")
    cols = st.columns(4)
    for col, (name, icon) in zip(cols, [("learners", "👥"), ("learning_activity", "🖱️"),
                                        ("submissions", "📝"), ("registrations", "🗂️")]):
        ui.kpi(col, name.replace("_", " "), f"{len(data[name]):,}", icon)
    st.caption("Plus courses, assessments and learning_resources · 400 fictional learners · 3 courses · 2026S2 · "
               "generated by us from the teaching team's data structure")
    tbl = st.selectbox("Preview a table", list(data))
    st.dataframe(data[tbl].head(10), width="stretch")
    u, n = st.columns(2)
    u.markdown('<div class="ss-card"><div class="ss-kpi-label">✅ Used (up to day 21)</div>'
               '<p>Learning activity · first quiz submission · registration day</p></div>', unsafe_allow_html=True)
    n.markdown('<div class="ss-card"><div class="ss-kpi-label">🚫 Never used</div>'
               '<p>Final outcome · later data · gender · age · deprivation · accessibility</p></div>',
               unsafe_allow_html=True)
    st.markdown("### Core rule - `rules.apply_rules`")
    st.code(inspect.getsource(rules.apply_rules).split("def reasons")[0], language="python")

elif page.startswith("3."):
    tests = run_all()
    passed = int(tests.passed.sum())
    ui.hero("Test scenarios", "Each test calls the real functions and compares expected with actual.",
            [f"{passed} / {len(tests)} passed", "Normal · boundary · error"])
    for t in tests.to_dict("records"):
        ui.test_card(t)

else:
    ui.hero("Status & AI use", "What works, what is simulated, and what is planned.")
    items = [("✅", "Working", ["Synthetic dataset (7 tables)", "Day-21 indicators, flag rule, reasons",
                               "Adviser list, decisions, learner detail", "Student status view and booking"]),
             ("🟡", "Simulated", ["Email confirmation", "Login (test accounts)",
                                 "Storage - resets when the app restarts"]),
             ("⚪", "Planned", ["Real Canvas / LMS data", "Fairness dashboard", "Consent flow"])]
    for col, (icon, title, lst) in zip(st.columns(3), items):
        col.markdown(f'<div class="ss-card"><div class="ss-kpi-label">{icon} {title}</div>'
                     + "".join(f"<p style='margin:8px 0'>{x}</p>" for x in lst) + "</div>",
                     unsafe_allow_html=True)
    st.write("")
