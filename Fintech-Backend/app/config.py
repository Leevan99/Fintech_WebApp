class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db" 
    JWT_SECRET_KEY = "MiaPrimaChiaveSegreta" # Cambia di test
    JWT_ACCESS_TOKEN_EXPIRES = 864000 # 10 giorni
    JWT_COOKIE_SECURE = False
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_BLACKLIST_ENABLED = True  # Attiva la blacklist
    JWT_BLACKLIST_TOKEN_CHECKS = ["access"]  # Blocca sia access che refresh token
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_COOKIE_CSRF_PROTECT = False
