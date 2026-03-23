"""
データベース初期化スクリプト
todosテーブルを作成し、サンプルデータを投入します。

実行方法:
  python init_db.py
"""

import sqlite3

DATABASE = "todo.db"


def init_db():
    """データベースを初期化する"""
    conn = sqlite3.connect(DATABASE)

    # todosテーブルを作成（既に存在する場合は作り直す）
    conn.execute("DROP TABLE IF EXISTS todos")
    conn.execute("""
        CREATE TABLE todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    """)

    # サンプルデータを投入
    sample_todos = [
        ("レポートを書く", False),
        ("牛乳を買う", False),
        ("部屋を掃除する", True),
    ]

    conn.executemany(
        "INSERT INTO todos (title, done) VALUES (?, ?)",
        sample_todos
    )

    conn.commit()
    conn.close()

    print(f"データベース '{DATABASE}' を初期化しました。")
    print(f"サンプルデータ {len(sample_todos)} 件を投入しました。")


if __name__ == "__main__":
    init_db()
