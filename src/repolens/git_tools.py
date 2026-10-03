import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class Commit:
    sha: str
    subject: str


def parse_commits(result: str) -> list[Commit]:
    if not result.strip():
        return []
    
    commits: list[Commit] = []

    for line in result.splitlines():
        parts = line.split('\x1f', 1)
        if len(parts) != 2:
            raise ValueError("Invalid commit format")
        commit = Commit(sha = parts[0],subject = parts[1])
        commits.append(commit)

    return commits



def get_recent_commits(path: Path, n: int = 1) -> list[Commit]:
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