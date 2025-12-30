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
- `layouts/` - Custom layout overrides (currently minimal - only empty shortcodes dir)
- `static/` - Static assets (images, icons, fonts)
- `themes/hugo-clarity/` - Git submodule for the theme
- `public/` - Generated site output (not in version control)

### Theme Customization Strategy
The project uses git submodules for theme management, keeping custom layouts minimal (`layouts/shortcodes/.gitkeep`). This approach allows painless theme updates. Customize via:
- `config/_default/params.toml` - Theme configuration
- `layouts/` - Override specific templates only when needed

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

### Git Submodule
Theme is managed as a submodule:
```bash
git submodule status                     # Check submodule status
git submodule update --remote --merge    # Update theme to latest
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
