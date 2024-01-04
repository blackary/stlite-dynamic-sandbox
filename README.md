# stlite-sandbox

Streamlit component that allows you to create an stlite sandbox inside your streamlit app,
and change the code without requiring the whole component to be reloaded. Comes with
an (optional) built-in editor using `streamlit-monaco` so you can quickly play with your
code and see what happens.

## Installation instructions

```sh
pip install stlite-sandbox
```

## Usage instructions

```python
import streamlit as st

from stlite_sandbox import stlite_sandbox

code = """import streamlit as st

st.write("Hello, world!")
"""

stlite_sandbox(code, height=500, editor=True)
```