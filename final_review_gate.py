#!/usr/bin/env python3
import sys

def main() -> int:
    print("FINAL REVIEW GATE: Ready. Type sub-prompts; type 'TASK_COMPLETE' to finish.")
    try:
        for line in sys.stdin:
            line = line.rstrip("\n")
            if line.strip() == "TASK_COMPLETE":
                print("--- REVIEW GATE: USER CONFIRMED TASK COMPLETE ---")
                return 0
            if line:
                print(f"USER_REVIEW_SUB_PROMPT: {line}")
    except KeyboardInterrupt:
        pass
    print("--- FINAL REVIEW GATE SCRIPT EXITED ---")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

