"""
Vulnerable Flask Application - Redis Web Interface
Intentionally insecure for assignment

NOTE: This entire file is AI generated, checked with Lukas
"""

import os
import redis
from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "password123")

# Connect to Redis using environment variables
redis_client = redis.Redis(
    host=os.environ.get("REDIS_HOST", "127.0.0.1"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    decode_responses=True
)

# ============================================================================
# HTML Templates (inline for single-file deployment)
# ============================================================================

BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Redis Manager</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #1a1a2e; color: #eee; }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { color: #e94560; }
        h2 { color: #0f3460; background: #16213e; padding: 10px; border-radius: 5px; color: #eee; }
        form { background: #16213e; padding: 20px; border-radius: 8px; margin: 15px 0; }
        input, textarea { width: 95%; padding: 10px; margin: 8px 0; border: 1px solid #0f3460;
                         border-radius: 4px; background: #1a1a2e; color: #eee; }
        button { background: #e94560; color: white; padding: 10px 25px; border: none;
                border-radius: 4px; cursor: pointer; margin: 5px; }
        button:hover { background: #c81e45; }
        .data-table { width: 100%; border-collapse: collapse; margin: 15px 0; }
        .data-table th, .data-table td { padding: 10px; border: 1px solid #0f3460; text-align: left; }
        .data-table th { background: #0f3460; }
        .data-table tr:hover { background: #16213e; }
        .alert { padding: 12px; border-radius: 4px; margin: 10px 0; }
        .alert-success { background: #1b4332; border: 1px solid #2d6a4f; }
        .alert-danger { background: #461220; border: 1px solid #e94560; }
        .nav { margin: 20px 0; }
        .nav a { color: #e94560; margin-right: 15px; text-decoration: none; }
        .nav a:hover { text-decoration: underline; }
        .warning { background: #461220; border: 2px solid #e94560; padding: 15px;
                  border-radius: 8px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Redis Data Manager</h1>
        <div class="warning">
            ⚠️ WARNING: This application is intentionally vulnerable.
            Do NOT use in production or expose to the internet.
        </div>
        <div class="nav">
            <a href="/">Home</a>
            <a href="/store">Store Data</a>
            <a href="/query">Query Data</a>
            <a href="/users">User Management</a>
            <a href="/info">System Info</a>
        </div>
        <hr>
        {{ content | safe }}
    </div>
</body>
</html>
"""

HOME_CONTENT = """
<h2>Dashboard</h2>
<p>Connected to Redis at {{ redis_host }}:{{ redis_port }}</p>
<p>Total keys in database: <strong>{{ total_keys }}</strong></p>
<h3>Stored Keys:</h3>
{% if keys %}
<table class="data-table">
    <tr><th>Key</th><th>Value</th><th>Action</th></tr>
    {% for key, value in keys %}
    <tr>
        <td>{{ key }}</td>
        <td>{{ value }}</td>
        <td>
            <form method="POST" action="/delete" style="display:inline;background:none;padding:0;margin:0;">
                <input type="hidden" name="key" value="{{ key }}">
                <button type="submit">Delete</button>
            </form>
        </td>
    </tr>
    {% endfor %}
</table>
{% else %}
<p>No keys stored yet.</p>
{% endif %}
"""

STORE_CONTENT = """
<h2>Store Data</h2>
{% if message %}
<div class="alert alert-success">{{ message }}</div>
{% endif %}
<form method="POST" action="/store">
    <label>Key:</label>
    <input type="text" name="key" placeholder="Enter key name" required>
    <label>Value:</label>
    <textarea name="value" rows="4" placeholder="Enter value" required></textarea>
    <button type="submit">Store in Redis</button>
</form>
"""

# VULNERABLE: Raw query execution with no input sanitization
QUERY_CONTENT = """
<h2>Query Redis</h2>
<p>Execute Redis commands directly:</p>
{% if message %}
<div class="alert alert-success">{{ message }}</div>
{% endif %}
{% if error %}
<div class="alert alert-danger">{{ error }}</div>
{% endif %}
<form method="POST" action="/query">
    <label>Redis Command:</label>
    <input type="text" name="command" placeholder="e.g., KEYS *, GET mykey, INFO" required>
    <button type="submit">Execute</button>
</form>
{% if result %}
<h3>Result:</h3>
<pre style="background:#16213e;padding:15px;border-radius:5px;overflow-x:auto;">{{ result }}</pre>
{% endif %}
"""

USERS_CONTENT = """
<h2>User Management</h2>
{% if message %}
<div class="alert alert-success">{{ message }}</div>
{% endif %}
<form method="POST" action="/users">
    <label>Username:</label>
    <input type="text" name="username" required>
    <label>Password:</label>
    <input type="password" name="password" required>
    <label>Role:</label>
    <input type="text" name="role" value="user">
    <button type="submit">Create User</button>
</form>
<h3>Existing Users:</h3>
{% if users %}
<table class="data-table">
    <tr><th>Username</th><th>Password</th><th>Role</th></tr>
    {% for user in users %}
    <tr>
        <td>{{ user.username }}</td>
        <td>{{ user.password }}</td>
        <td>{{ user.role }}</td>
    </tr>
    {% endfor %}
</table>
{% else %}
<p>No users created yet.</p>
{% endif %}
"""

# VULNERABLE: Exposes server configuration details
INFO_CONTENT = """
<h2>System Information</h2>
<div class="warning">
    This page exposes sensitive system information - a real vulnerability!
</div>
<pre style="background:#16213e;padding:15px;border-radius:5px;overflow-x:auto;">{{ info }}</pre>
"""

# ============================================================================
# Routes
# ============================================================================

@app.route("/")
def home():
    """Dashboard showing all stored Redis keys and values."""
    try:
        all_keys = redis_client.keys("*")
        keys = []
        for key in sorted(all_keys):
            try:
                value = redis_client.get(key)
                if value:
                    keys.append((key, value))
            except redis.ResponseError:
                keys.append((key, "[non-string type]"))
        
        content = render_template_string(HOME_CONTENT,
            keys=keys,
            total_keys=len(all_keys),
            redis_host=os.environ.get("REDIS_HOST", "127.0.0.1"),
            redis_port=os.environ.get("REDIS_PORT", 6379)
        )
    except redis.ConnectionError:
        content = '<div class="alert alert-danger">Cannot connect to Redis!</div>'
    
    return render_template_string(BASE_TEMPLATE, content=content)


@app.route("/store", methods=["GET", "POST"])
def store():
    """Store key-value pairs in Redis. No input validation (VULNERABLE)."""
    message = None
    if request.method == "POST":
        key = request.form.get("key", "")
        value = request.form.get("value", "")
        # VULNERABLE: No input sanitization or validation
        redis_client.set(key, value)
        message = f"Stored: {key} = {value}"
    
    content = render_template_string(STORE_CONTENT, message=message)
    return render_template_string(BASE_TEMPLATE, content=content)


@app.route("/delete", methods=["POST"])
def delete():
    """Delete a key from Redis."""
    key = request.form.get("key", "")
    redis_client.delete(key)
    return redirect(url_for("home"))


@app.route("/query", methods=["GET", "POST"])
def query():
    """
    Execute raw Redis commands (VULNERABLE).
    Allows arbitrary command execution against Redis backend.
    """
    result = None
    message = None
    error = None
    
    if request.method == "POST":
        command = request.form.get("command", "")
        try:
            # VULNERABLE: Direct command execution with no filtering
            parts = command.split()
            response = redis_client.execute_command(*parts)
            
            # Format the response for display
            if isinstance(response, list):
                result = "\n".join(str(item) for item in response)
            elif isinstance(response, bytes):
                result = response.decode("utf-8")
            else:
                result = str(response)
            
            message = f"Executed: {command}"
        except Exception as e:
            error = f"Error: {str(e)}"
    
    content = render_template_string(QUERY_CONTENT,
        result=result, message=message, error=error)
    return render_template_string(BASE_TEMPLATE, content=content)


@app.route("/users", methods=["GET", "POST"])
def users():
    """
    User management page.
    VULNERABLE: Stores passwords in plaintext in Redis.
    VULNERABLE: Displays passwords in the UI.
    """
    message = None
    
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        role = request.form.get("role", "user")
        
        # VULNERABLE: Plaintext password storage
        redis_client.hset(f"user:{username}", mapping={
            "username": username,
            "password": password,
            "role": role
        })
        message = f"User '{username}' created successfully"
    
    # Retrieve all users
    user_list = []
    for key in redis_client.keys("user:*"):
        user_data = redis_client.hgetall(key)
        if user_data:
            user_list.append(user_data)
    
    content = render_template_string(USERS_CONTENT,
        users=user_list, message=message)
    return render_template_string(BASE_TEMPLATE, content=content)


@app.route("/info")
def info():
    """
    VULNERABLE: Exposes Redis server information.
    Leaks version, OS, memory, connected clients, etc.
    """
    try:
        redis_info = redis_client.info()
        formatted = "\n".join(f"{k}: {v}" for k, v in redis_info.items())
    except Exception as e:
        formatted = f"Error: {str(e)}"
    
    content = render_template_string(INFO_CONTENT, info=formatted)
    return render_template_string(BASE_TEMPLATE, content=content)


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    # Seed some default data for the competition
    try:
        redis_client.set("app:name", "Vulnerable Redis Manager")
        redis_client.set("app:version", "1.0.0")
        redis_client.set("flag:secret", "FLAG{r3d1s_unauth_acc3ss_ftw}")
        redis_client.hset("user:admin", mapping={
            "username": "admin",
            "password": "admin123!",
            "role": "administrator"
        })
    except Exception:
        pass
    
    # Listen on all interfaces via Flask (behind Nginx proxy)
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("FLASK_APP_PORT", 5000)),
        debug=False
    )