from argon2 import PasswordHasher, exceptions as argon2_exceptions

# Contexte sécurisé par défaut (argon2id, itérations contrôlées)
hasher = PasswordHasher()

def hash_password(password: str) -> str:
    return hasher.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    try:
        return hasher.verify(hashed, password)
    except argon2_exceptions.VerifyMismatchError:
        return False
    except argon2_exceptions.VerificationError:
        return False
