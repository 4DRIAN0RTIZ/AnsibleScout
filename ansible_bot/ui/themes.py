"""
Theme configuration for Ansible Bot TUI

Defines color schemes and visual styling using Textual's Theme system.
"""

from textual.theme import Theme


DRACULA_THEME = Theme(
    name="dracula",
    primary="#bd93f9",
    secondary="#6272a4",
    accent="#ff79c6",
    warning="#ffb86c",
    error="#ff5555",
    success="#50fa7b",
    background="#282a36",
    surface="#44475a",
    panel="#21222c",
    dark=True,
    variables={
        "footer-key-foreground": "#282a36",
        "footer-key-background": "#bd93f9",
    }
)

ORANGE_THEME = Theme(
    name="orange",
    primary="#e38528",
    secondary="#222222",
    accent="#ff9f50",
    warning="#ffb86c",
    error="#ff5555",
    success="#50c878",
    background="#fff8f0",
    surface="#f5e6d3",
    panel="#ffe4c4",
    dark=False,
    variables={
        "footer-key-foreground": "#fff8f0",
        "footer-key-background": "#e38528",
    }
)

NORD_THEME = Theme(
    name="nord",
    primary="#88c0d0",
    secondary="#5e81ac",
    accent="#b48ead",
    warning="#ebcb8b",
    error="#bf616a",
    success="#a3be8c",
    background="#2e3440",
    surface="#3b4252",
    panel="#434c5e",
    dark=True,
    variables={
        "footer-key-foreground": "#2e3440",
        "footer-key-background": "#88c0d0",
    }
)

MONOKAI_THEME = Theme(
    name="monokai",
    primary="#66d9ef",
    secondary="#f92672",
    accent="#a6e22e",
    warning="#fd971f",
    error="#f92672",
    success="#a6e22e",
    background="#272822",
    surface="#3e3d32",
    panel="#49483e",
    dark=True,
    variables={
        "footer-key-foreground": "#272822",
        "footer-key-background": "#66d9ef",
    }
)

ALL_THEMES = [
    DRACULA_THEME,
    ORANGE_THEME,
    NORD_THEME,
    MONOKAI_THEME,
]


def get_all_themes() -> list[Theme]:
    """Get all available Theme objects"""
    return ALL_THEMES


def get_theme_names() -> list[str]:
    """Get list of available theme names"""
    return [theme.name for theme in ALL_THEMES]


def get_syntax_theme(theme_name: str) -> str:
    """Get corresponding syntax highlighting theme name"""
    syntax_map = {
        "dracula": "dracula",
        "orange": "paraiso-light",
        "nord": "nord",
        "monokai": "monokai",
    }
    return syntax_map.get(theme_name, "monokai")
