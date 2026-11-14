from __future__ import annotations
import os
from pathlib import Path
import shutil
import subprocess
import pytest

from daat.source import SourceSelection, RightsDeclaration
from daat.pipeline import prepare_local
from daat.errors import AdmissionError


def git(*args, cwd: Path) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL).strip()


@pytest.fixture
def simple_repo(tmp_path):
    if not shutil.which("git"):
        pytest.skip("Git not installed")
    root = tmp_path / "sample"
    root.mkdir()
    git("init", cwd=root)
    git("config", "user.name", "Unit Test", cwd=root)
    git("config", "user.email", "test@example.invalid", cwd=root)
    (root / "README.md").write_text("# Sample\nThis is untrusted input.\n", encoding="utf-8")
    (root / ".env").write_text("NOT_A_REAL_SECRET=dummy\n", encoding="utf-8")
    (root / "script.py").write_text("print('code is never executed')\n", encoding="utf-8")
    git("add", ".", cwd=root)
    git("commit", "-m", "initial", cwd=root)
    sha = git("rev-parse", "HEAD", cwd=root)
    return tmp_path, sha


def selected(root: Path, sha: str | None):
    return SourceSelection(root, "sample", "git", "11",
                           RightsDeclaration("tenant-t", "audit", "source-grant", "actor-t", True),
                           revision=sha)


def test_git_reads_pinned_commit_without_checkout_or_secrets(simple_repo):
    root, sha = simple_repo
    batch = prepare_local(selected(root, sha))
    assert batch["source"]["revision"] == sha
    assert len(batch["records"]) == 2
    assert all(".env" not in item["anchor"]["location"] for item in batch["records"])
    assert any(".env" in msg for msg in batch["warnings"])
    assert any(item["data"].get("path") == "README.md" for item in batch["records"])


def test_unpinned_and_nonhex_git_denied(simple_repo):
    root, sha = simple_repo
    for revision in (None, "HEAD", "main", "a" * 39):
        with pytest.raises(AdmissionError):
            prepare_local(selected(root, revision))


def test_git_blob_with_private_key_is_not_returned(simple_repo):
    root, sha = simple_repo
    repo = root / "sample"
    (repo / "secrets.txt").write_text("-----BEGIN PRIVATE KEY-----\nFAKE\n", encoding="utf-8")
    git("add", ".", cwd=repo)
    git("commit", "-m", "secret fixture", cwd=repo)
    new_sha = git("rev-parse", "HEAD", cwd=repo)
    batch = prepare_local(selected(root, new_sha))
    assert all("secrets.txt" not in record["anchor"]["location"] for record in batch["records"])
    assert any("skipped_possible_secret" in warning for warning in batch["warnings"])


def test_git_original_commit_unchanged_after_later_edit(simple_repo):
    root, sha = simple_repo
    before = prepare_local(selected(root, sha))
    repo = root / "sample"
    (repo / "README.md").write_text("# Different working tree\n", encoding="utf-8")
    after = prepare_local(selected(root, sha))
    assert before["preview_sha256"] == after["preview_sha256"]
