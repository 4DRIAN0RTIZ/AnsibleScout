# AnsibleScout

Scout and discover Ansible modules instantly with fuzzy search recommendations.

## Features

- Real-time fuzzy search as you type
- Vim-style keyboard navigation
- Split-panel interface: results and details
- Module details with parameters and examples
- Quick selection with number keys (1-9)
- Multiple color themes (Original, Dracula)
- Theme switching with Ctrl+P

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Basic mode
./ansible_bot_tui.py

# With custom theme
./ansible_bot_tui.py --theme dracula

# Custom modules file location
./ansible_bot_tui.py --modules-file /path/to/modules.json
```

## Keyboard Shortcuts

### Navigation (Vim-style)
- `j` or `↓` - Move down (in results) or scroll down (in details)
- `k` or `↑` - Move up (in results) or scroll up (in details)
- `g` - Jump to first (results) or top (details)
- `G` - Jump to last (results) or bottom (details)
- `Ctrl+d` - Scroll details down (page)
- `Ctrl+u` - Scroll details up (page)

### Search
- `/` or `i` - Focus search input
- `Esc` - Clear search

### Selection
- `1-9` - Jump directly to result by number
- `Enter` or `d` - Show module details
- `Tab` - Cycle focus between search, results, and details (highlighted with orange border)

### General
- `?` - Show help screen
- `q` - Quit application
- `Ctrl+c` - Quit application

## Examples

### Search for file copying modules
1. Type "copy files" in the search box
2. Press `1` to jump to the first result
3. Use `j`/`k` to browse other results
4. Press `Enter` or `d` to view details

### Quick navigation
1. Type your search query
2. Press `g` to jump to top result
3. Press `G` to jump to bottom result
4. Press `3` to jump directly to third result
