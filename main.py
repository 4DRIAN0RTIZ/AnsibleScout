#!/usr/bin/env python3
"""
Ansible Scout

Interactive terminal UI to find Ansible modules using fuzzy search
with optional AI-powered recommendations.
"""

import argparse
from ansible_bot.config import Config, load_user_config, CONFIG_PATH
from ansible_bot.ui import AnsibleBotApp
from ansible_bot.ui.themes import get_theme_names


def main():
    """Main entry point for TUI application"""
    user_cfg = load_user_config()
    Config.apply(user_cfg)

    parser = argparse.ArgumentParser(
        description="AnsibleScout - Textual TUI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"\nAvailable themes: {', '.join(get_theme_names())}"
              f"\nConfig file: {CONFIG_PATH}"
    )
    parser.add_argument(
        '--modules-file',
        default=None,
        help='Path to modules JSON file (overrides config.toml)'
    )
    parser.add_argument(
        '--theme',
        choices=get_theme_names(),
        default=None,
        help='Color theme to use (overrides config.toml)'
    )

    args = parser.parse_args()

    theme = args.theme or user_cfg.theme
    modules_file = args.modules_file or user_cfg.modules_file

    app = AnsibleBotApp(
        modules_file=modules_file,
        theme=theme
    )
    app.run()


if __name__ == "__main__":
    main()
