import json
import glob
import os

def parse_gitleaks(filepath):
    with open(filepath) as f:
        data = json.load(f)
    return [{
        "event_type": "security_finding",
        "scanner": "gitleaks",
        "type": "Secrets",
        "rule_id": item.get("RuleID"),
        "location": f"{item.get('File')}:{item.get('StartLine')}",
        "description": item.get("Description"),
        "severity": "CRITICAL"
    } for item in data]

def parse_safety(filepath):
    with open(filepath) as f:
        content = f.read()
        json_start = content.find('{')
        data = json.loads(content[json_start:]) if json_start != -1 else {}
    
    findings = []
    for vuln in data.get("vulnerabilities", []):
        findings.append({
            "event_type": "security_finding",
            "scanner": "safety",
            "type": "SCA",
            "rule_id": vuln.get("CVE") or vuln.get("vulnerability_id"),
            "package": vuln.get("package_name"),
            "installed_version": vuln.get("analyzed_version"),
            "severity": "HIGH"
        })
    return findings

def parse_checkov(filepath):
    with open(filepath) as f:
        data = json.load(f)
    results = data if isinstance(data, list) else [data]
    findings = []
    for res in results:
        for check in res.get("results", {}).get("failed_checks", []):
            findings.append({
                "event_type": "security_finding",
                "scanner": "checkov",
                "type": "IaC",
                "rule_id": check.get("check_id"),
                "description": check.get("check_name"),
                "file": check.get("file_path"),
                "severity": check.get("severity") or "MEDIUM"
            })
    return findings

def parse_semgrep(filepath):
    with open(filepath) as f:
        data = json.load(f)
    return [{
        "event_type": "security_finding",
        "scanner": "semgrep",
        "type": "SAST",
        "rule_id": item.get("check_id"),
        "file": item.get("path"),
        "line": item.get("start", {}).get("line"),
        "severity": item.get("extra", {}).get("severity", "MEDIUM")
    } for item in data.get("results", [])]

def run_ingestion():
    all_findings = []
    
    for file in glob.glob("reports/*.json"):
        filename = os.path.basename(file)
        print(f"[*] Processing {filename}...")
        
        try:
            if "gitleaks" in filename:
                all_findings.extend(parse_gitleaks(file))
            elif "safety" in filename:
                all_findings.extend(parse_safety(file))
            elif "checkov" in filename:
                all_findings.extend(parse_checkov(file))
            elif "semgrep" in filename:
                all_findings.extend(parse_semgrep(file))
        except Exception as e:
            print(f"[!] Error processing {filename}: {e}")

    print(f"\n[✓] Successfully normalized {len(all_findings)} security findings for SentinelX.")
    return all_findings

if __name__ == "__main__":
    findings = run_ingestion()
    # Output to a consolidated file
    with open("sentinelx_findings.json", "w") as f:
        json.dump(findings, f, indent=2)
    print("[+] Saved normalized report to sentinelx_findings.json")