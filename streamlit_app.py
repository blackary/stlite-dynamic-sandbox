import streamlit as st
from streamlit_monaco import st_monaco
from stlite_sandbox import stlite_sandbox
from short_urls import get_short_url_button, expand_short_url

st.set_page_config(
    page_title="Streamlit Sandbox", page_icon=":sunglasses:", layout="wide"
)

HEIGHT = 500
DEFAULT_CODE = """import streamlit as st
import pandas as pd

st.title("Hello world!")

df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
df_edited = st.data_editor(df)

st.line_chart(df_edited)
"""

DEFAULT_DEPENDENCIES = "streamlit-extras\n"

resp = expand_short_url()
if resp is not None:
    code, requirements = resp
else:
    code, requirements = DEFAULT_CODE, DEFAULT_DEPENDENCIES

col1, col2 = st.columns(2)


with col1:
    with st.expander("Add requirements"):
        requirements = st.text_area("Requirements", value=requirements, height=100)
    code = st_monaco(value=code, language="python", height=f"{HEIGHT}px")

with col2:
    try:
        import_statement = "import streamlit as st"
        if import_statement not in code:
            code = f"{import_statement}\n\n" + code
        reqs = [r for r in requirements.split("\n") if r]
        stlite_sandbox(code=code, height=HEIGHT, requirements=reqs)
    except Exception as e:
        st.error(e)

get_short_url_button(code=code, requirements=requirements, show_custom_hash=False)
