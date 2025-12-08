import os, uuid, hashlib, shelve, json
from flask import Flask, request, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = "supersecretkey"

DB_PATH = "vector_store.db"
USER_DB = "users.db"


# -----------------------------------------------------
# Utilities
# -----------------------------------------------------

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(raw, hashed):
    return hash_password(raw) == hashed


# --- Fake embedding ---
def fake_embed(text):
    """Deterministic tiny embedding using md5 hashing."""
    return [float(int(hashlib.md5(text.encode()).hexdigest()[:8], 16)) / 1e8]


# -----------------------------------------------------
# User management
# -----------------------------------------------------

def create_user(username, password, role):
    with shelve.open(USER_DB, writeback=True) as db:
        if username in db:
            return False
        db[username] = {
            "password": hash_password(password),
            "role": role
        }
        return True

def authenticate_user(username, password):
    with shelve.open(USER_DB) as db:
        user = db.get(username)
        if user and check_password(password, user["password"]):
            return user["role"]
    return None


# -----------------------------------------------------
# Document operations
# -----------------------------------------------------

def save_document(content, tags=None, doc_id=None):
    doc_id = doc_id or str(uuid.uuid4())
    tags = tags or {}
    with shelve.open(DB_PATH, writeback=True) as db:
        db[doc_id] = {
            "content": content,
            "tags": tags,
            "embedding": fake_embed(content)
        }
    return doc_id


def search_documents(question, number_of_results=3):
    """Sort by absolute difference between embeddings."""
    q_emb = fake_embed(question)

    with shelve.open(DB_PATH) as db:
        items = list(db.items())

    # Improved scoring
    def score(item):
        diff = abs(item[1]["embedding"][0] - q_emb[0])
        return diff

    items_sorted = sorted(items, key=score)
    results = []

    for doc_id, data in items_sorted[:number_of_results]:
        relevance = 1 - abs(data["embedding"][0] - q_emb[0])
        results.append({
            "document_id": doc_id,
            "content": data["content"],
            "tags": data["tags"],
            "relevance_score": round(relevance, 3)
        })

    return results


def format_answer(results, is_admin=False):
    if not results:
        return "No matching information found."

    formatted = []

    for r in results:
        if is_admin:
            formatted.append(
                f"[Document {r['document_id']} – score: {r['relevance_score']}]\n"
                f"{r['content']}\nTags: {r['tags']}\n"
            )
        else:
            snippet = r["content"][:150] + "..."
            formatted.append(
                f"[Document {r['document_id']}]\n{snippet}"
            )

    return "\n---\n\n".join(formatted)


# -----------------------------------------------------
# Routes
# -----------------------------------------------------

@app.route("/signup", methods=["GET", "POST"])
def signup():
    message = ""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")

        if not role:
            message = "Please select a role."
        elif create_user(username, password, role):
            return redirect(url_for("login"))
        else:
            message = "Username already exists."

    return render_template_string("""
    <h2>Sign Up</h2>
    <form method="POST">
        <label>Role:</label>
        <select name="role" required>
            <option value="">Select Role</option>
            <option value="admin">Admin / Teacher</option>
            <option value="parent">Parent</option>
        </select><br><br>
        <input name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit">Sign Up</button>
    </form>
    <p style='color:red;'>{{ message }}</p>
    <p>Already have an account? <a href="/login">Login</a></p>
    """, message=message)


@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = authenticate_user(username, password)

        if role:
            session["role"] = role
            session["username"] = username
            return redirect(url_for("index"))
        else:
            message = "Invalid username or password."

    return render_template_string("""
    <h2>Login</h2>
    <form method="POST">
        <input name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit">Login</button>
    </form>
    <p style='color:red;'>{{ message }}</p>
    <p>No account? <a href="/signup">Sign up</a></p>
    """, message=message)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
def index():
    role = session.get("role")
    if not role:
        return redirect(url_for("login"))

    is_admin = (role == "admin")
    message = ""
    answer_text = ""

    # Admin: Add document
    if is_admin and request.method == "POST" and "add_document" in request.form:
        content = request.form.get("content")
        tags_str = request.form.get("tags")

        try:
            tags = json.loads(tags_str) if tags_str else {}
        except:
            tags = {}

        if content:
            doc_id = save_document(content, tags)
            message = f"Document saved with ID: {doc_id}"
        else:
            message = "Content cannot be empty."

    # Query
    if request.method == "POST" and "ask_question" in request.form:
        question = request.form.get("question")
        num_results = int(request.form.get("num_results") or 3)
        results = search_documents(question, num_results)
        answer_text = format_answer(results, is_admin=is_admin)

    # Page layout
    html = f"""
    <h1>📘 RAG Demo</h1>
    <p>Logged in as <b>{session.get('username')}</b> ({role}) |
       <a href='/logout'>Logout</a></p>
    """

    if is_admin:
        html += """
        <h3>Add Document (Admin)</h3>
        <form method="POST">
            <textarea name="content" rows="4" cols="60" placeholder="Document content"></textarea><br>
            <input name="tags" placeholder='Tags as JSON (e.g. {"class":"1A"})'><br>
            <button type="submit" name="add_document">Save Document</button>
        </form>
        <hr>
        """

    html += """
    <h3>Ask a Question</h3>
    <form method="POST">
        <textarea name="question" rows="3" cols="60" placeholder="Ask something"></textarea><br>
        <input name="num_results" placeholder="Number of results (default 3)"><br>
        <button type="submit" name="ask_question">Get Answer</button>
    </form>
    """

    if message:
        html += f"<p style='color:green;'><b>{message}</b></p>"

    if answer_text:
        html += f"<pre>{answer_text}</pre>"

    return render_template_string(html)


# -----------------------------------------------------
# Run App
# -----------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
