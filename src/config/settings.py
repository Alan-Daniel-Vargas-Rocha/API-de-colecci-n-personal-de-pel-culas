from dotenv import load_dotenv
import os
# carga de environment
load_dotenv()

class Settings:
    
    #Configuración de la base de datos
    DB_SERVER = os.getenv("DB_SERVER")
    DB_DATABASE = os.getenv("DB_DATABASE")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    
    DATABASE_URL = (
        f"mssql+pyodbc://@ALANTONIC\\SQLEXPRESS/PeliculasCollection?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
        f"{DB_USERNAME}:"
        f"{DB_PASSWORD}@"
        f"{DB_SERVER}/"
        f"{DB_DATABASE}"
        
        "?driver=ODBC+Driver+18+for+SQL+Server"
        "&TrustServerCertificate=yes"
    )
    
settings = Settings()
    