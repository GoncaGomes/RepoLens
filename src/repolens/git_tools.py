import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


@dataclass(slots=True, frozen=True)
class Commit:
    sha: str
    subject: str


@dataclass(slots=True, frozen=True)
class ChangedFile:
    path: str
    status: Literal["Modified", "Added", "Deleted"]


def parse_commits(result: str) -> list[Commit]:
    if not result.strip():
        return []

    commits: list[Commit] = []

    for line in result.splitlines():
        parts = line.split("\x1f", 1)
        if len(parts) != 2:
            raise ValueError("Invalid commit format")
        commit = Commit(sha=parts[0], subject=parts[1])
        commits.append(commit)

    return commits


def parse_changed_files(result: str) -> list[ChangedFile]:
    parts = result.split("\x00")

    if parts and parts[-1] == "":
        parts.pop()
    else:
        raise ValueError("Malformed diff output")

    if len(parts) % 2 != 0:
        raise ValueError("Malformed diff output")
    

    changed_files = []
    for i in range(0, len(parts), 2):
        path = parts[i + 1]
        status = parts[i]
        if status not in ["A", "M", "D"]:
            raise ValueError("Status must be A, M, or D")

        match status:
            case "A":
                status = "Added"
            case "M":
                status = "Modified"
            case "D":
                status = "Deleted"
        changed_files.append(ChangedFile(path=path, status=status))

    return changed_files


def get_recent_commits(path: Path, n: int = 1) -> list[Commit]:
    git_dir = Path(path)
    if not git_dir.is_dir():
        raise NotADirectoryError

    if type(n) is not int or n <= 0:
        raise ValueError("N must be an integer greater than 0.")

    command = ["git", "-C", str(git_dir), "log", f"-{n}", "--format=%H%x1f%s"]
    subprocess_result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
    )

    return parse_commits(subprocess_result.stdout)


def get_changed_files(
    repo_path: Path,
    base: str,
    target: str,
) -> list[ChangedFile]:
    if not base.strip() or not target.strip():
        raise ValueError("Base and target must be non-empty.")

    command = ["git", "-C", str(repo_path), "diff", "--name-status", "--no-renames" ,"-z", base, target]
    subprocess_result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
    )
    if not subprocess_result.stdout:
        return []
    
    return parse_changed_files(subprocess_result.stdout)