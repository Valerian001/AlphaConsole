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
    
    # Check FastAPI version pinning
    pyproject_path = os.path.join(ROOT_DIR, "control-plane/pyproject.toml")
    if os.path.exists(pyproject_path):
        with open(pyproject_path, 'r') as f:
            content = f.read()
            if 'fastapi =' in content and 'fastapi = ">=' not in content and 'fastapi = "' not in content:
                # This is a bit loose, let's look for specific pinning
                if '"fastapi"' in content:
                    errors.append("FastAPI version is not pinned in pyproject.toml")
            if 'requires-python' not in content:
                errors.append("Python version requirement missing from pyproject.toml")

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
        with open(tokens_path, 'r') as f:
            tokens_content = f.read()
            
        # Check Surface-Deep
        if "#080808" not in css_content:
            errors.append("Surface-Deep color (#080808) missing or incorrect in globals.css")
            
        # Check Typography (Monospace)
        if "JetBrains Mono" not in css_content and "JetBrains Mono" in tokens_content:
            # Check if it's imported in layout.tsx instead
            layout_path = os.path.join(ROOT_DIR, "AlphaConsole/src/app/layout.tsx")
            with open(layout_path, 'r') as f:
                layout_content = f.read()
                if "JetBrains_Mono" not in layout_content:
                    errors.append("JetBrains Mono font not implemented (found Geist Mono or default)")

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
            mandatory_fields = ["QDRANT_URL", "MINIO_ENDPOINT", "OLLAMA_BASE_URL"]
            for field in mandatory_fields:
                if field not in content:
                    errors.append(f"Mandatory production field '{field}' missing from config.py")
                    
    return errors

if __name__ == "__main__":
    all_errors = {}
    all_errors["Software Stack"] = test_software_stack_versions()
    all_errors["Design Tokens"] = test_design_tokens()
    all_errors["SEO"] = test_seo_metadata()
    all_errors["Live Readiness"] = test_live_readiness()
    
    has_errors = any(len(errs) > 0 for errs in all_errors.values())
    
    if has_errors:
        report_content = "# Audit Failure Report\n\n"
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
        print("Audit PASSED.")
