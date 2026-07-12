import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_db():
    try:
        print("Menghubungkan ke PostgreSQL (database default 'postgres')...")
        # Hubungkan ke postgres default
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            host='localhost',
            port=5432
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Cek apakah database 'tobaguide_db' sudah ada
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'tobaguide_db'")
        exists = cursor.fetchone()
        
        if not exists:
            print("Membuat database 'tobaguide_db'...")
            cursor.execute("CREATE DATABASE tobaguide_db")
            print("Database 'tobaguide_db' berhasil dibuat!")
        else:
            print("Database 'tobaguide_db' sudah ada, tidak perlu dibuat ulang.")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    create_db()
