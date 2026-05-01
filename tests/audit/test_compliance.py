import os
import re
import json

ROOT_DIR = "/Users/ralphbetta/Documents/Work/.gr/Alpha"
DOCS_DIR = os.path.join(ROOT_DIR, "docs")

def test_software_stack_versions():
    """Verify that software versions in code match specs."""
    print("Running Software Stack Version Check...")
    errors = []
    
    # Check Go version
    go_mod_path = os.path.join(ROOT_DIR, "worker-runtime/go.mod")
    if os.path.exists(go_mod_path):
        with open(go_mod_path, 'r') as f:
            content = f.read()
            if "go 1.22" not in content:
                errors.append("Go version in go.mod is not 1.22")
    
    # Check FastAPI requirement
    pyproject_path = os.path.join(ROOT_DIR, "control-plane/pyproject.toml")
    if os.path.exists(pyproject_path):
        with open(pyproject_path, 'r') as f:
            content = f.read()
            if 'requires-python = ">=3.12"' not in content:
                errors.append("Python version requirement (>=3.12) missing or incorrect in pyproject.toml")
            
    return errors

def test_design_tokens():
    """Verify that design tokens in globals.css match Core_Tokens.md."""
    print("Running Design Token Alignment Check...")
    errors = []
    
    css_path = os.path.join(ROOT_DIR, "AlphaConsole/src/app/globals.css")
    tokens_path = os.path.join(DOCS_DIR, "Design/DesignSystem/Core_Tokens.md")
    
    if os.path.exists(css_path) and os.path.exists(tokens_path):
        with open(css_path, 'r') as f:
            css_content = f.read()
            
        if "#080808" not in css_content:
            errors.append("Surface-Deep color (#080808) missing or incorrect in globals.css")
        if "--border-muted: #262626" not in css_content:
            errors.append("Border-Muted token does not match spec (#262626)")
            
        layout_path = os.path.join(ROOT_DIR, "AlphaConsole/src/app/layout.tsx")
        if os.path.exists(layout_path):
            with open(layout_path, 'r') as f:
                layout_content = f.read()
                if "JetBrains_Mono" not in layout_content:
                    errors.append("JetBrains Mono font not implemented in layout.tsx")

    return errors

def test_seo_metadata():
    """Verify that SEO metadata is not default."""
    print("Running SEO Metadata Check...")
    errors = []
    layout_path = os.path.join(ROOT_DIR, "AlphaConsole/src/app/layout.tsx")
    
    if os.path.exists(layout_path):
        with open(layout_path, 'r') as f:
            content = f.read()
            if "Create Next App" in content:
                errors.append("Default 'Create Next App' title/description found in layout.tsx")
    
    return errors

def test_live_readiness():
    """Verify that config.py contains mandatory production fields."""
    print("Running Live Readiness Check...")
    errors = []
    config_path = os.path.join(ROOT_DIR, "control-plane/app/core/config.py")
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            content = f.read()
            mandatory_fields = ["QDRANT_URL", "MINIO_ENDPOINT", "OLLAMA_BASE_URL", "DATABASE_URL", "VAST_API_KEY"]
            for field in mandatory_fields:
                if field not in content:
                    errors.append(f"Mandatory production field '{field}' missing from config.py")
                    
    return errors

def test_infrastructure_readiness():
    """Verify that infrastructure scripts and agent shells exist."""
    print("Running Infrastructure Readiness Check...")
    errors = []
    
    bootstrap_script = os.path.join(ROOT_DIR, "scripts/init_system.sh")
    if not os.path.exists(bootstrap_script):
        errors.append("Critical infrastructure script 'scripts/init_system.sh' is missing.")
        
    required_agents = ["planner_agent.py", "reviewer_agent.py", "memory_agent.py", "tester_agent.py"]
    for agent in required_agents:
        path = os.path.join(ROOT_DIR, f"agents/{agent}")
        if not os.path.exists(path):
            errors.append(f"Specialized agent shell 'agents/{agent}' is missing.")
            
    alembic_dir = os.path.join(ROOT_DIR, "control-plane/alembic")
    if not os.path.exists(alembic_dir):
        errors.append("Database migration directory 'control-plane/alembic' is missing.")
        
    return errors

def test_production_readiness():
    """Verify that no code is using stubs or 'in production' placeholders."""
    print("Running Production Readiness Check...")
    errors = []
    
    placeholder_patterns = [
        r"#\s*In production",
        r"Stubbed for now",
        r"Simulation of",
        r"Mocking",
        r"Adjust in production",
        r"Dummy .* for simulation"
    ]
    
    # Exclude standard library/dependency paths that might be caught in venv or node_modules
    exclude_dirs = ["tests", "docs", ".agents", ".git", "node_modules", "venv", "__pycache__"]
    
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith((".py", ".go", ".ts", ".tsx")):
                path = os.path.join(root, file)
                # Skip massive generated files or vendor files if they somehow got in
                if os.path.getsize(path) > 1024 * 500: # 500KB limit
                    continue
                with open(path, 'r', errors='ignore') as f:
                    for i, line in enumerate(f, 1):
                        for pattern in placeholder_patterns:
                            if re.search(pattern, line, re.IGNORECASE):
                                errors.append(f"Placeholder in {file}:{i} -> {line.strip()}")
                                
    return errors

def test_nats_protocol():
    """Verify that NATS subjects match Software_Stack_Specs.md."""
    print("Running NATS Protocol Audit...")
    errors = []
    
    spec_subjects = [
        "agent.task.create",
        "agent.task.status",
        "agent.worker.*.exec",
        "agent.worker.logs",
        "task.*.assigned",
        "worker.ready",
        "worker.teardown.complete"
    ]
    
    # Refined search: look for strings inside NATS method calls
    nats_call_pattern = re.compile(r'(?:publish|subscribe|request)\s*\(\s*[\"\']([a-z0-9\.\*\_]+)[\"\']', re.IGNORECASE)
    
    exclude_dirs = ["tests", "docs", ".agents", ".git", "node_modules", "venv"]
    
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith((".py", ".go")):
                path = os.path.join(root, file)
                with open(path, 'r', errors='ignore') as f:
                    content = f.read()
                    matches = nats_call_pattern.findall(content)
                    for match in matches:
                        # Check if match adheres to any spec subject pattern
                        if not any(re.match(spec.replace(".", "\\.").replace("*", ".*"), match) for spec in spec_subjects):
                            errors.append(f"Non-standard NATS subject found in {file}: '{match}'")
                                    
    return errors

if __name__ == "__main__":
    all_errors = {}
    all_errors["Software Stack"] = test_software_stack_versions()
    all_errors["Design Tokens"] = test_design_tokens()
    all_errors["SEO"] = test_seo_metadata()
    all_errors["Live Readiness"] = test_live_readiness()
    all_errors["Infrastructure Readiness"] = test_infrastructure_readiness()
    all_errors["Production Readiness"] = test_production_readiness()
    all_errors["NATS Protocol"] = test_nats_protocol()
    
    has_errors = any(len(errs) > 0 for errs in all_errors.values())
    
    if has_errors:
        report_content = f"# Audit Failure Report\n**Generated:** {os.popen('date').read().strip()}\n\n"
        report_content += "The following issues were identified during the automated system audit:\n\n"
        
        for category, errs in all_errors.items():
            if errs:
                report_content += f"## {category}\n"
                for err in errs:
                    report_content += f"- [ ] {err}\n"
                report_content += "\n"
        
        with open(os.path.join(ROOT_DIR, "report.md"), "w") as f:
            f.write(report_content)
        
        print("Audit FAILED. report.md generated.")
    else:
        report_path = os.path.join(ROOT_DIR, "report.md")
        if os.path.exists(report_path):
            os.remove(report_path)
        print("Audit PASSED.")
