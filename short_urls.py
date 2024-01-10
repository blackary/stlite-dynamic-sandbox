from __future__ import annotations

import hashlib
from textwrap import dedent
from urllib import parse

import streamlit as st

from db import insert_row, select_where

TABLE = "url_table"
DEFAULT_HASH_LENGTH = 6
BASE_URL = st.secrets.get("BASE_URL", "https://stlite.streamlit.app")


def get_hash(data: str, length: int = DEFAULT_HASH_LENGTH) -> str:
    """
    Given a string representation of data, return a length-characters-long string hash
    """
    return hashlib.md5(data.encode()).hexdigest()[:length]


def get_hash_from_python(code: str, requirements: str) -> str:
    return get_hash(code + requirements)


def get_python_from_hash(hash: str) -> tuple[str, str]:
    row = select_where(TABLE, ["python", "requirements"], "hash", hash, limit=1)
    return row[0]["python"], row[0]["requirements"] or ""


def is_hash_in_table(hash: str) -> bool:
    row = select_where(TABLE, "hash", "hash", hash, limit=1)
    return len(row) > 0


def save_hash_if_not_exists(hash: str, code: str, requirements: str) -> str:
    if not is_hash_in_table(hash):
        insert_row({"hash": hash, "python": code, "requirements": requirements}, TABLE)
    return hash


def get_short_url_from_hash(hash: str) -> str:
    return BASE_URL + "/?" + parse.urlencode({"q": hash})


def get_embed_code_from_hash(hash: str):
    return dedent(
        f"""
    <iframe
        width="100%"
        height="500px"
        frameBorder="0"
        src="{BASE_URL}/~/+/?embed=true&q={hash}">
    </iframe>
    """
    )


def get_short_url_button(code: str, requirements: str, show_custom_hash: bool = True):
    custom_hash = None
    if show_custom_hash:
        custom_hash = st.text_input("Custom Hash").strip()
    if st.button("Get shareable url"):
        if custom_hash:
            hash = custom_hash
        else:
            hash = get_hash_from_python(code=code, requirements=requirements)
        save_hash_if_not_exists(hash, code, requirements)
        url = get_short_url_from_hash(hash)
        embed_code = get_embed_code_from_hash(hash)
        st.write(f"[{url}]({url})")
        # st.write("Embed code")
        st.code(url, language="html")
        st.code(embed_code, language="html")


def expand_short_url() -> tuple[str, str] | None:
    query_params = st.experimental_get_query_params()
    if "q" in query_params:
        short_hash = query_params["q"][0]
        try:
            return get_python_from_hash(short_hash)
        except IndexError:
            st.error(f"Invalid short url: {short_hash}")
    return None
