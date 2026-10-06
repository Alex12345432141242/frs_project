"""One-off helper: search Wikimedia Commons and download Peterhof photos."""

from __future__ import annotations

import json
import time
from pathlib import Path

import requests

API_URL = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = (
    "PeterhofGuideBot/1.0 (educational Telegram guidebook; "
    "https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia)"
)
ASSETS_DIR = Path(__file__).resolve().parent / "assets" / "peterhof"
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": USER_AGENT})

SEARCHES = {
    "map": {
        "object": "Lower Park map / plan",
        "queries": [
            "Peterhof Lower Gardens plan",
            "Петергоф Нижний парк план",
            "Peterhof park map",
        ],
        "keywords": ["plan", "map", "план", "схема", "lower", "park", "нижн"],
        "files": ["map.jpg"],
    },
    "palace": {
        "object": "Grand Peterhof Palace",
        "queries": [
            "Peterhof Grand Palace facade",
            "Большой Петергофский дворец",
        ],
        "keywords": ["palace", "дворец", "peterhof", "петергоф"],
        "exclude": ["cascade", "каскад", "samson", "самсон", "monplaisir", "марли", "marly"],
        "files": ["palace_1.jpg", "palace_2.jpg", "palace_3.jpg"],
    },
    "cascade": {
        "object": "Grand Cascade",
        "queries": [
            "Peterhof Grand Cascade",
            "Петергоф Большой каскад",
        ],
        "keywords": ["cascade", "каскад", "grand cascade"],
        "exclude": ["chess", "шахмат", "golden hill", "золотая гора"],
        "files": ["cascade_1.jpg", "cascade_2.jpg", "cascade_3.jpg"],
    },
    "samson": {
        "object": "Samson Fountain",
        "queries": [
            "Peterhof Samson fountain",
            "Петергоф фонтан Самсон",
        ],
        "keywords": ["samson", "самсон"],
        "files": ["samson_1.jpg", "samson_2.jpg", "samson_3.jpg"],
    },
    "adam": {
        "object": "Adam Fountain",
        "queries": [
            "Peterhof fountain Adam",
            "Петергоф фонтан Адам",
        ],
        "keywords": ["adam", "адам"],
        "exclude": ["eve", "ева", "and eve"],
        "files": ["adam_1.jpg", "adam_2.jpg"],
    },
    "eve": {
        "object": "Eve Fountain",
        "queries": [
            "Peterhof fountain Eve",
            "Петергоф фонтан Ева",
        ],
        "keywords": ["eve", "ева"],
        "exclude": ["adam", "адам"],
        "files": ["eve_1.jpg", "eve_2.jpg"],
    },
    "monplaisir": {
        "object": "Monplaisir Palace",
        "queries": [
            "Peterhof Monplaisir Palace",
            "Петергоф дворец Монплезир",
        ],
        "keywords": ["monplaisir", "монплезир"],
        "files": ["monplaisir_1.jpg", "monplaisir_2.jpg", "monplaisir_3.jpg"],
    },
    "marli": {
        "object": "Marly Palace",
        "queries": [
            "Peterhof Marly Palace",
            "Петергоф дворец Марли",
        ],
        "keywords": ["marly", "марли"],
        "exclude": ["cascade", "каскад", "golden"],
        "files": ["marli_1.jpg", "marli_2.jpg"],
    },
    "voronikhin": {
        "object": "Voronikhin Colonnades",
        "queries": [
            "Peterhof Voronikhin Colonnades",
            "Петергоф Воронихинские колоннады",
        ],
        "keywords": ["voronikhin", "воронихин", "colonnade", "колоннад"],
        "files": ["voronikhin_1.jpg", "voronikhin_2.jpg"],
    },
    "chess": {
        "object": "Chessboard Hill / Dragon Cascade",
        "queries": [
            "Peterhof Chessboard Hill cascade",
            "Петергоф Шахматная гора",
            "Peterhof Dragon cascade",
        ],
        "keywords": ["chess", "шахмат", "dragon", "дракон"],
        "files": ["chess_1.jpg", "chess_2.jpg"],
    },
    "gold": {
        "object": "Golden Hill Cascade",
        "queries": [
            "Peterhof Golden Hill cascade",
            "Петергоф Золотая гора каскад",
        ],
        "keywords": ["golden hill", "золотая гора", "gold mountain"],
        "files": ["gold_1.jpg", "gold_2.jpg"],
    },
    "roman": {
        "object": "Roman Fountains",
        "queries": [
            "Peterhof Roman Fountains",
            "Петергоф Римские фонтаны",
        ],
        "keywords": ["roman", "римск"],
        "files": ["roman_1.jpg", "roman_2.jpg"],
    },
    "gulf": {
        "object": "Gulf of Finland / Sea Channel at Peterhof",
        "queries": [
            "Peterhof Sea Channel Gulf of Finland",
            "Петергоф Финский залив",
            "Петергоф Морской канал",
        ],
        "keywords": ["gulf", "залив", "sea channel", "морской канал", "gulf of finland"],
        "files": ["gulf_1.jpg", "gulf_2.jpg"],
    },
}


def search_files(query: str, limit: int = 20) -> list[dict]:
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap {query}",
        "gsrnamespace": 6,
        "gsrlimit": limit,
        "prop": "imageinfo",
        "iiprop": "url|extmetadata|mime|size|user",
        "iiurlwidth": 1600,
    }
    response = SESSION.get(API_URL, params=params, timeout=30)
    response.raise_for_status()
    pages = response.json().get("query", {}).get("pages", {})
    results = []
    for page in pages.values():
        info_list = page.get("imageinfo") or []
        if not info_list:
            continue
        info = info_list[0]
        results.append(
            {
                "title": page.get("title", ""),
                "pageid": page.get("pageid"),
                "mime": info.get("mime", ""),
                "size": info.get("size", 0),
                "url": info.get("url"),
                "thumburl": info.get("thumburl"),
                "descriptionurl": info.get("descriptionurl"),
                "user": info.get("user"),
                "extmetadata": info.get("extmetadata") or {},
            }
        )
    return results


def meta_value(extmetadata: dict, key: str) -> str:
    value = (extmetadata.get(key) or {}).get("value") or ""
    return str(value)


def matches(item: dict, spec: dict) -> bool:
    blob = " ".join(
        [
            item["title"],
            meta_value(item["extmetadata"], "ObjectName"),
            meta_value(item["extmetadata"], "ImageDescription"),
            meta_value(item["extmetadata"], "Categories"),
        ]
    ).lower()
    if "peterhof" not in blob and "петергоф" not in blob and "petergof" not in blob:
        return False
    keywords = spec.get("keywords") or []
    if keywords and not any(word.lower() in blob for word in keywords):
        return False
    for word in spec.get("exclude") or []:
        if word.lower() in blob:
            return False
    return True


def pick_download_url(item: dict) -> str | None:
    if item.get("mime") != "image/jpeg":
        return None
    return item.get("thumburl") or item.get("url")


def download(url: str, dest: Path) -> None:
    response = SESSION.get(url, timeout=60)
    response.raise_for_status()
    dest.write_bytes(response.content)


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    sources = []
    missing = []
    for key, spec in SEARCHES.items():
        chosen = []
        seen_titles = set()
        for query in spec["queries"]:
            try:
                found = search_files(query)
            except requests.RequestException as exc:
                print(f"SEARCH FAIL {key} {query}: {exc}")
                continue
            time.sleep(0.4)
            for item in found:
                title = item["title"]
                if title in seen_titles:
                    continue
                seen_titles.add(title)
                if not matches(item, spec):
                    continue
                url = pick_download_url(item)
                if not url:
                    continue
                chosen.append(item | {"download_url": url})
                if len(chosen) >= len(spec["files"]):
                    break
            if len(chosen) >= len(spec["files"]):
                break

        print(f"\n=== {key}: {len(chosen)} candidates ===")
        for item in chosen:
            print(" -", item["title"], item.get("mime"), item.get("descriptionurl"))

        for filename, item in zip(spec["files"], chosen):
            dest = ASSETS_DIR / filename
            try:
                download(item["download_url"], dest)
            except requests.RequestException as exc:
                print(f"DOWNLOAD FAIL {filename}: {exc}")
                missing.append(filename)
                continue
            license_name = meta_value(item["extmetadata"], "LicenseShortName") or meta_value(
                item["extmetadata"], "UsageTerms"
            )
            artist = meta_value(item["extmetadata"], "Artist")
            sources.append(
                {
                    "file": filename,
                    "object": spec["object"],
                    "commons_title": item["title"],
                    "source": item.get("descriptionurl"),
                    "author": artist or item.get("user") or "Unknown",
                    "license": license_name or "See source page",
                    "download_url": item["download_url"],
                }
            )
            print("saved", filename, dest.stat().st_size)

        for filename in spec["files"][len(chosen) :]:
            missing.append(filename)
            print("MISSING", filename)

    (ASSETS_DIR / "_download_manifest.json").write_text(
        json.dumps({"sources": sources, "missing": missing}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("\nDONE saved", len(sources), "missing", missing)


if __name__ == "__main__":
    main()
