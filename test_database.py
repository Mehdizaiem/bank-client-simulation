import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def test_database():
    try:
        # Connect to database
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="bank_simulation",
            user="sim_admin",
            password="SimBank2024!"
        )
        
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Database connected successfully!")
        print(f"   PostgreSQL version: {version[0]}")
        
        # Check if TimescaleDB extension is available
        cursor.execute("SELECT * FROM pg_extension WHERE extname = 'timescaledb';")
        timescale = cursor.fetchone()
        if timescale:
            print("✅ TimescaleDB extension is available")
        else:
            print("⚠️ TimescaleDB extension not found (this is OK for basic testing)")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_database()
