import sys
import sqlite3
from pathlib import Path

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from werkzeug.security import generate_password_hash
from config import Config

def get_db_connection():
    """Returns a SQLite database connection with row dictionary mapping."""
    if not Config.DATABASE_PATH.exists():
        init_db()
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes SQLite database schemas and default administrator."""
    Config.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    schema_path = Path(__file__).parent / "schema.sql"
    
    with open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
        
    cursor = conn.cursor()
    
    # Create default administrator if not present
    cursor.execute("SELECT id FROM users WHERE username = ?", ("admin",))
    if not cursor.fetchone():
        admin_pass = generate_password_hash("admin123")
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            ("admin", admin_pass, "admin")
        )
        print("Default administrator created: admin / admin123")
        
    # Pre-populate model registry metadata
    for key, info in Config.MODELS.items():
        cursor.execute("SELECT id FROM model_registry WHERE model_key = ?", (key,))
        if not cursor.fetchone():
            cursor.execute(
                """
                INSERT INTO model_registry (model_key, model_name, version, accuracy, precision, recall, f1_score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (key, info["name"], "1.0", 0.0, 0.0, 0.0, 0.0)
            )

    conn.commit()
    conn.close()
    print("Database initialized successfully at:", Config.DATABASE_PATH)

if __name__ == "__main__":
    init_db()
