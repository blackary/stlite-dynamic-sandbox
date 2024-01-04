# stlite-sandbox

Streamlit component that allows you to create an stlite sandbox inside your streamlit app,
and change the code without requiring the whole component to be reloaded.

## Installation instructions

```sh
pip install stlite-sandbox
```

## Usage instructions

```python
import streamlit as st

from stlite_sandbox import stlite_sandbox

code1 = """import streamlit as st

st.write('Code1')
"""

code2 = """import streamlit as st

st.write('Code2')
"""

code = code2 if st.checkbox('use code 2') else code1

stlite_sandbox(code)
```