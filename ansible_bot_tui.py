#!/usr/bin/env python3
"""
Ansible Scout

Interactive terminal UI to find Ansible modules using fuzzy search
with optional AI-powered recommendations.
"""

import argparse
from ansible_bot.ui import AnsibleBotApp
from ansible_bot.ui.themes import get_theme_names


def main():
    """Main entry point for TUI application"""
    parser = argparse.ArgumentParser(
        description="AnsibleScout - Textual TUI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""

Available themes: """ + ", ".join(get_theme_names())
    )
    parser.add_argument(
        '--modules-file',
        default=None,
        help='Path to modules JSON file (default: /tmp/ansible_modules.json)'
    )
    parser.add_argument(
        '--theme',
        choices=get_theme_names(),
        default='dracula',
        help='Color theme to use'
    )

    args = parser.parse_args()

    app = AnsibleBotApp(
        modules_file=args.modules_file,
        theme=args.theme
    )
    app.run()


if __name__ == "__main__":
    main()
