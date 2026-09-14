"""Build OpenWhisk ZIP actions inside their target Python runtime (Python 3.6+)."""

import argparse
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


def write_archive(source, environment, destination):
    """Include native virtualenv files, dereferencing executable symlinks."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(str(destination), "w", zipfile.ZIP_DEFLATED) as archive:
        for root, prefix in ((source, Path()), (environment, Path("virtualenv"))):
            for path in sorted(root.rglob("*")):
                relative = path.relative_to(root)
                if "__pycache__" in relative.parts or path.suffix in (".pyc", ".zip"):
                    continue
                if root == source and "virtualenv" in relative.parts:
                    continue
                if path.is_file():
                    archive.write(str(path), str(prefix / relative))


def package_actions(source, output, constraints):
    actions = sorted(path for path in source.iterdir() if path.is_dir())
    if not actions:
        raise ValueError("No action directories found")
    requirements = []
    for action in actions:
        for name in ("__main__.py", "requirements.txt"):
            if not (action / name).is_file():
                raise ValueError(f"Missing {name} in {action}")
        requirements.extend(["--requirement", str((action / "requirements.txt").resolve())])

    with tempfile.TemporaryDirectory(prefix="flight-action-packages-") as temporary:
        environment = Path(temporary) / "virtualenv"
        # Use the runtime's bundled virtualenv and seed packages, not a moving
        # installer download. All actions currently share the Redis dependency.
        subprocess.run([sys.executable, "-m", "virtualenv", "--no-download", str(environment)], check=True)
        subprocess.run(
            [
                str(environment / "bin/python"),
                "-m",
                "pip",
                "install",
                "--no-cache-dir",
                "--constraint",
                str(constraints.resolve()),
            ]
            + requirements,
            check=True,
        )
        subprocess.run([str(environment / "bin/python"), "-c", "import redis"], check=True)
        for action in actions:
            write_archive(action, environment, output / action.name / "function.zip")
            print("Packaged " + action.name, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--constraints", type=Path, required=True)
    args = parser.parse_args()
    package_actions(args.source, args.output, args.constraints)
