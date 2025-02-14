import requests
from enums import BASE_URL
import lib


def latest_post(headers):
    resp = requests.get(f"{BASE_URL}/posts.json", headers=headers)
    resp.raise_for_status()
    return resp.json().get("latest_posts")


def main():
    headers = lib.get_headers()
    categories = lib.list_categories(headers)
    posts = latest_post(headers)
    for p in posts:
        lib.print(p, categories)


if __name__ == "__main__":
    main()
