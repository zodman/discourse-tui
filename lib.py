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


def get_post_formated(p, categories, headers):
    return textwrap.dedent(f"""\
        [bold]{p["topic_title"]}[/bold]
        {get_category_format(p["category_id"], categories, headers)}
        [green]/u/{p["username"]}[/green] [orange]/t/{p['topic_slug']}[/orange]
        """)


def show_category(id, headers):
    resp = requests.get(f"{BASE_URL}/c/{id}/show.json", headers=headers)
    resp.raise_for_status()
    return resp.json()["category"]


def list_categories(headers):
    resp = requests.get(
        f"{BASE_URL}/categories.json",
        params={"include_subcategories": True},
        headers=headers,
    )
    resp.raise_for_status()
    data = resp.json()["category_list"]["categories"]
    return data


def get_category_format(id, categories, headers):
    ids = list(map(lambda x: x["id"], categories))
    category = None
    if id in ids:
        idx = ids.index(id)
        category = categories[idx]
    else:
        category = show_category(id, headers)
    return f"[#{category['color']}]{category['name']}[/#{category['color']}]"
