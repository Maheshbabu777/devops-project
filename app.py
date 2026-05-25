# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os

app = Flask(__name__)

DATABASE = "todos.db"

def get_db():
    """Open a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row   # rows behave like dicts
    return conn


def init_db():
    """Create the todos table if it doesn't exist."""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                task      TEXT    NOT NULL,
                done      INTEGER NOT NULL DEFAULT 0,
                created   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


@app.route("/")
def home():
    """Render all todos, split into pending and completed."""
    with get_db() as conn:
        todos = conn.execute(
            "SELECT * FROM todos ORDER BY created DESC"
        ).fetchall()
    pending   = [t for t in todos if not t["done"]]
    completed = [t for t in todos if t["done"]]
    return render_template("index.html", pending=pending, completed=completed)


@app.route("/add", methods=["POST"])
def add():
    """Insert a new todo."""
    task = request.form.get("task", "").strip()
    if task:
        with get_db() as conn:
            conn.execute("INSERT INTO todos (task) VALUES (?)", (task,))
            conn.commit()
    return redirect(url_for("home"))


@app.route("/toggle/<int:todo_id>")
def toggle(todo_id):
    """Flip the done/undone state of a todo."""
    with get_db() as conn:
        conn.execute(
            "UPDATE todos SET done = 1 - done WHERE id = ?", (todo_id,)
        )
        conn.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    """Delete a todo permanently."""
    with get_db() as conn:
        conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()
    return redirect(url_for("home"))


@app.route("/health")
def health():
    """Health-check endpoint (used by Kubernetes probes)."""
    try:
        with get_db() as conn:
            conn.execute("SELECT 1")
        return jsonify(status="healthy", database="connected")
    except Exception as e:
        return jsonify(status="unhealthy", error=str(e)), 500


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)