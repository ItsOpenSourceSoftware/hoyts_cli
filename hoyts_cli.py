import requests
import sys
import textwrap

API = "https://apim.hoyts.com.au/au/cinemaapi/api/movies"


# ---------------- FETCH ----------------

def fetch_movies():
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; HOYTS CLI)"
    }

    try:
        r = requests.get(API, headers=headers, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("❌ Failed to fetch movies:", e)
        return []


# ---------------- FILTERS ----------------

def filter_by_name(movies, query):
    return [
        m for m in movies
        if query.lower() in m.get("name", "").lower()
    ]


def filter_by_type(movies, mtype):
    return [
        m for m in movies
        if m.get("type", "").lower() == mtype.lower()
    ]


def filter_by_rating(movies, rating):
    return [
        m for m in movies
        if m.get("rating", {}).get("id", "").lower() == rating.lower()
    ]


def filter_by_synopsis(movies, query):
    return [
        m for m in movies
        if query.lower() in m.get("summary", "").lower()
    ]


# ---------------- DISPLAY ----------------

def show(movies):
    if not movies:
        print("\n⚠️ No results found\n")
        return

    print("\n🎬 HOYTS RESULTS")
    print("=" * 60)

    for m in movies:
        name = m.get("name", "Unknown")
        mtype = m.get("type", "unknown")
        rating = m.get("rating", {}).get("id", "N/A")
        genres = ", ".join(m.get("genres", [])) or "None"
        summary = m.get("summary", "")

        print(f"\n🎞 {name}")
        print(f"📌 Type: {mtype}")
        print(f"⭐ Rating: {rating}")
        print(f"🎭 Genres: {genres}")
        print("📖 Synopsis:")

        # FULL WRAPPED SYNOPSIS (no cutoff)
        print(textwrap.fill(summary, width=80))

        print("-" * 60)


# ---------------- HELP ----------------

def help_menu():
    print("""
🎬 HOYTS CLI

Usage:
  python hoyts_cli.py name <text>
  python hoyts_cli.py type <nowShowing|comingSoon|advanceSale>
  python hoyts_cli.py rating <PG|M|MA|CTC>
  python hoyts_cli.py synopsis <text>

Examples:
  python hoyts_cli.py name avengers
  python hoyts_cli.py type comingSoon
  python hoyts_cli.py type nowShowing
  python hoyts_cli.py rating M
  python hoyts_cli.py synopsis robot
""")


# ---------------- MAIN ----------------

def main():
    movies = fetch_movies()

    if not movies:
        return

    args = sys.argv[1:]

    if not args:
        help_menu()
        return

    command = args[0]
    query = " ".join(args[1:]) if len(args) > 1 else ""

    if command == "name":
        result = filter_by_name(movies, query)

    elif command == "type":
        result = filter_by_type(movies, query)

    elif command == "rating":
        result = filter_by_rating(movies, query)

    elif command == "synopsis":
        result = filter_by_synopsis(movies, query)

    else:
        print("❌ Unknown command")
        help_menu()
        return

    show(result)


if __name__ == "__main__":
    main()
