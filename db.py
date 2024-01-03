from typing import Any

import streamlit as st
from supabase.client import Client, create_client

key: str = st.secrets["SUPABASE_KEY"]
url: str = st.secrets["SUPABASE_URL"]
client: Client = create_client(url, key)


def get_all_data(table: str) -> list[dict]:
    resp = client.table(table).select("*").execute()
    return resp.model_dump()["data"]


def select_where(
    table: str,
    columns_to_select: str,
    column_to_check: str,
    column_equals: str,
) -> list[dict]:
    """
    Given a comma-separated list of columns, a column to check, and a value to check
    for it to be equal to, return all the matches rows, if any.
    """
    return (
        client.table(table)
        .select(columns_to_select)
        .eq(column_to_check, column_equals)
        .execute()
        .dict()
        .get("data", [])
    )


def insert_row(data: dict, table: str) -> Any:
    return client.table(table).insert(data).execute()
