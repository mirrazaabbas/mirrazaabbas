import csv
import statistics
import sys
from collections import defaultdict


def load_rows(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def to_float(value: str) -> float:
    return float(value.replace(",", "").strip())


def analyze_sales(rows: list[dict]) -> None:
    revenues = [to_float(row["revenue"]) for row in rows]
    by_region = defaultdict(float)
    by_product = defaultdict(float)

    for row in rows:
        revenue = to_float(row["revenue"])
        by_region[row["region"]] += revenue
        by_product[row["product"]] += revenue

    top_region = max(by_region.items(), key=lambda item: item[1])
    top_product = max(by_product.items(), key=lambda item: item[1])

    print("\nCSV Insight Analyzer")
    print("--------------------")
    print(f"Rows analyzed: {len(rows)}")
    print(f"Total revenue: ${sum(revenues):,.2f}")
    print(f"Average revenue per row: ${statistics.mean(revenues):,.2f}")
    print(f"Median revenue per row: ${statistics.median(revenues):,.2f}")
    print(f"Top region: {top_region[0]} (${top_region[1]:,.2f})")
    print(f"Top product: {top_product[0]} (${top_product[1]:,.2f})")

    print("\nRevenue by region:")
    for region, revenue in sorted(by_region.items(), key=lambda x: x[1], reverse=True):
        print(f"- {region}: ${revenue:,.2f}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyzer.py <sales.csv>")
        raise SystemExit(1)

    rows = load_rows(sys.argv[1])
    if not rows:
        print("The CSV file contains no data rows.")
        raise SystemExit(1)

    analyze_sales(rows)
