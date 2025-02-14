from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random
import urllib.parse
import subprocess
from rich.prompt import Prompt
import rich
from base64 import b64decode, b64encode
from .enums import BASE_URL


def gen_keys():
    key = RSA.generate(2048)
    private_key = key.export_key("PEM")
    public_key = key.publickey().export_key("PEM").decode("utf-8")
    return (private_key, public_key)


def main():
    priv, pub = gen_keys()
    params = {
        # "auth_redirect": "http://localhost:8081",
        "application_name": "PolicyKit",
        "client_id": "1231231312312",  # 32 random nibbles (not bytes! despite what API doc says)
        "nonce": "abc123",  # 16 random nibbles (not bytes! despite what API doc says)
        "scopes": "read,write,message_bus,session_info",
        "public_key": pub,
    }
    query_string = urllib.parse.urlencode(params)
    subprocess.check_output(
        f"xdg-open '{BASE_URL}/user-api-key/new?{query_string}'", shell=True
    )
    cipher_rsa = PKCS1_v1_5.new(RSA.import_key(priv))
    sentinel = Random.new()
    token = Prompt.ask("TOKEN?")
    t = b64decode(token)
    payload = cipher_rsa.decrypt(t, sentinel)
    with open("secret.json", "w") as f:
        f.write(payload.decode("utf8"))


if __name__ == "__main__":
    main()
