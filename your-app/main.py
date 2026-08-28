import os
import sqlite3
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

app = FastAPI()

DB_FILE = "expense.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            amount INTEGER
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO config (key, value) VALUES ('budget', 10000)")
    conn.commit()
    conn.close()

init_db()

class ExpenseItem(BaseModel):
    title: str
    amount: int

class BudgetSetting(BaseModel):
    budget: int

@app.get("/api/data")
def get_data():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM config WHERE key = 'budget'")
    budget = cursor.fetchone()[0]
    cursor.execute("SELECT id, title, amount FROM expenses")
    items = [{"id": row[0], "title": row[1], "amount": row[2]} for row in cursor.fetchall()]
    conn.close()
    return {"budget": budget, "items": items}

@app.post("/api/budget")
def update_budget(data: BudgetSetting):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE config SET value = ? WHERE key = 'budget'", (data.budget,))
    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.post("/api/expenses")
def add_expense(item: ExpenseItem):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (title, amount) VALUES (?, ?)", (item.title, item.amount))
    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.delete("/api/expenses/{item_id}")
def delete_expense(item_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return {"status": "ok"}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
