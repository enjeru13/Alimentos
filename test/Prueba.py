import bcrypt

print(bcrypt.hashpw(b"Admin123", bcrypt.gensalt()).decode())
