"""Search Unsplash and download chosen photos with credit (API guidelines: hotlink-free download, trigger
download_location, credit the photographer). The key is read from UNSPLASH_ACCESS_KEY and never printed.

python3 tools/unsplash_fetch.py search "wildflower meadow" [n]     -> prints id, size, photographer, thumb saved to scratch
python3 tools/unsplash_fetch.py get <id> <out.jpg>                  -> downloads, triggers download_location, appends CREDITS.md
"""
import os, sys, json, urllib.request, urllib.parse
from pathlib import Path

API = "https://api.unsplash.com"


def call(url):
    req = urllib.request.Request(url, headers={"Authorization": "Client-ID " + os.environ["UNSPLASH_ACCESS_KEY"],
                                               "Accept-Version": "v1"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 401: sys.exit("Unsplash returned 401: stopping.")
        raise


def fetch(url, out):
    with urllib.request.urlopen(url, timeout=120) as r: Path(out).write_bytes(r.read())


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "search":
        q, n = sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 6
        res = call(f"{API}/search/photos?" + urllib.parse.urlencode({"query": q, "per_page": n, "content_filter": "high"}))
        tmp = Path(os.environ.get("SCRATCH", "/tmp")); tmp.mkdir(parents=True, exist_ok=True)
        for p in res["results"]:
            fetch(p["urls"]["thumb"], tmp / f"us-{p['id']}.jpg")
            print(p["id"], p["width"], p["height"], p["user"]["name"], "|", (p.get("alt_description") or "")[:70])
    elif cmd == "get":
        pid, out = sys.argv[2], sys.argv[3]
        p = call(f"{API}/photos/{pid}")
        call(p["links"]["download_location"])          # required by the API guidelines
        fetch(p["urls"]["raw"] + "&w=2000&q=85&fm=jpg", out)
        credit = Path(out).parent / "CREDITS.md"
        line = (f"- `{Path(out).name}`: photo by {p['user']['name']} on Unsplash, "
                f"{p['links']['html']}?utm_source=sfw&utm_medium=referral\n")
        if not credit.exists(): credit.write_text("# Photo credits (Unsplash)\n\n")
        if Path(out).name not in credit.read_text(): credit.open("a").write(line)
        print("saved", out, "by", p["user"]["name"])
