"""
CSS styles for Ansible Bot TUI

Centralized styling definitions using Textual design variables for theme support.
"""

CSS = """
Screen {
    background: $background;
}

Header {
    background: $primary;
    color: $background;
    text-style: bold;
}

Footer {
    background: $panel;
    color: $foreground;
    height: auto;
}

Footer > .footer--highlight {
    background: $primary;
    color: $background;
}

Footer > .footer--key {
    background: $primary;
    color: $background;
    text-style: bold;
}

#main-container {
    background: $background;
    height: 1fr;
    layout: vertical;
}

#search-container {
    height: auto;
    padding: 1;
    background: $background;
}

#search-input {
    border: solid $border;
    background: $surface;
    color: $foreground;
}

#search-input:focus {
    border: heavy $primary;
    background: $surface;
    color: $foreground;
}

#ai-recommendation-container {
    height: auto;
    max-height: 6;
    border: solid $border;
    background: $surface;
    padding: 0 1;
    margin-top: 1;
}

#ai-recommendation-container:focus-within {
    border: heavy $primary;
}

#ai-recommendation-panel {
    background: $surface;
    color: $foreground;
    padding: 0 1;
}

#content-container {
    background: $background;
    height: 1fr;
}

#results-container {
    width: 50%;
    height: 100%;
    border: solid $border;
    background: $surface;
    padding: 1;
}

#results-container:focus-within {
    border: heavy $primary;
}

#details-container {
    width: 50%;
    height: 100%;
    border: solid $border;
    background: $surface;
    padding: 1;
}

#details-container:focus-within {
    border: heavy $primary;
}

ResultsList {
    background: $surface;
    color: $foreground;
}

ResultsList:focus {
    border: none;
}

ResultsList > ListItem {
    background: $surface;
    color: $foreground;
    padding: 1;
}

ResultsList > ListItem.--highlight {
    background: $primary;
    color: $background;
    text-style: bold;
}

DetailsPanel {
    background: $surface;
    color: $foreground;
    padding: 1;
}

ScrollableContainer:focus {
    border: none;
}

.status-text {
    color: $primary;
    text-style: bold;
}

.info-text {
    color: $foreground;
}

ThemePalette {
    align: center middle;
}

#palette-container {
    width: 50;
    height: auto;
    border: solid $primary;
    background: $surface;
    padding: 1;
}

#palette-title {
    text-align: center;
    margin-bottom: 1;
}

#theme-options {
    height: auto;
    max-height: 10;
    border: none;
    background: $surface;
    color: $foreground;
}

#theme-options > .option-list--option {
    background: $surface;
    color: $foreground;
}

#theme-options > .option-list--option-highlighted {
    background: $primary;
    color: $background;
    text-style: bold;
}
"""
