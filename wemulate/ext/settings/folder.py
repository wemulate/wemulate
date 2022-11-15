import os
from pathlib import Path
from wemulate.ext.settings.config import get_folder_location

if not os.environ.get("WEMULATE_TESTING"):
    Path(get_folder_location()).mkdir(parents=True, exist_ok=True)
