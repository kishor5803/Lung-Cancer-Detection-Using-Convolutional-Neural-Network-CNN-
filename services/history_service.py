from database.db import get_db_connection

def save_prediction(
    user_id,
    filename,
    predicted_class,
    confidence,
    model_name,
    heatmap_path="",
    pdf_path="",
    class_probabilities=None
):
    """Stores inference result and probability distribution in SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        INSERT INTO predictions (user_id, filename, predicted_class, confidence, model_name, heatmap_path, pdf_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (user_id, filename, predicted_class, confidence, model_name, heatmap_path, pdf_path)
    )
    prediction_id = cursor.lastrowid
    
    if class_probabilities:
        for c_name, prob in class_probabilities.items():
            cursor.execute(
                """
                INSERT INTO class_probabilities (prediction_id, class_name, probability)
                VALUES (?, ?, ?)
                """,
                (prediction_id, c_name, prob)
            )
            
    conn.commit()
    conn.close()
    return prediction_id

def get_user_history(user_id, limit=50):
    """Fetches past classifications for a given user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM predictions
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (user_id, limit)
    )
    records = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return records

def get_all_predictions(limit=100):
    """Fetches global predictions for the administrative dashboard."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT p.*, u.username
        FROM predictions p
        LEFT JOIN users u ON p.user_id = u.id
        ORDER BY p.created_at DESC
        LIMIT ?
        """,
        (limit,)
    )
    records = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return records

def get_dashboard_metrics():
    """Calculates summary telemetry for the admin dashboard."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) AS total FROM predictions")
    total_predictions = cursor.fetchone()["total"]
    
    cursor.execute("SELECT COUNT(*) AS total FROM users")
    total_users = cursor.fetchone()["total"]
    
    cursor.execute(
        """
        SELECT predicted_class, COUNT(*) as count
        FROM predictions
        GROUP BY predicted_class
        """
    )
    class_distribution = {row["predicted_class"]: row["count"] for row in cursor.fetchall()}
    
    cursor.execute("SELECT * FROM model_registry ORDER BY id ASC")
    models = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return {
        "total_predictions": total_predictions,
        "total_users": total_users,
        "class_distribution": class_distribution,
        "models": models
    }

