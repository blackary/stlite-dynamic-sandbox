from __future__ import annotations

import hashlib
from textwrap import dedent
from urllib import parse

import streamlit as st

from db import insert_row, select_where

TABLE = "url_table"
DEFAULT_HASH_LENGTH = 6
BASE_URL = st.secrets.get("BASE_URL", "https://playground2.streamlit.app")


def get_hash(data: str, length: int = DEFAULT_HASH_LENGTH) -> str:
    """
    Given a string representation of data, return a length-characters-long string hash
    """
    return hashlib.md5(data.encode()).hexdigest()[:length]


def get_hash_from_python(code: str) -> str:
    return get_hash(code)


def get_python_from_hash(hash: str) -> str:
    row = select_where(TABLE, "python", "hash", hash)
    return row[0]["python"]


def is_hash_in_table(hash: str) -> bool:
    row = select_where(TABLE, "hash", "hash", hash)
    return len(row) > 0


def save_hash_if_not_exists(hash: str, code: str) -> str:
    if not is_hash_in_table(hash):
        insert_row({"hash": hash, "python": code}, TABLE)
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
        src="https://{BASE_URL}/~/+/?embedded=true&q={hash}">
    </iframe>
    """
    )


def get_short_url_button(code: str, show_custom_hash: bool = True):
    custom_hash = None
    if show_custom_hash:
        custom_hash = st.text_input("Custom Hash").strip()
    if st.button("Get shareable url"):
        if custom_hash:
            hash = custom_hash
        else:
            hash = get_hash_from_python(code=code)
        save_hash_if_not_exists(hash, code)
        url = get_short_url_from_hash(hash)
        embed_code = get_embed_code_from_hash(hash)
        st.write(f"[{url}]({url})")
        st.write("Embed code")
        st.code(embed_code, language="html")


def expand_short_url() -> str | None:
    query_params = st.experimental_get_query_params()
    if "q" in query_params:
        short_hash = query_params["q"][0]
        try:
            return get_python_from_hash(short_hash)
        except IndexError:
            st.error(f"Invalid short url: {short_hash}")
    return None
