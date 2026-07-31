import os
import io
import zipfile
import requests

# Repository Configuration
REPO_OWNER = "Vithika2005"
REPO_NAME = "SOC_sentinel"

# Optional: Set GITHUB_TOKEN environment variable if repository is private.
# For public repos, downloading public artifacts doesn't strictly require authentication.
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

HEADERS = {
    "Accept": "application/vnd.github.v3+json"
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

def download_artifacts():
    os.makedirs("reports", exist_ok=True)
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/artifacts"
    
    print(f"[*] Fetching artifact list from {REPO_OWNER}/{REPO_NAME}...")
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"[!] Failed to query GitHub API: {response.status_code} - {response.text}")
        return

    artifacts = response.json().get("artifacts", [])
    if not artifacts:
        print("[!] No artifacts found in GitHub Actions.")
        return

    print(f"[+] Found {len(artifacts)} artifact(s). Downloading...")

    for artifact in artifacts:
        name = artifact["name"]
        download_url = artifact["archive_download_url"]
        
        print(f"[*] Downloading '{name}'...")
        res = requests.get(download_url, headers=HEADERS)
        
        if res.status_code == 200:
            with zipfile.ZipFile(io.BytesIO(res.content)) as z:
                z.extractall("reports")
            print(f"[✓] Extracted '{name}' into reports/")
        else:
            print(f"[!] Failed to download {name}: Status {res.status_code}")

if __name__ == "__main__":
    download_artifacts()