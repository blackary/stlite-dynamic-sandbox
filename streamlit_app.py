import streamlit as st
from streamlit_monaco import st_monaco
from stlite_sandbox import stlite_sandbox
from short_urls import get_short_url_button, expand_short_url

st.set_page_config(
    page_title="Streamlit Sandbox", page_icon=":sunglasses:", layout="wide"
)

code_from_url = expand_short_url()

col1, col2 = st.columns(2)

DEFAULT_CODE = """import streamlit as st

st.write("Hello world!")"""
HEIGHT = 500

code = DEFAULT_CODE if not code_from_url else code_from_url

with col1:
    code = st_monaco(value=code, language="python", height=f"{HEIGHT}px")

with col2:
    try:
        import_statement = "import streamlit as st"
        if import_statement not in code:
            code = f"{import_statement}\n\n" + code
        stlite_sandbox(code=code, height=HEIGHT, requirements=["streamlit-extras"])
    except Exception as e:
        st.error(e)

get_short_url_button(code=code, show_custom_hash=False)
