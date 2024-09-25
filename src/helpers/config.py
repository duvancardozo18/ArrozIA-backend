# config.py
ALGORITHM = "HS256"
JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"  # Llave secreta para Access Tokens
JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"  # Llave secreta para Refresh Tokens
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutos
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 días
