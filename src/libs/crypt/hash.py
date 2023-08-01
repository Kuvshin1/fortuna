from passlib.hash import sha256_crypt

def hash(value: str) -> str:
  return sha256_crypt.encrypt(value)

def verify(value, hash) -> bool:
  return sha256_crypt.verify(value, hash)
