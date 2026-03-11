import argparse
import csv
from collections import defaultdict
from pathlib import Path


def read_students(csv_path: Path):
    records = []
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("name") or "").strip()
            grade_raw = (row.get("grade") or "").strip()
            subject = (row.get("subject") or "").strip()

            if not name or not grade_raw:
                continue

            try:
                grade = float(grade_raw)
            except ValueError:
                continue

            records.append({"name": name, "grade": grade, "subject": subject})
    return records


def build_report(records):
    sum_by_student = defaultdict(float)
    count_by_student = defaultdict(int)
    subject_counts = defaultdict(int)

    for r in records:
        name = r["name"]
        grade = r["grade"]
        subject = r["subject"]

        sum_by_student[name] += grade
        count_by_student[name] += 1
        if subject:
            subject_counts[subject] += 1

    averages = {
        name: sum_by_student[name] / count_by_student[name]
        for name in sum_by_student
    }

    highest_name = max(averages, key=averages.get) if averages else None
    lowest_name = min(averages, key=averages.get) if averages else None

    return {
        "averages": averages,
        "highest": (highest_name, averages[highest_name]) if highest_name else None,
        "lowest": (lowest_name, averages[lowest_name]) if lowest_name else None,
        "subject_counts": subject_counts,
        "total_records": len(records),
    }


def print_report(report, csv_path: Path):
    print("Student Report")
    print(f"File: {csv_path}")
    print(f"Total records: {report['total_records']}")
    print()

    print("Average grade per student:")
    for name in sorted(report["averages"]):
        print(f"{name:<10} {report['averages'][name]:.2f}")
    print()

    if report["highest"]:
        name, avg = report["highest"]
        print(f"Highest average: {name} ({avg:.2f})")
    if report["lowest"]:
        name, avg = report["lowest"]
        print(f"Lowest average: {name} ({avg:.2f})")
    print()

    print("Students per subject:")
    for subject in sorted(report["subject_counts"]):
        print(f"{subject:<10} {report['subject_counts'][subject]}")


def resolve_csv_path(path_str: str) -> Path:
    path = Path(path_str)
    if path.exists():
        return path
    script_dir = Path(__file__).resolve().parent
    alt = script_dir / path_str
    return alt


def main():
    parser = argparse.ArgumentParser(description="Student report from CSV.")
    parser.add_argument(
        "--file",
        default="students.csv",
        help="Path to CSV file with name,grade,subject headers.",
    )
    args = parser.parse_args()

    csv_path = resolve_csv_path(args.file)
    if not csv_path.exists():
        raise SystemExit(f"CSV file not found: {csv_path}")

    records = read_students(csv_path)
    report = build_report(records)
    print_report(report, csv_path)


if __name__ == "__main__":
    main()
