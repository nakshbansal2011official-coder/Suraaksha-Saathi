import os
import sys
import json
import base64
import urllib.request
import urllib.error

TOKEN = os.environ.get("GITHUB_TOKEN", "")
if not TOKEN:
    # Read from local environment or prompt if missing
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_file):
        try:
            with open(env_file, "r", encoding="utf-8") as ef:
                for line in ef:
                    if line.startswith("GITHUB_TOKEN="):
                        TOKEN = line.split("=", 1)[1].strip()
                        break
        except Exception:
            pass
OWNER = "nakshbansal2011official-coder"
REPO = "Suraaksha-Saathi"
BRANCH = "main"

BASE_URL = f"https://api.github.com/repos/{OWNER}/{REPO}"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "SurakshaaSaathi-AutoSync"
}

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

def api_request(endpoint, data=None, method="GET"):
    url = f"{BASE_URL}/{endpoint}"
    req = urllib.request.Request(url, headers=HEADERS, method=method)
    if data:
        req.data = json.dumps(data).encode("utf-8")
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"API Error [{e.code}] on {endpoint}: {err_msg}")
        raise

def get_latest_commit():
    ref_data = api_request(f"git/ref/heads/{BRANCH}")
    commit_sha = ref_data["object"]["sha"]
    commit_data = api_request(f"git/commits/{commit_sha}")
    tree_sha = commit_data["tree"]["sha"]
    return commit_sha, tree_sha

def create_blob(file_path):
    with open(file_path, "rb") as f:
        content_bytes = f.read()

    # Determine if text or binary
    try:
        content_bytes.decode("utf-8")
        encoding = "utf-8"
        content_str = content_bytes.decode("utf-8")
    except:
        encoding = "base64"
        content_str = base64.b64encode(content_bytes).decode("utf-8")

    data = {
        "content": content_str,
        "encoding": encoding
    }
    blob_res = api_request("git/blobs", data, method="POST")
    return blob_res["sha"]

def collect_files():
    files_to_sync = []
    # Ignore patterns
    ignored_dirs = {".git", "__pycache__", ".vscode", ".idea"}
    ignored_files = {".DS_Store", "surakshaa_saathi.db"}

    for root, dirs, files in os.walk(WORKSPACE_DIR):
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        for f in files:
            if f in ignored_files or f.endswith(".pyc"):
                continue
            abs_path = os.path.join(root, f)
            rel_path = os.path.relpath(abs_path, WORKSPACE_DIR).replace("\\", "/")
            files_to_sync.append((abs_path, rel_path))

    return files_to_sync

def sync_to_github(commit_message="Deploy Surakshaa Saathi - National Cyber Safety Platform"):
    print(f"[*] Starting GitHub sync to {OWNER}/{REPO} on branch '{BRANCH}'...")
    commit_sha, base_tree_sha = get_latest_commit()
    print(f"[*] Current commit SHA: {commit_sha[:8]}, Base tree: {base_tree_sha[:8]}")

    files = collect_files()
    print(f"[*] Found {len(files)} files to upload...")

    tree_entries = []
    for idx, (abs_path, rel_path) in enumerate(files):
        print(f"  [{idx+1}/{len(files)}] Uploading blob: {rel_path} ...", end=" ", flush=True)
        try:
            blob_sha = create_blob(abs_path)
            tree_entries.append({
                "path": rel_path,
                "mode": "100644",
                "type": "blob",
                "sha": blob_sha
            })
            print("OK")
        except Exception as e:
            print(f"FAILED ({e})")

    print(f"[*] Creating new Git tree with {len(tree_entries)} entries...")
    tree_res = api_request("git/trees", {
        "base_tree": base_tree_sha,
        "tree": tree_entries
    }, method="POST")
    new_tree_sha = tree_res["sha"]

    print(f"[*] Creating commit with message: '{commit_message}'...")
    commit_res = api_request("git/commits", {
        "message": commit_message,
        "tree": new_tree_sha,
        "parents": [commit_sha]
    }, method="POST")
    new_commit_sha = commit_res["sha"]

    print(f"[*] Updating branch reference heads/{BRANCH} to {new_commit_sha[:8]}...")
    ref_res = api_request(f"git/refs/heads/{BRANCH}", {
        "sha": new_commit_sha
    }, method="PATCH")

    print("\n" + "="*60)
    print("SUCCESS: Surakshaa Saathi repository is live on GitHub!")
    print(f"Repository URL: https://github.com/{OWNER}/{REPO}")
    print(f"Commit SHA: {new_commit_sha}")
    print("="*60 + "\n")

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "Complete national-level Surakshaa Saathi cybersecurity platform"
    sync_to_github(msg)
