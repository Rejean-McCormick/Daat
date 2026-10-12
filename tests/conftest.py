from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]

@pytest.fixture
def root():
    return ROOT

@pytest.fixture
def native_profile(root):
    return root/'mappings/native/profile.json'

@pytest.fixture
def foreign_profile(root):
    return root/'mappings/foreign-inventory/profile.json'
