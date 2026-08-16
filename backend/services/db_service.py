import os
import sqlite3
from typing import Optional
from backend.config import settings

class DatabaseService:
    def __init__(self):
        self.db_path = settings.BASE_DIR / "backend" / "trustchain.db"
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS document_metadata (
                        document_hash TEXT PRIMARY KEY,
                        filename TEXT,
                        classification TEXT,
                        authenticity_score REAL,
                        ai_prediction TEXT,
                        ela_variance REAL,
                        ocr_character_count INTEGER,
                        blockchain_status TEXT,
                        transaction_hash TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
            print("[INFO] SQLite metadata database initialized successfully.")
        except Exception as e:
            print("[WARN] Database initialization exception:", e)

    def save_analysis(self, doc_hash: str, filename: str, classification: str, score: float, ai_pred: str, ela_var: float, ocr_count: int, bc_status: str, tx_hash: Optional[str] = None):
        """
        Saves application-level document analysis metadata off-chain.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO document_metadata (
                        document_hash, filename, classification, authenticity_score,
                        ai_prediction, ela_variance, ocr_character_count,
                        blockchain_status, transaction_hash
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (doc_hash, filename, classification, score, ai_pred, ela_var, ocr_count, bc_status, tx_hash))
                conn.commit()
        except Exception as e:
            print("[WARN] Save database metadata exception:", e)

    def get_analysis(self, doc_hash: str) -> Optional[dict]:
        """
        Retrieves off-chain document metadata by SHA-256 hash.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM document_metadata WHERE document_hash = ?", (doc_hash,))
                row = cursor.fetchone()
                if row:
                    return {
                        "document_hash": row[0],
                        "filename": row[1],
                        "classification": row[2],
                        "authenticity_score": row[3],
                        "ai_prediction": row[4],
                        "ela_variance": row[5],
                        "ocr_character_count": row[6],
                        "blockchain_status": row[7],
                        "transaction_hash": row[8],
                        "created_at": row[9]
                    }
        except Exception as e:
            print("[WARN] Get database metadata exception:", e)
        return None

db_service = DatabaseService()
