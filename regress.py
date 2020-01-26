"""Regression search. Execute a command-line operation on historical git commits, searching for the location
where a failure was introduced."""
from pathlib import Path
import subprocess
import argparse


def opts():
    p = argparse.ArgumentParser()
    p.add_argument('--commit', required=True, help='Commit hash where scan should start. First test will run against this commit.')
    p.add_argument('--repo', required=True, help='Local path to an existing git repo.')
    p.add_argument('-n', '--num-commits', type=int, default=5, help='Number of commit hashes to test. How far back in the repo'
                                                                    'scanned is determined by this value and --skip.')
    p.add_argument('--command', required=True, help='Command used to perform pass/fail testing.')
    p.add_argument('--dry-run', action='store_true', help='Do not execute test command, but do scan through git repo.')
    p.add_argument('--skip', type=int, default=1, help='Number of commits to skip when scanning backwards through repo.')
    p.add_argument('--stop-on-fail', action='store_true', help='Stop iterating on first failure.')
    p.add_argument('--stop-on-pass', action='store_true', help='Stop iterating on first pass.')
    return p.parse_args()


def exec(command: str) -> bool:
    """Run a command, and return True if it passes."""
    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def which_commit(repo_dir: Path) -> str:
    """Which commit is the repo currently on."""
    result = subprocess.run("git rev-parse --short=12 HEAD", cwd=repo_dir, check=True, capture_output=True)
    return result.stdout.decode().strip()


def main(args: argparse.Namespace) -> int:
    """Search through the repo for a change the breaks/fixes the regression."""
    repo_dir = Path(args.repo)
    skip = args.skip

    # Checkout the first commit to start the search.
    subprocess.call(f"git checkout {args.commit}", cwd=repo_dir)
    for i in range(args.num_commits):
        subprocess.call(f"git log --oneline -n 1", cwd=repo_dir)
        commit = which_commit(repo_dir)
        print(f"CURRENT COMMIT: {commit}")
        if not args.dry_run:
            command_passed = exec(args.command)
            print("PASS" if command_passed else "FAIL")
            if (command_passed and args.stop_on_pass) or (not command_passed and args.stop_on_fail):
                print("Termination state satisfied.")
                break

        # Work backwards through the git repo, checking out out every SKIP commit.
        subprocess.call(f"git checkout HEAD~{skip}", cwd=repo_dir)


if __name__ == "__main__":
    main(opts())
