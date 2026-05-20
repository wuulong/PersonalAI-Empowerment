import os
import sqlite3

def setup_db():
    db_path = "/Users/wuulong/github/bmad-pa/events/AIBooks/PersonalEmpowerment/PersonalAI-Empowerment/data/research/Research_Artifacts.db"
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Force clean rebuild: delete existing DB file to apply updated schema
    if os.path.exists(db_path):
        print(f"🧹 Detected existing database file. Removing for a clean DDL update: {db_path}")
        try:
            os.remove(db_path)
        except Exception as e:
            print(f"⚠️ Warning: Could not delete old database file: {e}")
            
    print(f"Initializing SQLite database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Read and execute schema.sql
    if os.path.exists(schema_path):
        print(f"Loading schema from: {schema_path}")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()
        cursor.executescript(schema_sql)

    else:
        raise FileNotFoundError(f"Schema file not found at: {schema_path}")
    
    conn.commit()
    conn.close()
    print("Database initialized successfully with v1.2.0 Three-Tier Schema.")

if __name__ == "__main__":
    setup_db()

