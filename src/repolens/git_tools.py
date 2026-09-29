import subprocess
from pathlib import Path


def parse_commits(result: str) -> list[dict[str, str]]:
    if not result.strip():
        return []
    
    commits = []
    for commit in result.splitlines():
        parts = commit.split('\x1f', 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid commit format: {commit}")
        commits.append({
            "sha": parts[0],
            "subject": parts[1]
            })

    return commits



def get_recent_commits(path: Path, n: int = 1) -> list[dict[str, str]]:
    git_dir = Path(path)
    if not git_dir.is_dir():
        raise NotADirectoryError

    if type(n) is not int or n <= 0:
        raise ValueError("N must be an integer greater than 0.")

    command = ['git', '-C', str(git_dir) ,'log', f"-{n}", '--format=%H%x1f%s']
    subprocess_result = subprocess.run(command, 
                   capture_output=True, 
                   text=True, 
                   check=True,
                   )

    return parse_commits(subprocess_result.stdout)