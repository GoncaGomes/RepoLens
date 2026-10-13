from pathlib import Path

from src.repolens.git_tools import get_recent_commits, get_changed_files


def main():
    testing_dir = Path(r"C:\dev\antenna-paper-extraction")
    recent_commits = get_recent_commits(testing_dir,5)
    for commit in recent_commits:
        print(f"{commit.sha}: {commit.subject}")

    sha_commit_target = recent_commits[-2].sha
    sha_commit_base = recent_commits[-1].sha

    changed_files = get_changed_files(testing_dir, sha_commit_base, sha_commit_target)
    for changed_file in changed_files:
        print(f"{changed_file.status}: {changed_file.path}")

if __name__ == "__main__":
    main()
