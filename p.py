import lib
import json
import requests
import enums


def latest_post(headers):
    resp = requests.get(f"{enums.BASE_URL}/posts.json", headers=headers)
    resp.raise_for_status()
    return resp.json().get("latest_posts")


def main():
    headers = lib.get_headers()
    posts = latest_post(headers)
    print(json.dumps(posts))


if __name__ == "__main__":
    main()
