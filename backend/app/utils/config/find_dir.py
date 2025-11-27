from pathlib import Path

def find_dir(dir_name: str, start_path: Path | None = None) -> Path:
    """
    Automatically finds a folder anywhere under the 'app' package.
    Starts searching from the current file and walks upward, then scans the entire app/ tree.
    """
    
    if start_path is None:
        start_path = Path(__file__).resolve()
        
    # First: check common quick locations
    app_dir = start_path.parent
    while app_dir.name != "app" and app_dir.parent != app_dir:
        app_dir = app_dir.parent
    if app_dir.name != "app":
        # Fallback: find the app package root
        for parent in start_path.parents:
            if parent.name == "app" and (parent.parent / "__init__.py").exists():
                app_dir = parent
                break
        else:
            raise RuntimeError("Could not find 'app' package root")
        
    # Now search the entire app/ directory for the folder
    for name_path in app_dir.rglob(dir_name):
        if name_path.is_dir():
            return name_path
        
    raise FileNotFoundError(f"No '{dir_name}' folder found inside the 'app' package")