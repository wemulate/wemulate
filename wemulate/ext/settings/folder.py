from pathlib import Path
from wemulate.ext.settings.config import get_folder_location

Path(get_folder_location()).mkdir(parents=True, exist_ok=True)

