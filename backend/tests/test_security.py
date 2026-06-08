from app.core.security import create_token, decode_token, hash_password, verify_password


def test_password_hash_roundtrip():
    password_hash = hash_password("ChangeMe123!")
    assert verify_password("ChangeMe123!", password_hash)
    assert not verify_password("wrong-password", password_hash)


def test_jwt_roundtrip():
    token = create_token("user-1", "access")
    payload = decode_token(token, "access")
    assert payload["sub"] == "user-1"

