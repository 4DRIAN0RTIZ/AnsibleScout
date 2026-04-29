# AnsibleScout

Scout and discover Ansible modules instantly with fuzzy search and AI-powered semantic recommendations.

## Features

- **Real-time fuzzy search** as you type
- **AI Semantic Search** with embeddings (Ctrl+I) - finds modules by meaning, not just text
- **Vim-style keyboard navigation**
- **Split-panel interface**: results and details
- **Module details** with parameters and examples
- **Quick selection** with number keys (1-9)
- **Multiple color themes** (Original, Dracula)
- **Theme switching** with Ctrl+P

## AI Semantic Search (New!)

Ansible Scout now includes AI-powered semantic search using OpenAI embeddings:

- **Press `Ctrl+I`** to activate semantic search
- Understands synonyms and context: "backup" finds `mysql_db`, `archive`
- Works in multiple languages: "instalar" finds `package`, `apt`, `yum`
- **Cost**: ~$0.003 for 9,600+ modules (one-time on first run)
- Embeddings are cached locally after first generation

### Example AI Searches

| Query | Fuzzy Result | **Semantic Result (Ctrl+I)** |
|-------|--------------|------------------------------|
| "backup database" | copy, fetch | **mysql_db, postgresql_db, archive** |
| "install program" | template | **package, apt, yum, pip** |
| "check if file exists" | copy, file | **stat, find, file** |

## Installation

```bash
pip install -r requirements.txt
```

### Setup Configuration

Create config file at `~/.config/ascout/config.toml`:

```toml
[ui]
theme = "dracula"

[search]
limit = 10
results_display = 5

[ai]
# Enable or disable AI features
enabled = true
model = "gpt-4o-mini"
max_tokens = 500
# Add your OpenAI API key here (or set OPENAI_API_KEY env var)
api_key = "sk-your-api-key"

[ansible]
doc_timeout = 10
modules_file = "/tmp/ansible_modules.json"
```

## Usage

```bash
# Basic mode
./main.py

# With custom theme
./main.py --theme dracula

# Custom modules file location
./main.py --modules-file /path/to/modules.json
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

### AI Features
- `Ctrl+I` - **Semantic AI Search** with embeddings (manual trigger to save tokens)

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

### AI Semantic Search
1. Type "backup database" in the search box
2. Press `Ctrl+I` to activate AI semantic search
3. The AI will find modules like `mysql_db`, `postgresql_db`, `archive`
4. View AI recommendations and select the best module

### Quick navigation
1. Type your search query
2. Press `g` to jump to top result
3. Press `G` to jump to bottom result
4. Press `3` to jump directly to third result

## Requirements

- Python 3.8+
- OpenAI API key (for AI features)
- ~128MB disk space for embeddings cache (9,600+ modules)

## Cost Information

- **Embeddings generation** (first run): ~$0.003 USD
- **Each Ctrl+I search**: ~$0.0001 USD
- **Monthly usage** (100 searches/day): ~$0.30 USD
