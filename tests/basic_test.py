"""
Basic tests for Safari game
"""


def test_screen_dimensions():
    """Test that screen dimensions are correct"""
    from src.safari.constants import SCREEN_HEIGHT, SCREEN_WIDTH

    assert SCREEN_WIDTH == 1024
    assert SCREEN_HEIGHT == 768


def test_game_initialization():
    """Test that game can be initialized"""
    # This is a placeholder test
    assert True
