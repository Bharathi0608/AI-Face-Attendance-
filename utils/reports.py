"""
utils/reports.py
Generate CSV / summary reports from attendance data.
"""

import csv
import io
from datetime import date
from utils.helpers import format_date_display, attendance_percentage


def build_daily_csv(records: list[dict], class_name: str, day: str) -> str:
    """
    Build a CSV string for a single day's attendance.
    records: list of {name, roll_number, status, timestamp}
    Returns CSV as a string.
    """
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([f"Attendance Report — {class_name}"])
    writer.writerow([f"Date: {format_date_display(day)}"])
    writer.writerow([])
    writer.writerow(["Roll No.", "Name", "Status", "Time"])

    for r in sorted(records, key=lambda x: x.get("roll_number", "")):
        writer.writerow([
            r.get("roll_number", "—"),
            r.get("name", "—"),
            r.get("status", "—").upper(),
            r.get("timestamp", "—")
        ])

    writer.writerow([])
    present = sum(1 for r in records if r.get("status") == "present")
    writer.writerow(["", "Present", present])
    writer.writerow(["", "Absent",  len(records) - present])
    writer.writerow(["", "Total",   len(records)])
    writer.writerow(["", "Rate",    f"{attendance_percentage(present, len(records))}%"])

    return output.getvalue()


def build_summary_csv(summary: list[dict], class_name: str) -> str:
    """
    Build a summary CSV across all dates for a class.
    summary: list of {date, present, absent, total}
    """
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([f"Attendance Summary — {class_name}"])
    writer.writerow([f"Generated: {date.today().isoformat()}"])
    writer.writerow([])
    writer.writerow(["Date", "Present", "Absent", "Total", "Attendance %"])

    for row in summary:
        pct = attendance_percentage(row.get("present", 0), row.get("total", 0))
        writer.writerow([
            format_date_display(row["date"]),
            row.get("present", 0),
            row.get("absent", 0),
            row.get("total", 0),
            f"{pct}%"
        ])

    return output.getvalue()


def build_student_report_csv(student_records: list[dict],
                              student_name: str,
                              class_name: str) -> str:
    """Per-student attendance history CSV."""
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([f"Student Attendance — {student_name}"])
    writer.writerow([f"Class: {class_name}"])
    writer.writerow([])
    writer.writerow(["Date", "Status", "Time"])

    for r in sorted(student_records, key=lambda x: x.get("date", "")):
        writer.writerow([
            format_date_display(r.get("date", "—")),
            r.get("status", "—").upper(),
            r.get("timestamp", "—")
        ])

    writer.writerow([])
    present = sum(1 for r in student_records if r.get("status") == "present")
    total   = len(student_records)
    writer.writerow(["", "Total Classes", total])
    writer.writerow(["", "Attended",      present])
    writer.writerow(["", "Percentage",    f"{attendance_percentage(present, total)}%"])

    return output.getvalue()
