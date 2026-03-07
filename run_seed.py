from database import SessionLocal
from data.seed import seed_all
import traceback

print("Running database seed...")
db = SessionLocal()
try:
    result = seed_all(db)
    print("Seed result:", result)
except Exception as e:
    print("Error during seeding:")
    traceback.print_exc()
finally:
    db.close()
