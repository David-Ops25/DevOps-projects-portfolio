from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class Args:
    input_path: Path
    output_dir: Path
    version: str


def parse_args(argv: list[str] | None = None) -> Args:
    p = argparse.ArgumentParser(prog="release-notes", description="Generate release notes from a spreadsheet.")
    p.add_argument("--input", required=True, help="Path to input .xlsx/.csv with changelog rows.")
    p.add_argument("--output-dir", default="out", help="Directory to write outputs into.")
    p.add_argument("--version", default="Unreleased", help="Release version header, e.g. 1.2.0")
    ns = p.parse_args(argv)
    return Args(input_path=Path(ns.input), output_dir=Path(ns.output_dir), version=str(ns.version))


def load_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise SystemExit("Input must be .csv or .xlsx/.xls")


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    if "description" not in df.columns:
        raise SystemExit("Missing required column: description")

    for col in ["type", "ticket", "owner"]:
        if col not in df.columns:
            df[col] = ""

    df["type"] = df["type"].fillna("").astype(str).str.strip().str.title()
    df["description"] = df["description"].fillna("").astype(str).str.strip()
    df["ticket"] = df["ticket"].fillna("").astype(str).str.strip()
    df["owner"] = df["owner"].fillna("").astype(str).str.strip()

    df = df[df["description"].str.len() > 0]

    allowed = {"Added", "Changed", "Fixed", "Removed", ""}
    df.loc[~df["type"].isin(allowed), "type"] = "Changed"

    return df[["type", "description", "ticket", "owner"]]


def to_markdown(df: pd.DataFrame, version: str) -> str:
    sections = ["Added", "Changed", "Fixed", "Removed"]
    lines: list[str] = [f"# Release Notes — {version}", ""]
    for sec in sections:
        rows = df[df["type"] == sec]
        if rows.empty:
            continue
        lines.append(f"## {sec}")
        for _, r in rows.iterrows():
            ticket = f" ({r['ticket']})" if r["ticket"] else ""
            owner = f" — {r['owner']}" if r["owner"] else ""
            lines.append(f"- {r['description']}{ticket}{owner}")
        lines.append("")
    if len(lines) == 2:
        lines.append("_No items found._")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    raw = load_table(args.input_path)
    clean = normalize(raw)

    md = to_markdown(clean, args.version)
    (args.output_dir / "release_notes.md").write_text(md, encoding="utf-8")

    summary = {
        "version": args.version,
        "counts": clean["type"].value_counts(dropna=False).to_dict(),
        "total_items": int(len(clean)),
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"Wrote: {args.output_dir / 'release_notes.md'}")
    print(f"Wrote: {args.output_dir / 'summary.json'}")


if __name__ == "__main__":
    main()
