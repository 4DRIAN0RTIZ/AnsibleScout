"""
Configuration module for Ansible Bot

Centralizes all configuration settings and constants.
"""

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

CONFIG_PATH = Path.home() / ".config" / "ascout" / "config.toml"


@dataclass
class UserConfig:
    theme: str = "dracula"
    modules_file: str = "/tmp/ansible_modules.json"
    search_limit: int = 10
    search_results_display: int = 5
    ai_enabled: bool = True
    ai_model: str = "gpt-4o-mini"
    ai_max_tokens: int = 500
    ai_api_key: Optional[str] = None
    ansible_doc_timeout: int = 10


def load_user_config() -> UserConfig:
    cfg = UserConfig()
    if not CONFIG_PATH.exists():
        return cfg

    with open(CONFIG_PATH, "rb") as f:
        data = tomllib.load(f)

    ui = data.get("ui", {})
    if "theme" in ui:
        cfg.theme = ui["theme"]

    search = data.get("search", {})
    if "limit" in search:
        cfg.search_limit = int(search["limit"])
    if "results_display" in search:
        cfg.search_results_display = int(search["results_display"])

    ai = data.get("ai", {})
    if "enabled" in ai:
        cfg.ai_enabled = ai["enabled"]
    if "model" in ai:
        cfg.ai_model = ai["model"]
    if "max_tokens" in ai:
        cfg.ai_max_tokens = int(ai["max_tokens"])
    if "api_key" in ai:
        cfg.ai_api_key = ai["api_key"]

    ansible = data.get("ansible", {})
    if "doc_timeout" in ansible:
        cfg.ansible_doc_timeout = int(ansible["doc_timeout"])
    if "modules_file" in ansible:
        cfg.modules_file = ansible["modules_file"]

    return cfg


class Config:
    """Application configuration — values seeded from UserConfig at runtime"""

    DEFAULT_MODULES_FILE = "/tmp/ansible_modules.json"

    AI_ENABLED = True
    AI_MODEL = "gpt-4o-mini"
    AI_MAX_TOKENS = 500
    AI_API_KEY: Optional[str] = None

    SEARCH_LIMIT = 10
    SEARCH_RESULTS_DISPLAY = 5

    ANSIBLE_DOC_TIMEOUT = 10

    @classmethod
    def get_api_key(cls) -> Optional[str]:
        """Get API key from config (priority) or environment variable"""
        # Priority 1: API key from config file
        if cls.AI_API_KEY:
            return cls.AI_API_KEY
        # Priority 2: Environment variable
        return os.environ.get("OPENAI_API_KEY")

    @staticmethod
    def validate_api_key() -> bool:
        return bool(Config.get_api_key())

    @classmethod
    def apply(cls, user_cfg: UserConfig) -> None:
        """Override class-level defaults with values from user config."""
        cls.DEFAULT_MODULES_FILE = user_cfg.modules_file
        cls.AI_ENABLED = user_cfg.ai_enabled
        cls.AI_MODEL = user_cfg.ai_model
        cls.AI_MAX_TOKENS = user_cfg.ai_max_tokens
        cls.AI_API_KEY = user_cfg.ai_api_key
        cls.SEARCH_LIMIT = user_cfg.search_limit
        cls.SEARCH_RESULTS_DISPLAY = user_cfg.search_results_display
        cls.ANSIBLE_DOC_TIMEOUT = user_cfg.ansible_doc_timeout


class Colors:
    """Color scheme configuration"""

    PRIMARY = "#e38528"
    SECONDARY = "#222222"
    BACKGROUND = "#fff8f0"
    TEXT = "#1a1a1a"
