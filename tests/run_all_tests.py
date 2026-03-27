import json
import subprocess
import os

ENDPOINT = "http://YOUR_SERVER_IP:8000/mcp"
PROJECT_ID = 176  # myCIM2+ DevOps

TOKEN = os.environ.get("REDMINE_MCP_TOKEN", "YOUR_TOKEN_HERE")

def call_mcp_tool(method_name, arguments={}):
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": method_name,
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
    try:
        if result.returncode != 0:
             return {"status": "FAIL", "type": "INTERNAL", "error": result.stderr or "Error running curl"}
        
        # Parse event-stream
        lines = result.stdout.splitlines()
        response = {}
        for line in lines:
            if line.startswith("data: "):
                response = json.loads(line[6:])
                break
        
        if not response:
            return {"status": "FAIL", "type": "INTERNAL", "error": "No data in response"}

        if "error" in response:
            return {"status": "FAIL", "type": "VALIDATION", "error": response["error"]["message"]}
        
        res_obj = response.get("result", {})
        content = res_obj.get("content", [])
        if content and len(content) > 0:
            text = content[0].get("text", "")
            is_error = content[0].get("isError", False)
            
            # Categorization
            if "not defined" in text or "NameError" in text or "TypeError" in text or "Traceback" in text:
                return {"status": "FAIL", "type": "CODE_BUG", "error": text[:200]}
            if "lacks permission" in text or "requires admin access" in text or "Access denied" in text:
                return {"status": "FAIL", "type": "PERMISSION", "error": text[:100]}
            if is_error:
                return {"status": "FAIL", "type": "OTHER_ERROR", "error": text[:100]}
            
            return {"status": "PASS", "type": "SUCCESS", "data": text[:100]}
        else:
             return {"status": "FAIL", "type": "EMPTY", "error": "No content in result"}
             
    except Exception as e:
        return {"status": "FAIL", "type": "EXCEPTION", "error": str(e)}

# Comprehensive Diagnostic List (Excluding ETL/Trigger)
diagnostic_tools = [
     ("list_redmine_projects", {}),
     ("list_my_redmine_issues", {"filters": {"limit": 1}}),
     ("search_redmine_issues", {"query": "DevOps"}),
     ("get_redmine_issue", {"issue_id": 78540}),
     ("create_redmine_issue", {"project_id": 176, "subject": "Diag Test"}),
     ("update_redmine_issue", {"issue_id": 78540, "fields": {"notes": "Diag"}}),
     ("get_redmine_data_catalog", {"schema": "warehouse"}),
     ("search_redmine_data_catalog", {"keyword": "issue"}),
     ("execute_redmine_sql_query", {"sql": "SELECT 1"}),
     ("save_redmine_report_template", {"code_content": "# test"}),
     ("preview_redmine_template", {"template_id": "tpl_project_daily"}),
     ("get_redmine_template_versions", {"template_id": "tpl_project_daily"}),
     ("rollback_redmine_template_version", {"template_id": "tpl_project_daily", "target_version": 1}),
     ("compare_redmine_template_versions", {"template_id": "tpl_project_daily", "version_a": 1, "version_b": 2}),
     ("activate_redmine_template_version", {"template_id": "tpl_project_daily", "version": 1}),
     ("get_redmine_active_template_version", {"template_id": "tpl_project_daily"}),
     ("get_redmine_report_template", {"template_id": "tpl_project_daily"}),
     ("list_redmine_report_templates", {}),
     ("execute_redmine_report_template", {"template_id": "tpl_project_daily"}),
     ("run_redmine_template_now", {"template_id": "tpl_project_daily"}),
     ("subscribe_redmine_template", {"template_id": "tpl_project_daily", "channel": "email"}),
     ("send_redmine_subscription_reports", {"report_type": "daily"}),
     ("search_entire_redmine", {"query": "DevOps"}),
     ("get_redmine_wiki_page", {"project_id": 176, "wiki_page_title": "Wiki"}),
     ("create_redmine_wiki_page", {"project_id": 176, "wiki_page_title": "DiagPage", "text": "Diag"}),
     ("update_redmine_wiki_page", {"project_id": 176, "wiki_page_title": "DiagPage", "text": "Diag2"}),
]

print("\n--- Starting Global Diagnostic Scan ---")
results = {}
for method, args in diagnostic_tools:
    print(f"Checking {method}... ", end="", flush=True)
    res = call_mcp_tool(method, args)
    print(f"[{res['type'] if res['status'] == 'FAIL' else 'PASS'}]")
    results[method] = res

with open("/docker/redmine-mcp-client/tests/diagnostic_results.json", "w") as f:
    json.dump(results, f, indent=4)
