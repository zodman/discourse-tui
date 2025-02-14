import json
import rich
import textwrap
from enums import BASE_URL

import requests


def get_token():
    with open("secret.json") as f:
        token = json.loads(f.read())
    return token.get("key")


def get_headers():
    token = get_token()
    return {"User-Api-Key": token}


def print(p, categories):
    rich.print(
        textwrap.dedent(f"""
        [bold]{p["topic_title"]}[/bold]
        [green]{get_category_name(p["category_id"], categories)}[/green]
        {BASE_URL}/t/{p['topic_slug']}
        {p["name"]}""")
    )


def list_categories(headers):
    resp = requests.get(f"{BASE_URL}/categories.json", headers=headers)
    resp.raise_for_status()
    data = resp.json()["category_list"]["categories"]
    return data


def get_category_name(id, categories):
    ids = list(map(lambda x: x["id"], categories))
    try:
        idx = ids.index(id)
    except ValueError:
        return ""
    return categories[idx]["name"]
