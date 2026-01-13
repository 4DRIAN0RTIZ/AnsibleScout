"""
Modal screens for Ansible Bot TUI

Custom screen overlays for theme selection and other modals.
"""

from textual.screen import ModalScreen
from textual.containers import Container
from textual.widgets import Static, OptionList
from textual.widgets.option_list import Option
from textual.binding import Binding
from textual.app import ComposeResult

from .themes import get_all_themes


class ThemePalette(ModalScreen):
    """Modal screen for selecting color themes"""

    BINDINGS = [
        Binding("escape", "dismiss", "Close", show=False),
    ]

    def __init__(self, current_theme_name: str):
        super().__init__()
        self.current_theme_name = current_theme_name

    def compose(self) -> ComposeResult:
        """Create modal content"""
        with Container(id="palette-container"):
            yield Static(
                "[bold]Select Theme[/bold]",
                id="palette-title"
            )
            yield self._create_theme_options()

    def _create_theme_options(self) -> OptionList:
        """Create theme selection options"""
        options = []
        for theme in get_all_themes():
            indicator = " " if theme.name == self.current_theme_name else "  "
            display_name = theme.name.capitalize()
            options.append(
                Option(f"{indicator}{display_name}", id=theme.name)
            )
        return OptionList(*options, id="theme-options")

    def on_mount(self) -> None:
        """Focus options list on mount"""
        self.query_one(OptionList).focus()

    def on_option_list_option_selected(
        self,
        event: OptionList.OptionSelected
    ) -> None:
        """Handle theme selection"""
        self.dismiss(event.option_id)

    def action_dismiss(self) -> None:
        """Close modal without selection"""
        self.dismiss(None)
