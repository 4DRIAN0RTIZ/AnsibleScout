"""
Configuration module for Ansible Bot

Centralizes all configuration settings and constants.
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Application configuration"""

    DEFAULT_MODULES_FILE = "/tmp/ansible_modules.json"

    AI_MODEL = "claude-sonnet-4-5-20250929"
    AI_MAX_TOKENS = 500

    SEARCH_LIMIT = 10
    SEARCH_RESULTS_DISPLAY = 5

    ANSIBLE_DOC_TIMEOUT = 10

    @staticmethod
    def get_api_key() -> Optional[str]:
        """Get Anthropic API key from environment"""
        return os.environ.get("ANTHROPIC_API_KEY")

    @staticmethod
    def validate_api_key() -> bool:
        """Check if API key is set"""
        return bool(Config.get_api_key())


class Colors:
    """Color scheme configuration"""

    PRIMARY = "#e38528"
    SECONDARY = "#222222"
    BACKGROUND = "#fff8f0"
    TEXT = "#1a1a1a"
