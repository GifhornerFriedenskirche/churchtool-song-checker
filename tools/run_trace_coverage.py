"""
Run pytest and collect coverage using the stdlib trace module.
Generates a simple coverage report for .py files in the repo root.
"""
import subprocess
import sys
import os
from trace import Trace


def run_tests():
    # Use pytest to run tests
    res = subprocess.run([sys.executable, '-m', 'pytest', '-q'], cwd=os.getcwd())
    return res.returncode == 0


def main():
    tracer = Trace(count=1, trace=0)
    # Run pytest under trace
    tracer.runfunc(run_tests)

    results = tracer.results()

    # Collect files to report
    files = [f for f in os.listdir('.') if f.endswith('.py')]
    total_lines = 0
    covered_lines = 0
    report = []
    for f in files:
        try:
            statements = results.counts.get((os.path.abspath(f),))
        except Exception:
            statements = None
        # We will use Python's built-in line cache to estimate total lines
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                lines = fh.readlines()
        except Exception:
            lines = []
        total = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
        # covered approximate from results.counts
        covered = 0
        for (filename, lineno), count in results.counts.items():
            if os.path.abspath(filename) == os.path.abspath(f) and count > 0:
                covered += 1

        total_lines += total
        covered_lines += covered
        pct = (covered / total * 100) if total else 100.0
        report.append((f, total, covered, pct))

    # Print report
    print('\nCoverage report (approximate):')
    for f, total, covered, pct in report:
        print(f'{f}: {covered}/{total} lines covered ({pct:.1f}%)')

    overall = (covered_lines / total_lines * 100) if total_lines else 100.0
    print(f'Overall coverage (approx): {overall:.1f}%')


if __name__ == '__main__':
    main()
