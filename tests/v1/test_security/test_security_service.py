import pytest
from fastapi import HTTPException

from app.core.sec import SecurityService


def test_create_jwt_token():
    data = {'name': 'andré'}
    token = SecurityService._create_token(data)
    assert isinstance(token, str)


def test_create_access_token_and_decode():
    data = {'name': 'andré'}
    token = SecurityService.create_access_token(data)
    assert isinstance(token, str)

    assert len(token) > 0

    decoded = SecurityService.verify_token(token)
    assert decoded
    assert decoded['name'] == 'andré'
    assert decoded['type'] == 'access'


def test_create_refresh_token_and_decode():
    data = {'name': 'andré'}
    token = SecurityService.create_refresh_token(data)
    assert isinstance(token, str)

    assert len(token) > 0

    decoded = SecurityService.verify_token(token)
    assert decoded
    assert decoded['name'] == 'andré'
    assert decoded['type'] == 'refresh'


def test_create_token_fail():
    with pytest.raises(HTTPException) as e:
        SecurityService.verify_token('wrong_token')

    assert e.value.status_code == 401  # noqa
    assert e.value.detail == 'Unauthorized'


def test_password_hashing():
    password = 'Password123'
    hash = SecurityService.get_password_hash(password)
    assert len(hash) > 0
    assert SecurityService.verify_password(password, hash)


def test_password_hashing_fail():
    password = 'Password123'
    hash = SecurityService.get_password_hash(password)
    assert len(hash) > 0
    assert not SecurityService.verify_password('WrongPassword', hash)
    assert not SecurityService.verify_password(password, 'WrongHash')
