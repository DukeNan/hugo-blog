# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a multilingual Hugo blog using the [hugo-clarity](https://github.com/chipzoller/hugo-clarity) theme (managed as a git submodule). The site is deployed via nginx with an automated deployment script.

## Common Commands

### Development
```bash
hugo server              # Start local development server (http://localhost:1313)
hugo                     # Build site to ./public/
hugo --minify            # Build with minification (production)
```

### Deployment
```bash
./deploy.sh              # Full deployment: git pull → build → nginx reload
```

### Creating New Posts
```bash
hugo new post/my-post.md  # Create post using archetype (starts as draft)
```

### Autotree Shortcode
```bash
# Add code files to assets/code/<dir>/
mkdir -p assets/code/my-scripts
# Add your code files...

# Generate filetree index
python3 scripts/generate_filetree.py

# Use in markdown
# {{</* autotree dir="my-scripts" */>}}
```

## Architecture

### Directory Structure
- `content/post/` - Blog posts (main content)
- `content/homepage/` - Headless bundle for homepage-specific content
- `config/_default/` - Modular configuration split by purpose
  - `config.toml` - Core Hugo settings (baseurl, theme, pagination, taxonomies)
  - `params.toml` - Theme-specific parameters
  - `languages.toml` - Multilingual configuration
  - `configTaxo.toml` - Taxonomy and privacy settings
  - `markup.toml` - Markdown/Goldmark configuration
  - `menu.*.toml` - Language-specific menu configurations
- `layouts/` - Custom layout overrides
  - `layouts/shortcodes/` - Custom shortcodes (autotree, notice)
- `static/` - Static assets (images, icons, fonts)
- `scripts/` - Utility scripts
  - `generate_filetree.py` - Generates YAML data for autotree shortcode
- `assets/code/` - Code files for autotree shortcode display
- `assets/sass/` - Custom SASS styles
  - `_custom.sass` - Custom styles including autotree component
- `themes/hugo-clarity/` - Git submodule for the theme
- `public/` - Generated site output (not in version control)
- `data/` - Generated data (gitignored)

### Theme Customization Strategy
The project uses git submodules for theme management. Customize via:
- `config/_default/params.toml` - Theme configuration
- `layouts/` - Override specific templates only when needed
- `assets/sass/_custom.sass` - Custom SASS styles for theme extensions

### Multilingual Setup
Configured for English (default), Chinese (zh-CN), and Portuguese (pt). Key settings:
- `hasCJKLanguage = true` in config.toml for proper Chinese/Japanese/Korean word counting
- Separate menu files per language: `menu.en.toml`, `menu.zh-cn.toml`, `menu.pt.toml`
- Language-switching enabled

### Content Front Matter Pattern
Posts use consistent front matter (see `archetypes/post.md`):
- draft: true (by default)
- title, date, description, author
- categories, tags, series (for related content)
- Feature image, thumbnail, share image
- Code display settings (toc, codeCopyButton)

## Custom Shortcodes

### Autotree Shortcode
Displays an interactive file tree with expandable file contents and syntax highlighting.

**Usage in markdown:**
```markdown
{{</* autotree dir="scripts" */>}}
```

**Workflow:**
1. Add code files to `assets/code/<dir>/`
2. Run `python3 scripts/generate_filetree.py` to generate YAML index
3. Use shortcode in markdown with `dir` parameter
4. The shortcode reads from `data/filetrees/<dir>.yaml` (generated, gitignored)

**Features:**
- Automatic ASCII tree structure generation
- Click to expand/collapse file contents
- Syntax highlighting for 20+ languages
- Light/dark theme support
- Responsive design with keyboard accessibility

### Notice Shortcode
Displays styled informational boxes.

**Usage in markdown:**
```markdown
{{</* notice info */>}}
This is an informational notice.
{{</* /notice */>}}

{{</* notice warning */>}}
This is a warning notice.
{{</* /notice */>}}
```

## Git Submodule

Theme is managed as a submodule:
```bash
git submodule status                     # Check submodule status
git submodule update --remote --merge    # Update theme to latest
```

## Dependencies

### Python Dependencies
```bash
pip3 install pyyaml    # Required for autotree shortcode
```

## Deployment

The deployment script automatically runs the filetree generator before building:
```bash
./deploy.sh    # Full deployment: git pull → generate filetree → build → nginx reload
```

## Commit Conventions

Recent commits follow conventional commit format:
- `docs(scope):` - Documentation changes
- `feat(scope):` - New features
- `fix(scope):` - Bug fixes
- `chore(scope):` - Maintenance tasks

Examples from history:
- `docs(post/linux): add UFW guide with setup steps and common rules`
- `docs(go): add test usage documentation`
- `chore(config): update config files`
- `feat(shortcodes): add autotree and notice shortcodes with file tree generation`
- `fix(shortcodes): prevent duplicate event binding in autotree`
- `docs(hugo): add autotree shortcode documentation with example scripts`
