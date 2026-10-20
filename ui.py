"""
Steady Step - visual components (HTML/CSS helpers for Streamlit)
Presentation only: no data processing happens in this file.
"""

import html

import streamlit as st

STATUS_STYLE = {  # status -> (text colour, background, icon)
    "On track": ("#137A4B", "#E3F7EC", "●"),
    "Worth keeping an eye on": ("#8A5A00", "#FFF4D6", "●"),
    "Suggested check-in": ("#B23A1E", "#FFE7DF", "●"),
}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], .stMarkdown, .stText, button, input, textarea, select {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.stApp { background: #F7F5FF; }
.block-container { padding-top: 1.6rem; max-width: 1200px; }
section[data-testid="stSidebar"] { background: linear-gradient(180deg, #2E1A6B 0%, #4A2BA8 100%); }
section[data-testid="stSidebar"] * { color: #F1ECFF !important; }
[data-testid="stSidebar"] [data-testid="stSelectbox"] div:has(> input),
[data-testid="stSidebar"] [data-baseweb="select"] > div {
  background: rgba(255,255,255,.14) !important; border: 1px solid rgba(255,255,255,.35) !important;
  border-radius: 10px; }
[data-testid="stSidebar"] [data-testid="stSelectbox"] input,
[data-testid="stSidebar"] [data-baseweb="select"] * { color: #FFFFFF !important;
  -webkit-text-fill-color: #FFFFFF !important; }
h1, h2, h3 { color: #1F1A33; letter-spacing: -0.02em; }

.ss-hero { background: linear-gradient(120deg, #2E1A6B 0%, #7C4DFF 60%, #A88BFF 100%);
  border-radius: 22px; padding: 28px 32px; color: #fff; margin-bottom: 18px;
  box-shadow: 0 12px 30px rgba(76, 43, 168, .25); }
.ss-hero h1 { color: #fff; font-size: 2.1rem; margin: 0 0 6px 0; font-weight: 800; }
.ss-hero p { margin: 0; opacity: .9; font-size: 1.02rem; }
.ss-chip { display: inline-block; background: rgba(255,255,255,.18); border: 1px solid rgba(255,255,255,.35);
  padding: 4px 12px; border-radius: 999px; font-size: .8rem; margin: 12px 8px 0 0; }

.ss-card { background: #fff; border-radius: 18px; padding: 18px 20px; border: 1px solid #ECE6FF;
  box-shadow: 0 4px 14px rgba(46, 26, 107, .06); height: 100%; }
.ss-kpi-label { font-size: .82rem; color: #6B6385; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; }
.ss-kpi-value { font-size: 2.1rem; font-weight: 800; color: #1F1A33; line-height: 1.15; margin-top: 4px; }
.ss-kpi-icon { float: right; font-size: 1.6rem; }

.ss-pill { display: inline-block; padding: 5px 14px; border-radius: 999px; font-weight: 700; font-size: .9rem; }
.ss-reason { background: #F3EEFF; color: #3A2A7A; border-radius: 12px; padding: 10px 14px;
  margin: 8px 0; font-size: .95rem; border-left: 4px solid #7C4DFF; }

.ss-ind { border-radius: 16px; padding: 16px 18px; border: 2px solid #ECE6FF; background: #fff; height: 100%; }
.ss-ind.on { border-color: #F26B4F; background: #FFF6F3; }
.ss-ind-title { font-weight: 700; color: #1F1A33; }
.ss-ind-val { color: #6B6385; font-size: .9rem; margin-top: 4px; }
.ss-ind-flag { float: right; font-weight: 800; font-size: .8rem; padding: 2px 10px; border-radius: 999px; }
.ss-ind.on .ss-ind-flag { background: #F26B4F; color: #fff; }
.ss-ind.off .ss-ind-flag { background: #E3F7EC; color: #137A4B; }

.ss-adv { text-align: center; }
.ss-avatar { width: 58px; height: 58px; border-radius: 50%; margin: 0 auto 10px auto; display: flex;
  align-items: center; justify-content: center; color: #fff; font-weight: 800; font-size: 1.2rem; }
.ss-adv-name { font-weight: 700; color: #1F1A33; }
.ss-adv-role { color: #6B6385; font-size: .85rem; margin-top: 2px; }

.ss-session { display: flex; gap: 14px; align-items: center; background: #fff; border-radius: 14px;
  padding: 12px 16px; border: 1px solid #ECE6FF; margin-bottom: 8px; }
.ss-date { background: #7C4DFF; color: #fff; border-radius: 12px; padding: 6px 12px; text-align: center;
  font-weight: 800; line-height: 1.1; min-width: 56px; }
.ss-date small { display: block; font-weight: 600; font-size: .7rem; opacity: .9; }

.ss-test { background: #fff; border-radius: 16px; padding: 16px 20px; border: 1px solid #ECE6FF; margin-bottom: 12px; }
.ss-test-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.ss-test-id { font-weight: 800; color: #7C4DFF; margin-right: 8px; }
.ss-pass { background: #E3F7EC; color: #137A4B; font-weight: 800; padding: 4px 12px; border-radius: 999px; }
.ss-fail { background: #FFE7DF; color: #B23A1E; font-weight: 800; padding: 4px 12px; border-radius: 999px; }
.ss-grid { display: grid; grid-template-columns: 110px 1fr; gap: 4px 12px; font-size: .92rem; }
.ss-grid b { color: #6B6385; font-weight: 600; }

div[data-testid="stForm"] { background: #fff; border-radius: 18px; border: 1px solid #ECE6FF; padding: 18px; }
div[data-testid="stDataFrame"], div[data-testid="stDataEditor"] { border-radius: 14px; overflow: hidden; }
.stButton button[kind="primary"], div[data-testid="stFormSubmitButton"] button {
  border-radius: 12px; font-weight: 700; padding: .55rem 1.2rem; }
</style>
"""

AVATAR_COLOURS = ["#7C4DFF", "#2BB673", "#F5A524"]


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def hero(title, subtitle, chips=()):
    chip_html = "".join(f'<span class="ss-chip">{html.escape(c)}</span>' for c in chips)
    st.markdown(f'<div class="ss-hero"><h1>{html.escape(title)}</h1>'
                f'<p>{html.escape(subtitle)}</p>{chip_html}</div>', unsafe_allow_html=True)


def kpi(col, label, value, icon=""):
    col.markdown(f'<div class="ss-card"><span class="ss-kpi-icon">{icon}</span>'
                 f'<div class="ss-kpi-label">{html.escape(label)}</div>'
                 f'<div class="ss-kpi-value">{html.escape(str(value))}</div></div>', unsafe_allow_html=True)


def pill(status):
    fg, bg, dot = STATUS_STYLE[status]
    return f'<span class="ss-pill" style="color:{fg};background:{bg}">{dot} {html.escape(status)}</span>'


def reasons(items):
    st.markdown("".join(f'<div class="ss-reason">{html.escape(r)}</div>' for r in items),
                unsafe_allow_html=True)


def indicator(col, title, value, triggered):
    cls, flag = ("on", "TRIGGERED") if triggered else ("off", "OK")
    col.markdown(f'<div class="ss-ind {cls}"><span class="ss-ind-flag">{flag}</span>'
                 f'<div class="ss-ind-title">{html.escape(title)}</div>'
                 f'<div class="ss-ind-val">{html.escape(value)}</div></div>', unsafe_allow_html=True)


def adviser_cards(advisers):
    cols = st.columns(len(advisers))
    for i, (col, (name, desc)) in enumerate(zip(cols, advisers.items())):
        initials = "".join(p[0] for p in name.split())
        role, _, focus = desc.partition(" - ")
        col.markdown(f'<div class="ss-card ss-adv"><div class="ss-avatar" style="background:{AVATAR_COLOURS[i % 3]}">'
                     f'{initials}</div><div class="ss-adv-name">{html.escape(name)}</div>'
                     f'<div class="ss-adv-role">{html.escape(role)}</div>'
                     f'<div class="ss-adv-role">{html.escape(focus)}</div></div>', unsafe_allow_html=True)


def sessions(bookings):
    if not bookings:
        st.markdown('<div class="ss-card" style="color:#6B6385">No conversations booked yet.</div>',
                    unsafe_allow_html=True)
        return
    out = ""
    for b in sorted(bookings, key=lambda b: (b["date"], b["time"])):
        out += (f'<div class="ss-session"><div class="ss-date">{b["date"]:%d}<small>{b["date"]:%b}</small></div>'
                f'<div><b>{html.escape(b["adviser"])}</b> · {b["time"]}<br>'
                f'<span style="color:#6B6385;font-size:.88rem">{b["date"]:%A} · {b["learner_id"]} · '
                f'<span style="color:#137A4B;font-weight:700">✓ {b["status"]}</span></span></div></div>')
    st.markdown(out, unsafe_allow_html=True)


def test_card(t):
    badge = '<span class="ss-pass">✓ PASS</span>' if t["passed"] else '<span class="ss-fail">✗ FAIL</span>'
    st.markdown(
        f'<div class="ss-test"><div class="ss-test-head"><div><span class="ss-test-id">{t["id"]}</span>'
        f'<b>{html.escape(t["type"])}</b></div>{badge}</div><div class="ss-grid">'
        f'<b>Input</b><span>{html.escape(t["input"])}</span>'
        f'<b>Expected</b><span>{html.escape(t["expected"])}</span>'
        f'<b>Actual</b><span>{html.escape(t["actual"])}</span></div></div>', unsafe_allow_html=True)
