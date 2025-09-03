# Intentionally vulnerable for Semgrep testing. Do NOT run in prod.
import os, subprocess, pickle, yaml, hashlib, sqlite3, requests
from flask import Flask, request

app = Flask(__name__)
app.config["DEBUG"] = True  # flask.debug.true

@app.route("/eval")
def eval_route():
    cmd = request.args.get("cmd", "")
    return str(eval(cmd))  # python.lang.security.audit.eval

@app.route("/shell")
def shell_route():
    user_input = request.args.get("q", "id")
    subprocess.call(user_input, shell=True)  # subprocess.shell_true

@app.route("/sql")
def sql_route():
    q = request.args.get("name", "")
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name = '%s'" % q)  # sql-injection
    rows = c.fetchall()
    conn.close()
    return {"rows": rows}

def weak_hash(pw: str) -> str:
    return hashlib.md5(pw.encode()).hexdigest()  # weak-crypto-md5

def bad_yaml_load(s: str):
    return yaml.load(s)  # pyyaml.load-without-loader

def bad_pickle(path: str):
    with open(path, "rb") as f:
        return pickle.load(f)  # unsafe-deserialization

def insecure_request(url: str):
    return requests.get(url, verify=False)  # tls-insecure-noverify

if __name__ == "__main__":
    app.run()