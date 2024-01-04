from __future__ import annotations

from typing import Sequence

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
from streamlit_monaco import st_monaco
from streamlit_tags import st_tags


# Tell streamlit that there is a component called stlite_sandbox,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component("stlite_sandbox", path=str(frontend_dir))


# Create the python function that will be called
def stlite_sandbox(
    code: str,
    requirements: list[str] | None = None,
    key: str = "stlite_sandbox",
    height: int = 500,
    scrollable: bool = False,
    editor: bool = False,
    border: bool = True,
    requirements_picker: bool = False,
    layout: int | Sequence[int] | None = None,
) -> tuple[str, list[str]]:
    """
    Add a descriptive docstring
    """
    if requirements is None:
        requirements = []

    if layout is None:
        layout = [1, 1]

    if editor:
        col1, col2 = st.columns(layout)

        with col1:
            with st.container(border=border):
                code = st_monaco(value=code, language="python", height=f"{height}px")

        with col2:
            with st.container(border=border):
                _stlite_sandbox(
                    code=code,
                    requirements=requirements,
                    key=key,
                    height=height + 15,
                    scrollable=scrollable,
                )
    else:
        with st.container(border=border):
            _stlite_sandbox(
                code=code,
                requirements=requirements,
                key=key,
                height=height + 15,
                scrollable=scrollable,
            )

    if requirements_picker:
        requirements = st_tags(requirements, label="Requirements")

    return code, requirements


def _stlite_sandbox(
    code: str,
    requirements: list[str] | None = None,
    key: str = "stlite_sandbox",
    height: int = 500,
    scrollable: bool = False,
):
    if requirements is None:
        requirements = []

    _component_func(
        key=key,
        code=code,
        requirements=requirements,
        height=height,
        scrollable=scrollable,
    )


def main():
    st.write("## Example")
    default_code = """
import streamlit as st

st.write("Hello world!")"""
    code = st.text_area("Code", value=default_code, height=200, key="code")
    stlite_sandbox(code=code, key="blah", height=500)


if __name__ == "__main__":
    main()
