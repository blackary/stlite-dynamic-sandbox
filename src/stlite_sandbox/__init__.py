from __future__ import annotations

from pathlib import Path
from typing import Optional

# Import hashlib method for hashing string
from hashlib import md5

import streamlit as st
import streamlit.components.v1 as components

# Tell streamlit that there is a component called stlite_sandbox,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component("stlite_sandbox", path=str(frontend_dir))


# Create the python function that will be called
def stlite_sandbox(
    code: str,
    requirements: list[str] | None = None,
    key: Optional[str] = None,
):
    """
    Add a descriptive docstring
    """
    if requirements is None:
        requirements = []

    if key is None:
        key = md5(code.encode() + str(requirements).encode()).hexdigest()

    component_value = _component_func(
        key=key,
        code=code,
        requirements=requirements,
    )

    return component_value


def main():
    st.write("## Example")
    default_code = """
import streamlit as st

st.write("Hello world!")"""
    code = st.text_area("Code", value=default_code, height=200, key="code")
    stlite_sandbox(code=code, key="blah")


if __name__ == "__main__":
    main()
