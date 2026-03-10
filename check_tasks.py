import requests, urllib3, json, time, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
urllib3.disable_warnings()
s = requests.Session()
s.verify = False

BASE = "https://gemini-mengxing.zeabur.app"

# Login
r = s.post(f"{BASE}/login", data={"admin_key": "8OfC4Wow7vu4464C1UXsU66IFKcj1WoP"})
print("Login:", r.status_code)

# Start registration
r2 = s.post(f"{BASE}/admin/register/start", json={"count": 1})
start_data = r2.json()
task_id = start_data.get("id", "")
print("Task ID:", task_id)
print("Initial:", json.dumps(start_data, indent=2, ensure_ascii=False)[:300])

# Poll via /current
for i in range(40):
    time.sleep(5)
    r3 = s.get(f"{BASE}/admin/register/current")
    data = r3.json()
    status = data.get("status", "idle")
    logs = data.get("logs", [])
    last_log = logs[-1].get("message", "") if logs else ""
    results = data.get("results", [])
    print(f"[{(i+1)*5}s] {status} | logs={len(logs)} | {last_log[:80]}")
    if results:
        for res in results:
            print(f"  Result: {res.get('status')} email={res.get('email','')} error={res.get('error','')}")
    if status in ("completed", "failed", "cancelled", "idle"):
        print(json.dumps(data, indent=2, ensure_ascii=False)[:3000])
        break
