import subprocess
import tempfile
import os
import time
from fastapi import HTTPException

# ── Hardcoded problems (replaced by DB in Phase 7b) ─────────────────────────

PROBLEMS = {
    1: {
        "title": "Two Sum",
        "function": "twoSum",
        "test_cases": [
            {"input": "[2,7,11,15], 9",  "expected": "[0, 1]"},
            {"input": "[3,2,4], 6",       "expected": "[1, 2]"},
            {"input": "[3,3], 6",         "expected": "[0, 1]"},
        ],
    },
}

# ── Safety blocklist ─────────────────────────────────────────────────────────

BLOCKED = [
    "import os", "import sys", "import subprocess", "import shutil",
    "import socket", "import threading", "import multiprocessing",
    "__import__", "open(", "exec(", "eval(", "compile(", "globals()",
    "locals()", "getattr(", "setattr(", "delattr(",
]


def _check_safety(code: str):
    for token in BLOCKED:
        if token in code:
            raise HTTPException(
                status_code=400,
                detail=f"Unsafe code detected: '{token}' is not allowed."
            )


# ── Runner ───────────────────────────────────────────────────────────────────

def run_python_code(code: str, problem_id: int) -> dict:
    """
    Wraps the user's function in a test harness, executes it in a subprocess,
    and returns per-test-case results.
    """
    _check_safety(code)

    problem = PROBLEMS.get(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail=f"Problem {problem_id} not found.")

    fn_name   = problem["function"]
    test_cases = problem["test_cases"]

    results      = []
    total_time   = 0
    combined_out = []

    for tc in test_cases:
        # Build a self-contained script per test case
        script = f"""{code}

import json
result = {fn_name}({tc['input']})
print(json.dumps(result))
"""
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        )
        tmp.write(script)
        tmp.close()

        try:
            t0 = time.perf_counter()
            proc = subprocess.run(
                ["python", tmp.name],
                capture_output=True,
                text=True,
                timeout=5,
            )
            elapsed_ms = int((time.perf_counter() - t0) * 1000)
            total_time += elapsed_ms

            if proc.returncode != 0:
                actual = f"Error: {proc.stderr.strip()}"
                passed = False
            else:
                actual = proc.stdout.strip()
                # Normalize: parse both as JSON for comparison
                try:
                    import json
                    passed = json.loads(actual) == json.loads(tc["expected"])
                except Exception:
                    passed = actual == tc["expected"]

        except subprocess.TimeoutExpired:
            actual = "Error: Time limit exceeded (5s)"
            passed = False
            elapsed_ms = 5000
            total_time += elapsed_ms
        finally:
            os.unlink(tmp.name)

        combined_out.append(actual)
        results.append({
            "input":    tc["input"],
            "expected": tc["expected"],
            "actual":   actual,
            "passed":   passed,
        })

    passed_count = sum(1 for r in results if r["passed"])
    summary_out  = "\n".join(combined_out) if combined_out else ""

    return {
        "output":       summary_out,
        "runtime_ms":   total_time,
        "passed_cases": results,
        "total":        len(results),
        "passed":       passed_count,
    }
