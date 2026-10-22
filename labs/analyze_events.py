"""Безопасный учебный анализ локального CSV; сеть не используется."""
import csv
from collections import Counter
from pathlib import Path

def count_failures(rows):
    return Counter(row["source"] for row in rows
                   if row.get("action") == "login" and row.get("result") == "fail")

if __name__ == "__main__":
    path = Path(__file__).with_name("events.csv")
    try:
        with path.open(encoding="utf-8", newline="") as file:
            counts = count_failures(csv.DictReader(file))
        for source, count in sorted(counts.items()):
            print(f"{source}: {count} failed logins")
        print("This count does NOT implement a time window or prove compromise.")
    except FileNotFoundError:
        raise SystemExit("Put events.csv next to this script.")
