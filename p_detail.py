import lib
import json
import requests
import enums
import sys


def detail(id, headers):
    resp = requests.get(f"{enums.BASE_URL}/t/{id}.json", headers=headers)
    resp.raise_for_status()
    return resp.json()


def main():
    id = sys.argv[1]
    headers = lib.get_headers()
    posts = detail(id, headers)
    print(json.dumps(posts))


if __name__ == "__main__":
    main()
