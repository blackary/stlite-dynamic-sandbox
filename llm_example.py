import json
from textwrap import dedent

import streamlit as st
from openai import OpenAI
from stlite_sandbox import stlite_sandbox

from short_urls import get_short_url_button

st.set_page_config(
    page_title="App Generator",
    page_icon=":sunglasses:",
    layout="wide",
)


st.title(":robot: App Generator")

if "OPENAI_API_KEY" not in st.secrets:
    key = st.sidebar.text_input("Enter OpenAI Key", type="password")

    if not key:
        st.info("Enter your OpenAI key in the sidebar to get started")
        st.stop()

else:
    key = st.secrets["OPENAI_API_KEY"]

MODELS = ("gpt-3.5-turbo-1106", "gpt-4-1106-preview")

client = OpenAI(api_key=key)


@st.cache_data
def get_models() -> list[str]:
    return [model.id for model in client.models.list()]


models = [model for model in MODELS if model in get_models()]

model = st.selectbox("OpenAI Model", models)

app_description = st.text_input("What sort of app should I make?", key="prompt")

if not app_description:
    st.stop()


@st.cache_data
def get_response(prompt: str, model: str) -> dict:
    response = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": dedent(
                    """
                You are a helpful assistant designed to output JSON. The output should
                contain two keys 'code' and 'requirements' 'code' should be valid python
                code to create the requested streamlit app, and 'requirements' should be
                a list of strings which represent a the values that would be put in
                requirements.txt to run such an app. If possible, avoid using any
                calls to external files in the code, and hard-code values instead.
                If there are no dependencies, or if the only dependency is streamlit,
                leave 'requirements' as an empty list.
                """
                ),
            },
            {
                "role": "user",
                "content": f"Make me a streamlit app that does this: {prompt}",
            },
        ],
    )

    try:
        response = json.loads(response.choices[0].message.content)  # type: ignore
    except json.JSONDecodeError:
        st.error("Error decoding response from OpenAI")
        st.json(response.choices[0].message.content)
        st.stop()

    return response


response = get_response(app_description, model)
code = response["code"]
requirements = response["requirements"]


code, requirements = stlite_sandbox(
    code=code,
    requirements=requirements,
    height=700,
    editor=True,
    requirements_picker=True,
    theme="vs-dark",
    scrollable=True,
)

get_short_url_button(
    code=code, requirements="\n".join(requirements), show_custom_hash=False
)
