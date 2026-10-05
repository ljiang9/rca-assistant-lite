"""命令行：python3 cli.py "故障现象" """
import argparse
import sys

from rca import analyze, report


def main(argv=None):
    p = argparse.ArgumentParser(description="rca-assistant-lite 故障根因分析")
    p.add_argument("symptom", nargs="?", help="故障现象，如：服务宕机")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    symptom = args.symptom or sys.stdin.read().strip()
    if not symptom:
        print("错误：未提供故障现象", file=sys.stderr)
        return 2
    if args.json:
        import json
        print(json.dumps(analyze(symptom), ensure_ascii=False, indent=2))
    else:
        print(report(symptom))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
