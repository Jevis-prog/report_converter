from app.core.services.user_services import get_welcome_text


def test_get_welcome_text() -> None:
    welcome_text = get_welcome_text('ABC')
    assert 'ABC' in welcome_text
    assert 'CCC' not in welcome_text
