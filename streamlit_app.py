import streamlit as st

from short_urls import expand_short_url, get_short_url_button
from stlite_sandbox import stlite_sandbox

st.set_page_config(
    page_title="Streamlit Sandbox", page_icon=":sunglasses:", layout="wide"
)

HEIGHT = 600
DEFAULT_CODE = """import streamlit as st
import pandas as pd
import numpy as np

st.title("Hello world!")

if "seed" not in st.session_state:
    st.session_state["seed"] = 42

if st.button("Regenerate random numbers"):
    st.session_state["seed"] += 1

def get_data():
    np.random.seed(st.session_state.seed)
    return pd.DataFrame({"a": np.random.randn(5), "b": np.random.randn(5)})

df = get_data()

col1, col2 = st.columns([1, 2])

df_edited = col1.data_editor(df)

col2.line_chart(df_edited)
"""

DEFAULT_DEPENDENCIES = ["streamlit-extras"]
KEY = "stlite_sandbox"

if st.session_state.get(KEY, None):
    code = st.session_state[KEY]["code"]
    requirements = st.session_state[KEY]["requirements"]
else:
    resp = expand_short_url()
    if resp is not None:
        code, raw_reqs = resp
        if isinstance(raw_reqs, str):
            requirements = [r for r in raw_reqs.splitlines() if r]
        else:
            requirements = raw_reqs
    else:
        code, requirements = DEFAULT_CODE, DEFAULT_DEPENDENCIES

should_show_code = st.query_params.get("code", "1") == "1"


def update_code_query_param():
    should_show_code = st.session_state["show_code"]
    st.query_params["code"] = "1" if should_show_code else "0"


main, footer = st.empty(), st.empty()

with footer.container():
    show_code = st.toggle(
        "Show editor",
        value=should_show_code,
        on_change=update_code_query_param,
        key="show_code",
    )

with main.container():
    code, requirements = stlite_sandbox(
        code=code,
        height=HEIGHT + 15,
        requirements=requirements,
        scrollable=True,
        editor=show_code,
        requirements_picker=True,
        key=KEY,
        theme="vs-dark",
    )
    if not show_code:
        with st.expander("Code"):
            st.code(code, language="python")


if show_code:
    get_short_url_button(
        code=code,
        requirements="\n".join(requirements),
        show_custom_hash=False,
    )
