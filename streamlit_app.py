import streamlit as st
from stlite_sandbox import stlite_sandbox
from short_urls import get_short_url_button, expand_short_url

st.set_page_config(
    page_title="Streamlit Sandbox", page_icon=":sunglasses:", layout="wide"
)

HEIGHT = 600
DEFAULT_CODE = """import streamlit as st
import pandas as pd
import numpy as np

st.title("Hello world!")

st.button("Regenerate random numbers")

df = pd.DataFrame({"a": np.random.randn(5), "b": np.random.randn(5)})

col1, col2 = st.columns([1, 2])

df_edited = col1.data_editor(df)

col2.line_chart(df_edited)
"""

DEFAULT_DEPENDENCIES = ["streamlit-extras"]

resp = expand_short_url()
if resp is not None:
    code, raw_reqs = resp
    if isinstance(raw_reqs, str):
        requirements = [r for r in raw_reqs.splitlines() if r]
    else:
        requirements = raw_reqs
else:
    code, requirements = DEFAULT_CODE, DEFAULT_DEPENDENCIES

# Sync show_code with query params
query_params = st.experimental_get_query_params()
should_show_code = query_params.get("code", ["1"])[0] == "1"


def update_code_query_param():
    query_params = st.experimental_get_query_params()
    show_code = st.session_state["show_code"]
    query_params["code"] = ["1" if show_code else "0"]
    st.experimental_set_query_params(**query_params)


show_code = st.toggle(
    "Show editor", value=True, on_change=update_code_query_param, key="show_code"
)

_ = """
if show_code:
    col1, col2 = st.columns(2)
else:
    col2 = st.empty()
    col1 = col2

with st.expander("Add requirements"):
    # requirements = st.text_area("Requirements", value=requirements, height=100)
    requirements = st_tags(requirements, label="")

if show_code:
    with col1:
        with st.container(border=True):
            code = st_monaco(value=code, language="python", height=f"{HEIGHT}px")

with col2:
    with st.container(border=True):
        import_statement = "import streamlit as st"
        if code and import_statement not in code:
            code = f"{import_statement}\n\n" + code
        try:
            val = stlite_sandbox(
                code=code,
                height=HEIGHT + 15,
                requirements=requirements,
                scrollable=True,
            )
        except Exception as e:
            st.error(e)
"""

code, requirements = stlite_sandbox(
    code=code,
    height=HEIGHT + 15,
    requirements=requirements,
    scrollable=True,
    editor=show_code,
    requirements_picker=True,
)


get_short_url_button(
    code=code, requirements="\n".join(requirements), show_custom_hash=False
)
