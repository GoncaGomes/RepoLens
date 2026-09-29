from src.repolens.git_tools import get_recent_commits
from pathlib import Path

def main():
    testing_dir = Path(r"C:\dev\antenna-paper-extraction")
    recent_commits = get_recent_commits(testing_dir,5)
    for commit in recent_commits:
        print(commit)


if __name__ == "__main__":
    main()
