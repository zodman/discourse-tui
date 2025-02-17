import lib
import json
import requests
import enums


def main():
    headers = lib.get_headers()
    resp = requests.get(
        f"{enums.BASE_URL}/categories.json",
        params={"include_subcategories": True},
        headers=headers,
    )
    resp.raise_for_status()
    data = resp.json()

    print(json.dumps(data))


if __name__ == "__main__":
    main()
