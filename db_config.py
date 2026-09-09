import os
import mysql.connector
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

def get_db_credentials():
    """Extract database connection credentials from environment variables or DATABASE_URL."""
    db_url = os.getenv("DATABASE_URL") or os.getenv("MYSQL_URL")
    if db_url:
        parsed = urlparse(db_url)
        return {
            'host': parsed.hostname or 'localhost',
            'port': parsed.port or 3306,
            'user': parsed.username or 'root',
            'password': parsed.password or '',
            'database': parsed.path.lstrip('/') if parsed.path else 'heritage_handloom'
        }
    return {
        'host': os.getenv("DB_HOST", os.getenv("MYSQLHOST", "localhost")),
        'port': int(os.getenv("DB_PORT", os.getenv("MYSQLPORT", 3306))),
        'user': os.getenv("DB_USER", os.getenv("MYSQLUSER", "root")),
        'password': os.getenv("DB_PASSWORD", os.getenv("MYSQLPASSWORD", "")),
        'database': os.getenv("DB_NAME", os.getenv("MYSQLDATABASE", "heritage_handloom"))
    }

def get_db_connection():
    """Create a MySQL connection compatible with local, Docker, and Cloud hosted MySQL (TiDB, Aiven, Railway, Render)."""
    try:
        conn_kwargs = get_db_credentials()
        
        # Cloud SSL configuration if required
        ssl_ca = os.getenv("DB_SSL_CA")
        if ssl_ca and os.path.exists(ssl_ca):
            conn_kwargs['ssl_ca'] = ssl_ca
        elif os.getenv("DB_SSL", "").lower() in ("true", "1", "required"):
            conn_kwargs['ssl_disabled'] = False

        return mysql.connector.connect(**conn_kwargs)
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None
