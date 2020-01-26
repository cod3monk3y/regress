"""Generates an invoke task file for regression testing."""
from pathlib import Path
import subprocess
import sys

_ITERATIONS=10
"""Number of times to run the test."""

_EXIT_ON_FAIL=True
"""Exit immediately on failure instead of producing stats. Speeds up bisect/regression when set to True."""

_TASKS = 'abcdefghijklmnopqrstuvwxyz'


def generate_tasks():
    """Generate a task file with lots of individual tasks."""
    with Path('tasks.py').open('w') as fp:
        fp.write("from invoke import task")
        for char in _TASKS:
           task = f"""
@task
def {char}(ctx):
    ctx.run('echo {char} >> _out.txt')
"""
           fp.write(task)


def generate_executor():
    """Build a task executor batch script which invokes all the generated tasks in one step."""
    with Path('_exec.bat') as p:
        p.write_text(f'@invoke {" ".join(_TASKS)}')


def run_executor():
    failure_count = 0
    total_count = 0
    output = Path('_out.txt')
    for i in range(_ITERATIONS):
        total_count += 1
        if output.exists():
            output.unlink()
            if output.exists():
                raise IOError("Unable to delete temp output file")
        subprocess.run("cmd /c _exec.bat", check=True)

        # verify the last line in the file
        with output.open('r') as fp:
            lines = [x for x in fp.readlines() if x.strip() != '']

        last_line = lines[-1].strip()
        success = last_line == 'z'
        result = '.' if success  else "F"
        print(f"[{i}] {last_line} {result}")
        if not success:
            failure_count += 1
            if _EXIT_ON_FAIL:
                break

    print(f"Failures: {failure_count}/{total_count}")
    return_code = 0 if failure_count == 0 else 1
    return return_code


def main():
    generate_tasks()
    generate_executor()
    return_code = run_executor()
    sys.exit(return_code)


if __name__ == "__main__":
    main()