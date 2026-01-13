"""
Module Loader Service

Handles loading and caching of Ansible modules.
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Dict


class ModuleLoader:
    """Manages loading and caching of Ansible modules"""

    def __init__(self, modules_file: str):
        self.modules_file = modules_file
        self.modules: Dict[str, str] = {}

    def load(self) -> Dict[str, str]:
        """Load modules from JSON file or generate if needed"""
        if not os.path.exists(self.modules_file):
            self._generate_modules_file()

        with open(self.modules_file, 'r') as f:
            self.modules = json.load(f)

        return self.modules

    def _generate_modules_file(self) -> None:
        """Generate modules JSON file using ansible-doc"""
        print(f"Generating modules index from ansible-doc...")
        os.system(f"ansible-doc -l -j > {self.modules_file} 2>/dev/null")

    def get_module_details(self, module_name: str) -> dict:
        """Fetch detailed information about a module"""
        try:
            result = subprocess.run(
                ['ansible-doc', '-j', module_name],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                return data.get(module_name, {})
            return {}

        except Exception as e:
            print(f"Error fetching module details: {e}")
            return {}

    def count(self) -> int:
        """Get total number of loaded modules"""
        return len(self.modules)
