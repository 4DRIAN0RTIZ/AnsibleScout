"""
Main TUI Application for Ansible Bot

Textual-based terminal interface for module search and browsing.
"""

import subprocess
import json
from typing import List, Tuple, Optional

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Input, ListView
from textual.binding import Binding
from rich.text import Text
from rich.console import Group
from rich.syntax import Syntax

from ..services import (
    ModuleLoader,
    SearchService,
    AIService,
    EmbeddingService,
    SemanticSearchService,
)
from ..config import Config
from .widgets import (
    SearchInput,
    ResultsList,
    DetailsPanel,
    FocusableScrollableContainer,
    ModuleListItem,
)
from .screens import ThemePalette
from .themes import get_all_themes, get_theme_names, get_syntax_theme
from .styles import CSS


class AnsibleBotApp(App):
    """Main Textual application for Ansible Module Bot"""

    CSS = CSS

    BINDINGS = [
        Binding("q", "quit", "Quit", show=True, priority=True),
        Binding("?", "show_help", "Help", show=True, priority=True),
        Binding("ctrl+p", "command_palette", "Commands", show=True, priority=True),
        Binding("/", "focus_search", "Search", show=True, priority=True),
        Binding("tab", "toggle_focus", "Tab", show=True),
        Binding("j,down", "move_down", "Down", show=True),
        Binding("k,up", "move_up", "Up", show=True),
        Binding("escape", "clear_search", "Clear", show=False),
        Binding("enter", "show_details", "Details", show=False),
        Binding("g", "goto_top", "Top", show=False),
        Binding("G", "goto_bottom", "Bottom", show=False),
        Binding("i", "focus_search", "Search", show=False),
        Binding("d", "show_details", "Details", show=False),
        Binding("ctrl+u", "page_up", "Page Up", show=False),
        Binding("ctrl+d", "page_down", "Page Down", show=False),
        Binding("ctrl+i", "ai_search", "AI Search", show=False),
        Binding("1", "select_item(1)", "1", show=False),
        Binding("2", "select_item(2)", "2", show=False),
        Binding("3", "select_item(3)", "3", show=False),
        Binding("4", "select_item(4)", "4", show=False),
        Binding("5", "select_item(5)", "5", show=False),
        Binding("6", "select_item(6)", "6", show=False),
        Binding("7", "select_item(7)", "7", show=False),
        Binding("8", "select_item(8)", "8", show=False),
        Binding("9", "select_item(9)", "9", show=False),
    ]

    def __init__(self, modules_file: str = None, theme: str = "dracula"):
        super().__init__()
        self.title = "Ansible Scout"
        self.initial_theme = theme if theme in get_theme_names() else "dracula"

        self.loader = ModuleLoader(modules_file or Config.DEFAULT_MODULES_FILE)
        self.search_service = None
        self.semantic_search_service: Optional[SemanticSearchService] = None
        self.ai_service = AIService(
            enabled=Config.AI_ENABLED and Config.validate_api_key()
        )
        self.embedding_service = EmbeddingService(
            enabled=Config.AI_ENABLED and Config.validate_api_key()
        )

        self.current_results: List[Tuple[str, str, float]] = []
        self.current_query: str = ""
        self.ai_recommendation: str = ""
        self.focus_index = 0
        self.embeddings_loading = False
        self.embeddings_ready = False

    def compose(self) -> ComposeResult:
        """Create application layout"""
        theme_status = f"Theme: {self.theme}"
        ai_status = " | [cyan]Ctrl+I: AI[/cyan]" if Config.AI_ENABLED else ""

        yield Header(show_clock=True)

        with Container(id="main-container"):
            with Vertical(id="search-container"):
                yield Static(
                    f"[bold]Search Ansible Modules[/bold] | {theme_status}{ai_status} | Press [bold]?[/bold] for help",
                    classes="status-text",
                )
                yield SearchInput(
                    placeholder="Type to search modules (e.g., 'copy files', 'install packages')...",
                    id="search-input",
                )
                # AI panel only shown if AI is enabled
                if Config.AI_ENABLED:
                    with FocusableScrollableContainer(id="ai-recommendation-container"):
                        yield Static(
                            "[bold]AI Recommendations[/bold] [dim](Press Ctrl+I for AI suggestions)[/dim]",
                            classes="status-text",
                        )
                        yield DetailsPanel(id="ai-recommendation-panel")

            with Horizontal(id="content-container"):
                with Vertical(id="results-container"):
                    yield Static(
                        "[bold]Results[/bold] [dim](j/k to navigate, 1-9 to select)[/dim]",
                        classes="status-text",
                    )
                    yield ResultsList(id="results-list")

                with FocusableScrollableContainer(id="details-container"):
                    yield Static(
                        "[bold]Details[/bold] [dim](Ctrl+d/u to scroll)[/dim]",
                        classes="status-text",
                    )
                    yield DetailsPanel(id="details-panel")

        yield Footer()

    def on_mount(self) -> None:
        """Initialize application on mount"""
        for theme in get_all_themes():
            self.register_theme(theme)

        self.theme = self.initial_theme

        modules = self.loader.load()
        self.search_service = SearchService(modules)

        # Show loading state immediately
        if Config.AI_ENABLED and self.embedding_service.enabled:
            self._update_ai_panel(
                "[yellow]⏳ Loading AI embeddings...[/yellow]\n"
                "[dim]You can start searching now. Ctrl+I will be ready shortly.[/dim]"
            )
            self.embeddings_loading = True

            # Initialize embeddings in background (non-blocking)
            self.run_worker(
                self._initialize_embeddings_background(modules),
                thread=True,  # Run in thread to not block UI
            )

        self.notify(f"Loaded {self.loader.count()} modules", severity="information")
        # Don't focus input automatically - it hides app bindings in Footer
        # User can press '/' or 'i' to focus search

    async def _initialize_embeddings_background(self, modules: dict) -> None:
        """Initialize embeddings cache for semantic search (runs in background)"""
        try:
            self.call_from_thread(
                lambda: self._update_ai_panel(
                    "[yellow]⏳ Generating embeddings (first run takes ~30s)...[/yellow]"
                )
            )

            # Try to load cached embeddings first
            if self.embedding_service.load_cached_embeddings(modules):
                self.semantic_search_service = SemanticSearchService(
                    modules, self.embedding_service
                )
                self.embeddings_ready = True
                self.embeddings_loading = False
                stats = self.embedding_service.get_stats()

                self.call_from_thread(
                    lambda: self._update_ai_panel(
                        f"[green]✓ AI ready![/green] [dim]Press Ctrl+I for semantic search ({stats['cached_embeddings']} modules)[/dim]"
                    )
                )
                self.call_from_thread(
                    lambda: self.notify(
                        f"Semantic search ready: {stats['cached_embeddings']} modules",
                        severity="information",
                    )
                )
            else:
                # Generate new embeddings
                self.call_from_thread(
                    lambda: self._update_ai_panel(
                        "[yellow]⏳ Generating embeddings (first run takes ~30s)...[/yellow]\n"
                        "[dim]Processing all Ansible modules with OpenAI...[/dim]"
                    )
                )

                if self.embedding_service.generate_embeddings(modules):
                    self.semantic_search_service = SemanticSearchService(
                        modules, self.embedding_service
                    )
                    self.embeddings_ready = True
                    self.embeddings_loading = False

                    self.call_from_thread(
                        lambda: self._update_ai_panel(
                            "[green]✓ AI ready![/green] [dim]Press Ctrl+I for semantic search[/dim]"
                        )
                    )
                    self.call_from_thread(
                        lambda: self.notify(
                            "Semantic search initialized! Press Ctrl+I for AI recommendations",
                            severity="information",
                        )
                    )
                else:
                    self.embeddings_loading = False
                    self.call_from_thread(
                        lambda: self._update_ai_panel(
                            "[red]✗ AI unavailable[/red] [dim]Check api_key in config.toml[/dim]"
                        )
                    )
                    self.call_from_thread(
                        lambda: self.notify(
                            "AI search unavailable. Check OPENAI_API_KEY",
                            severity="warning",
                        )
                    )
        except Exception as e:
            self.embeddings_loading = False
            self.call_from_thread(
                lambda: self._update_ai_panel(
                    f"[red]✗ AI error:[/red] [dim]{str(e)}[/dim]"
                )
            )
            self.call_from_thread(
                lambda: self.notify(
                    f"Could not initialize embeddings: {e}", severity="warning"
                )
            )

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle search input changes"""
        if event.input.id == "search-input":
            query = event.value.strip()
            if query:
                self._perform_search(query)
            else:
                self._clear_results()

    def _perform_search(self, query: str) -> None:
        """Execute module search"""
        if not self.search_service:
            return

        self.current_query = query
        self.current_results = self.search_service.search(
            query, limit=Config.SEARCH_LIMIT * 2
        )
        self._update_results_list()

        # AI search is now triggered manually with Ctrl+I to save tokens
        if Config.AI_ENABLED:
            self._update_ai_panel("[dim]Press Ctrl+I for AI recommendations[/dim]")

    def _update_results_list(self) -> None:
        """Refresh results ListView with current results"""
        results_list = self.query_one("#results-list", ResultsList)
        results_list.clear()

        for idx, (name, desc, score) in enumerate(self.current_results, 1):
            item = ModuleListItem(name, desc, score, idx)
            results_list.append(item)

    async def _fetch_ai_recommendations(
        self, query: str, results: List[Tuple[str, str, float]]
    ) -> None:
        """Fetch AI recommendations asynchronously"""
        try:
            recommendation = self.ai_service.get_recommendations(query, results)
            self._update_ai_panel(recommendation)
        except Exception as e:
            self._update_ai_panel(f"[red]AI Error: {str(e)}[/red]")

    def _update_ai_panel(self, content: str) -> None:
        """Update AI recommendation panel"""
        try:
            ai_panel = self.query_one("#ai-recommendation-panel", DetailsPanel)
            ai_panel.set_content(content)
        except Exception:
            pass

    def action_ai_search(self) -> None:
        """Trigger semantic AI search (Ctrl+I) - Uses embeddings for high-quality recommendations"""
        if not Config.AI_ENABLED:
            self.notify("AI features are disabled in config", severity="warning")
            return

        if not self.ai_service.is_enabled():
            self.notify(
                "AI not available. Set api_key in config.toml or OPENAI_API_KEY env var",
                severity="error",
            )
            return

        if self.embeddings_loading:
            self.notify(
                "⏳ Embeddings still loading... Please wait a moment and try again",
                severity="warning",
            )
            return

        if (
            not self.semantic_search_service
            or not self.semantic_search_service.is_ready()
        ):
            self.notify(
                "❌ Semantic search not available. Check AI panel for status",
                severity="error",
            )
            return

        # Get query from search input
        search_input = self.query_one("#search-input", SearchInput)
        query = search_input.value.strip()

        if not query:
            self.notify(
                "Type a search query first, then press Ctrl+I", severity="warning"
            )
            return

        self.current_query = query
        self._update_ai_panel("[dim]Searching with AI embeddings...[/dim]")
        self.run_worker(
            self._perform_semantic_search(query),
            exclusive=True,
        )

    async def _perform_semantic_search(self, query: str) -> None:
        """Perform semantic search and get AI recommendations"""
        try:
            # Step 1: Semantic search with embeddings (NOT fuzzy)
            semantic_results = self.semantic_search_service.search(
                query, limit=Config.SEARCH_LIMIT
            )

            if not semantic_results:
                self._update_ai_panel("[red]No results from semantic search[/red]")
                return

            # Step 2: Update results list with semantic results
            self.current_results = semantic_results
            self._update_results_list()

            # Step 3: Get AI recommendations based on semantic results
            recommendation = self.ai_service.get_recommendations(
                query, semantic_results
            )
            self._update_ai_panel(recommendation)

            # Notify user about semantic search
            self.notify(
                f"Semantic search: {len(semantic_results)} results via embeddings",
                severity="information",
            )

        except Exception as e:
            self._update_ai_panel(f"[red]Semantic search error: {str(e)}[/red]")

    def _clear_results(self) -> None:
        """Clear search results and details"""
        self.current_results = []
        self.current_query = ""
        results_list = self.query_one("#results-list", ResultsList)
        results_list.clear()
        details = self.query_one("#details-panel", DetailsPanel)
        details.set_content("[dim]No module selected[/dim]")
        if Config.AI_ENABLED:
            if self.embeddings_loading:
                self._update_ai_panel(
                    "[yellow]⏳ Loading AI embeddings...[/yellow]\n"
                    "[dim]You can start searching now. Ctrl+I will be ready shortly.[/dim]"
                )
            elif self.embeddings_ready:
                self._update_ai_panel(
                    "[green]✓ AI ready![/green] [dim]Press Ctrl+I for semantic search[/dim]"
                )
            else:
                self._update_ai_panel("[dim]Press Ctrl+I for AI recommendations[/dim]")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle module selection from list"""
        if isinstance(event.item, ModuleListItem):
            self._show_module_details(event.item.module_name)

    def _show_module_details(self, module_name: str) -> None:
        """Load and display module details"""
        details_panel = self.query_one("#details-panel", DetailsPanel)
        details_panel.set_content(f"Loading details for {module_name}...")

        self.run_worker(self._fetch_module_details(module_name), exclusive=True)

    async def _fetch_module_details(self, module_name: str) -> None:
        """Fetch module details asynchronously"""
        try:
            result = subprocess.run(
                ["ansible-doc", "-j", module_name],
                capture_output=True,
                text=True,
                timeout=Config.ANSIBLE_DOC_TIMEOUT,
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                module_data = data.get(module_name, {})
                formatted = self._format_module_details(module_name, module_data)

                details_panel = self.query_one("#details-panel", DetailsPanel)
                details_panel.set_content(formatted)
            else:
                self._show_details_error("Could not fetch module details")

        except Exception as e:
            self._show_details_error(f"Error: {str(e)}")

    def _show_details_error(self, message: str) -> None:
        """Display error in details panel"""
        details_panel = self.query_one("#details-panel", DetailsPanel)
        details_panel.set_content(f"[red]{message}[/red]")

    def _format_module_details(self, module_name: str, details: dict):
        """Format module details with Rich renderables"""
        renderables = []
        syntax_theme = get_syntax_theme(self.theme)

        text_parts = [f"[bold]{module_name}[/bold]\n"]

        if "doc" in details:
            doc = details["doc"]

            if "short_description" in doc:
                text_parts.append(f"{doc['short_description']}\n")

            if "description" in doc:
                text_parts.append("[bold]Description:[/bold]")
                desc = doc["description"]
                if isinstance(desc, list):
                    text_parts.extend([f"  {line}" for line in desc])
                else:
                    text_parts.append(f"  {desc}")
                text_parts.append("")

            if "options" in doc and doc["options"]:
                text_parts.append("[bold]Parameters:[/bold]")
                for param_name, param_info in list(doc["options"].items())[:8]:
                    required = (
                        "[red](required)[/red]"
                        if param_info.get("required", False)
                        else "[dim](optional)[/dim]"
                    )
                    text_parts.append(f"  [bold]{param_name}[/bold] {required}")

                    if "description" in param_info:
                        desc = param_info["description"]
                        if isinstance(desc, list):
                            desc = " ".join(desc)
                        text_parts.append(f"    {desc[:150]}...")
                text_parts.append("")

        renderables.append(Text.from_markup("\n".join(text_parts)))

        if "examples" in details:
            examples = details["examples"]
            if examples:
                renderables.append(Text.from_markup("\n[bold]Examples:[/bold]"))
                yaml_code = "\n".join(examples.split("\n")[:20])
                syntax = Syntax(
                    yaml_code,
                    "yaml",
                    theme=syntax_theme,
                    line_numbers=False,
                    word_wrap=True,
                )
                renderables.append(syntax)

        renderables.append(
            Text.from_markup(f"\n[dim]Full docs: ansible-doc {module_name}[/dim]")
        )

        return Group(*renderables)

    # Actions
    def action_clear_search(self) -> None:
        """Clear search input and results"""
        search_input = self.query_one("#search-input", SearchInput)
        search_input.value = ""
        self._clear_results()

    def action_show_details(self) -> None:
        """Show details for currently selected module"""
        results_list = self.query_one("#results-list", ResultsList)
        if results_list.highlighted_child:
            item = results_list.highlighted_child
            if isinstance(item, ModuleListItem):
                self._show_module_details(item.module_name)

    def action_move_up(self) -> None:
        """Move selection up in results"""
        results_list = self.query_one("#results-list", ResultsList)
        results_list.action_cursor_up()

    def action_move_down(self) -> None:
        """Move selection down in results"""
        results_list = self.query_one("#results-list", ResultsList)
        results_list.action_cursor_down()

    def action_goto_top(self) -> None:
        """Jump to first result"""
        results_list = self.query_one("#results-list", ResultsList)
        if results_list.children:
            results_list.index = 0

    def action_goto_bottom(self) -> None:
        """Jump to last result"""
        results_list = self.query_one("#results-list", ResultsList)
        if results_list.children:
            results_list.index = len(results_list.children) - 1

    def action_focus_search(self) -> None:
        """Focus search input"""
        search_input = self.query_one("#search-input", SearchInput)
        search_input.focus()
        self.focus_index = 0

    def action_page_up(self) -> None:
        """Scroll details panel up"""
        details_container = self.query_one(
            "#details-container", FocusableScrollableContainer
        )
        details_container.scroll_page_up()

    def action_page_down(self) -> None:
        """Scroll details panel down"""
        details_container = self.query_one(
            "#details-container", FocusableScrollableContainer
        )
        details_container.scroll_page_down()

    def action_toggle_focus(self) -> None:
        """Cycle focus between search, results, and details"""
        search_input = self.query_one("#search-input", SearchInput)
        results_list = self.query_one("#results-list", ResultsList)
        details_container = self.query_one(
            "#details-container", FocusableScrollableContainer
        )

        self.focus_index = (self.focus_index + 1) % 3

        if self.focus_index == 0:
            search_input.focus()
        elif self.focus_index == 1:
            results_list.focus()
        else:
            details_container.focus()

    def action_select_item(self, number: str) -> None:
        """Select result by number (1-9)"""
        idx = int(number) - 1
        results_list = self.query_one("#results-list", ResultsList)

        if 0 <= idx < len(results_list.children):
            results_list.index = idx
            if isinstance(results_list.highlighted_child, ModuleListItem):
                self._show_module_details(results_list.highlighted_child.module_name)

    def watch_theme(self, new_theme: str) -> None:
        """Called when theme changes"""
        theme_status = f"Theme: {new_theme}"

        try:
            status_widget = self.query_one("#search-container Static", Static)
            status_widget.update(
                f"[bold]Search Ansible Modules[/bold] | {theme_status} | Press [bold]?[/bold] for help"
            )
        except Exception:
            pass

        if self.current_results:
            self._update_results_list()

    def action_open_theme_palette(self) -> None:
        """Open theme selection modal"""
        self.push_screen(ThemePalette(self.theme), self._handle_theme_selection)

    def _handle_theme_selection(self, theme_name: str | None) -> None:
        """Handle theme selection from modal"""
        if theme_name and theme_name in get_theme_names():
            self.theme = theme_name
            self.notify(f"Theme changed to: {self.theme}", severity="information")

    def action_show_help(self) -> None:
        """Display help screen with keybindings"""
        help_text = """
[bold]Keyboard Shortcuts[/bold]

[bold]Navigation (Vim-style)[/bold]
  j/↓           Move down in results
  k/↑           Move up in results
  g             Jump to first result
  G             Jump to last result
  Ctrl+d        Scroll details down (page)
  Ctrl+u        Scroll details up (page)

[bold]Search[/bold]
  /  or  i      Focus search input
  Esc           Clear search

[bold]Selection[/bold]
  1-9           Jump to result by number
  Enter or d    Show module details
  Tab           Cycle focus (search → results → details)

[bold]AI Features (Semantic Search)[/bold]
  Ctrl+i        Semantic AI search with embeddings
                Finds modules by meaning, not just text

[bold]Commands[/bold]
  Ctrl+p        Open command palette (themes, actions)

[bold]General[/bold]
  ?             Show this help
  q             Quit application

[dim]The active panel is highlighted with a colored border[/dim]
        """
        details_panel = self.query_one("#details-panel", DetailsPanel)
        details_panel.set_content(help_text)
