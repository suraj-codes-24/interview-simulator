"""
Migration: Add subtopic, tags, companies, time_complexity, space_complexity to questions table
Run this ONCE: python migrations/add_subtopic.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine
from sqlalchemy import text

def migrate():
    with engine.connect() as conn:
        # Add new columns safely (IF NOT EXISTS equivalent using try/except)
        columns = [
            "ALTER TABLE questions ADD COLUMN IF NOT EXISTS subtopic VARCHAR DEFAULT 'general'",
            "ALTER TABLE questions ADD COLUMN IF NOT EXISTS tags VARCHAR DEFAULT ''",
            "ALTER TABLE questions ADD COLUMN IF NOT EXISTS companies VARCHAR DEFAULT ''",
            "ALTER TABLE questions ADD COLUMN IF NOT EXISTS time_complexity VARCHAR DEFAULT 'N/A'",
            "ALTER TABLE questions ADD COLUMN IF NOT EXISTS space_complexity VARCHAR DEFAULT 'N/A'",
        ]
        for col in columns:
            try:
                conn.execute(text(col))
                print(f"✅ {col[:60]}...")
            except Exception as e:
                print(f"⚠️  Skipped (already exists): {e}")

        conn.commit()
        print("\n✅ Migration complete!")

if __name__ == "__main__":
    migrate()
