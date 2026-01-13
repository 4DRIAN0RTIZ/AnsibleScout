"""
Custom widgets for Ansible Bot TUI

Reusable Textual widget components.
"""

from textual.widgets import Input, ListView, ListItem, Label, Static
from textual.containers import ScrollableContainer
from textual.binding import Binding
from textual.app import ComposeResult


class SearchInput(Input):
    """Custom search input with auto-focus behavior"""
    pass


class ModuleListItem(ListItem):
    """Custom list item for displaying module search results"""

    def __init__(
        self,
        module_name: str,
        description: str,
        score: float,
        index: int = 0
    ):
        super().__init__()
        self.module_name = module_name
        self.description = description
        self.score = score
        self.index = index

    def compose(self) -> ComposeResult:
        """Render the list item content"""
        score_color = self._get_score_color()

        number_display = (
            f"[bold]{self.index}[/bold] "
            if 1 <= self.index <= 9 else ""
        )

        desc_text = self._format_description()

        yield Label(
            f"{number_display}[bold]{self.module_name}[/bold] "
            f"[{score_color}]({self.score:.0f}%)[/{score_color}]\n"
            f"  {desc_text}"
        )

    def _get_score_color(self) -> str:
        """Determine color based on match score"""
        if self.score > 80:
            return "green"
        elif self.score > 60:
            return "yellow"
        return "white"

    def _format_description(self) -> str:
        """Format description with truncation"""
        max_length = 78
        if len(self.description) > max_length:
            return f"[dim]{self.description[:max_length]}...[/dim]"
        return f"[dim]{self.description}[/dim]"


class ResultsList(ListView):
    """Custom ListView for displaying search results"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DetailsPanel(Static):
    """Panel for displaying detailed module information"""

    def set_content(self, content) -> None:
        """Update panel content with string or Rich renderable"""
        self.update(content)


class FocusableScrollableContainer(ScrollableContainer):
    """ScrollableContainer with keyboard navigation support"""

    can_focus = True

    BINDINGS = [
        Binding("j,down", "scroll_down", "Scroll Down", show=False),
        Binding("k,up", "scroll_up", "Scroll Up", show=False),
        Binding("g", "scroll_home", "Scroll Top", show=False),
        Binding("G", "scroll_end", "Scroll Bottom", show=False),
    ]
