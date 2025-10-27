"""
Unit tests for FakeInfo._get_random_text()

Black-box: Equivalence Partitioning (EP), Boundary Value Analysis (BVA)
White-box: Decision coverage for include_danish branch
"""
import pytest

from fake_info import FakeInfo


@pytest.fixture
def fake_instance():
    """Create FakeInfo instance"""
    return object.__new__(FakeInfo)


# ========== HELPERS ==========

ASCII_CHARS = set(' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
DANISH_CHARS = set('æøåÆØÅ')
ALL_CHARS = ASCII_CHARS | DANISH_CHARS


# ========== BLACK-BOX: ==========

@pytest.mark.parametrize("length", [
    1,      # minimum
    2,      # minimum + 1
    20,     # mid-value
    39,     # max-1 for some domains
    40,     # common "max" for some domains
    100     # larger value
])
def test_length_matches_input(length, fake_instance):
    """The output string length must equal the requested length."""
    s = fake_instance._get_random_text(length=length)
    assert len(s) == length


def test_first_character_is_not_space(fake_instance):
    """The first character must never be a space."""
    for _ in range(30):
        s = fake_instance._get_random_text(length=20)
        assert s[0] != ' ', f"First char was space in: {s!r}"


@pytest.mark.parametrize("include_danish, expected_charset", [
    (True,  ASCII_CHARS | DANISH_CHARS),
    (False, ASCII_CHARS),
])
def test_only_valid_characters(include_danish, expected_charset, fake_instance):
    """
    All characters must belong to the expected character set depending on
    the include_danish flag.
    """
    s = fake_instance._get_random_text(length=40, include_danish=include_danish)
    assert all(ch in expected_charset for ch in s)


def test_no_danish_chars_when_false(fake_instance):
    """With include_danish=False, the output must not contain Danish letters."""
    for _ in range(20):
        s = fake_instance._get_random_text(length=40, include_danish=False)
        assert not any(ch in DANISH_CHARS for ch in s)


# ========== WHITE-BOX: cover include_danish branch ==========

def test_branch_include_danish_true(monkeypatch, fake_instance):
    """
    White-box: Force random.choice so that a Danish char is chosen when available
    to prove the True branch permits Danish letters.
    """
    def choose(seq):
        return 'Æ' if 'Æ' in seq else 'A'
    monkeypatch.setattr('random.choice', choose)

    s = fake_instance._get_random_text(length=10, include_danish=True)
    assert any(ch in DANISH_CHARS for ch in s)


def test_branch_include_danish_false(monkeypatch, fake_instance):
    """
    White-box: Using forced chooser, prove that with include_danish=False,
    Danish letters cannot appear.
    """
    def choose(seq):
        return 'Æ' if 'Æ' in seq else 'A'
    monkeypatch.setattr('random.choice', choose)

    s = fake_instance._get_random_text(length=10, include_danish=False)
    assert not any(ch in DANISH_CHARS for ch in s)


# ========== EDGE CASES ==========

@pytest.mark.parametrize("invalid_length", [-1, -5, -100])
def test_negative_length(invalid_length, fake_instance):
    """
    For negative length, one first character is chosen, the loop runs 0 times,
    so total length == 1.
    """
    s = fake_instance._get_random_text(length=invalid_length)
    assert len(s) == 1


def test_very_large_length_is_supported(fake_instance):
    """Stress: Large length is produced and first char is not a space."""
    s = fake_instance._get_random_text(length=5000)
    assert len(s) == 5000
    assert s[0] != ' '

def test_invalid_type_string_raises(fake_instance):
    """Type error is raised if length is a string."""
    with pytest.raises(TypeError):
        fake_instance._get_random_text(length="abc")

def test_invalid_type_none_raises(fake_instance):
    """Type error is raised if length is None."""
    with pytest.raises(TypeError):
        fake_instance._get_random_text(length=None)
