# stlite-dynamic-sandbox

Streamlit component that allows you to dynamically create an stlite sandbox, but not reload the whole component when the code changes

## Installation instructions 

```sh
pip install stlite-dynamic-sandbox
```

## Usage instructions

```python
import streamlit as st

from stlite_sandbox import stlite_sandbox

value = stlite_sandbox()

st.write(value)
