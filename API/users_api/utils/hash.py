import bcrypt

class Hash:

    def hash_password(password:str) -> str:
        salt = bcrypt.gensalt()
        bytes = password.encode('utf-8')
        hash = bcrypt.hashpw(bytes,salt)
        hash_password = hash.decode('utf-8')
        return hash_password

    def verify_password(password: str, hashed:str) -> bool:
        password_encode = password.encode('utf-8')
        hashed_encode = hashed.encode('utf-8')
        return bcrypt.checkpw(password_encode,hashed_encode)