import json
import subprocess
import os
import argparse

ENDPOINT = os.environ.get("REDMINE_MCP_URL", "http://YOUR_SERVER_IP:8000/mcp")
TOKEN = os.environ.get("REDMINE_MCP_TOKEN", "YOUR_TOKEN_HERE")

def call_mcp_tool(name, arguments):
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": name,
            "arguments": arguments
        },
        "id": 1
    }
    
    cmd = [
        "curl", "-s", "-X", "POST", ENDPOINT,
        "-H", "Content-Type: application/json",
        "-H", "Accept: application/json, text/event-stream",
        "-H", f"X-Redmine-Token: {TOKEN}",
        "-d", json.dumps(payload)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {"error": result.stderr or "Execution failed"}
    
    try:
        lines = result.stdout.splitlines()
        for line in lines:
            if line.startswith("data: "):
                data_str = line[len("data: "):]
                response = json.loads(data_str)
                if "result" in response:
                    content = response["result"].get("content", [])
                    if content and len(content) > 0:
                        return {"result": content[0].get("text", "")}
                if "error" in response:
                    return {"error": response["error"].get("message", "Unknown error")}
    except Exception as e:
        return {"error": f"Parse error: {str(e)}\nRaw: {result.stdout[:200]}"}
    
    return {"error": "No valid response data found"}

def automate_report(report_type, project_id):
    print(f"[*] Starting automated workflow for report: {report_type} (Project: {project_id})")
    print(f"[*] Using MCP Endpoint: {ENDPOINT}")
    
    sql = ""
    if report_type == "project_daily":
        sql = f"""
        SELECT 
            snapshot_date, 
            total_issues, 
            new_issues, 
            closed_issues,
            status_new,
            status_in_progress,
            status_resolved,
            status_closed
        FROM dws_project_daily_summary
        WHERE project_id = {project_id}
          AND snapshot_date >= CURRENT_DATE - INTERVAL '7 days'
        ORDER BY snapshot_date DESC
        """
    elif report_type == "dev_efficiency":
        sql = f"""
        SELECT 
            u.name, 
            COUNT(i.id) as closed_issues, 
            AVG(i.done_ratio) as avg_done
        FROM dwd_issues_full i
        JOIN dim_users u ON i.assigned_to_id = u.id
        WHERE i.project_id = {project_id}
          AND i.status_id = 5
        GROUP BY u.name
        ORDER BY closed_issues DESC
        """
    else:
        print(f"[!] Unknown report type: {report_type}")
        return

    print("[*] Executing SQL...")
    res = call_mcp_tool("execute_redmine_sql_query", {"sql": sql})
    if "error" in res:
        print(f"[X] SQL Error: {res['error']}")
        return

    print("\n" + "="*50)
    print(f" REPORT PREVIEW: {report_type.upper()}")
    print("="*50)
    
    try:
        data = json.loads(res["result"])
        if isinstance(data, dict) and "data" in data:
            rows = data["data"]
            if not rows:
                print("No data found for the given parameters.")
            else:
                headers = rows[0].keys()
                print(" | ".join(headers))
                print("-" * 50)
                for row in rows[:10]:
                    print(" | ".join(str(row.get(h, "")) for h in headers))
        else:
             print(res["result"])
    except:
        print(res["result"])
    
    print("="*50)
    print("[*] Workflow complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate Redmine Report Workflow")
    parser.add_argument("type", choices=["project_daily", "dev_efficiency"], help="Report type")
    parser.add_argument("--project", type=int, default=176, help="Project ID")
    
    args = parser.parse_args()
    automate_report(args.type, args.project)
