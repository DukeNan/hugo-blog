# Hugo Blog

A multilingual personal blog built with [Hugo](https://gohugo.io/) static site generator, using the [hugo-clarity](https://github.com/chipzoller/hugo-clarity) theme. The blog is deployed via nginx with an automated deployment workflow.

## Features

- **Multilingual Support**: English (default), Chinese (zh-CN), and Portuguese
- **Clean Design**: Modern, responsive layout based on hugo-clarity theme
- **Syntax Highlighting**: Code blocks with line numbers and copy button
- **SEO Friendly**: Meta descriptions, Open Graph tags, and structured data
- **Fast Performance**: Static HTML generation with minification
- **Easy Deployment**: Automated deployment script with nginx reload

## Quick Start

### Prerequisites

- [Hugo](https://gohugo.io/installation/) (extended version recommended)
- Git

### Installation

```bash
# Clone the repository
git clone --recurse-submodules https://github.com/yourusername/hugo-blog.git
cd hugo-blog

# If you already cloned without --recurse-submodules
git submodule update --init --recursive

# Start development server
hugo server

# Build the site
hugo --minify
```

The site will be available at `http://localhost:1313` in development mode.

## Project Structure

```
hugo-blog/
├── config/              # Configuration files
│   └── _default/       # Default configuration
│       ├── config.toml       # Core Hugo settings
│       ├── params.toml       # Theme parameters
│       ├── languages.toml    # Multilingual settings
│       ├── configTaxo.toml   # Taxonomy configuration
│       ├── markup.toml       # Markdown/Goldmark settings
│       └── menus/            # Menu configurations per language
├── content/             # Site content
│   ├── post/           # Blog posts
│   └── homepage/       # Homepage-specific content
├── layouts/             # Custom layout overrides
│   └── shortcodes/     # Custom shortcodes
├── static/              # Static assets (images, icons, fonts)
├── themes/              # Hugo themes
│   └── hugo-clarity/   # Clarity theme (git submodule)
├── archetypes/          # Content templates
├── assets/              # Asset pipeline files
├── resources/           # Generated resources
├── public/              # Built site output (not in version control)
├── deploy.sh            # Deployment script
└── CLAUDE.md           # Project instructions for AI assistants
```

## Creating New Content

### Create a New Post

```bash
# Create a new post using the archetype
hugo new post/my-new-post.md
```

This creates a new markdown file in `content/post/` with front matter pre-populated from the archetype template.

### Front Matter Example

```yaml
---
title: "Post Title"
date: 2026-01-12T09:47:06+08:00
description: "A brief description for search engines"
author: "shaun"
featured: true
draft: true
toc: true
categories:
  - Technology
tags:
  - Git
  - Tutorial
---
```

### Publishing a Post

1. Set `draft: false` in the front matter
2. Build the site: `hugo --minify`
3. Deploy (if using automated deployment)

## Configuration

### Multilingual Setup

The blog supports three languages configured in `config/_default/languages.toml`:

- **English** (default): `en`
- **Chinese**: `zh-cn`
- **Portuguese**: `pt`

Key multilingual settings in `config/_default/config.toml`:

```toml
DefaultContentLanguage = "en"
hasCJKLanguage = true  # Proper word counting for Chinese/Japanese/Korean
```

### Theme Configuration

The [hugo-clarity](https://github.com/chipzoller/hugo-clarity) theme is managed as a git submodule:

```bash
# Check submodule status
git submodule status

# Update theme to latest version
git submodule update --remote --merge

# Sync submodule URLs
git submodule sync
```

### Customization

Customize the site by editing:

- **`config/_default/config.toml`**: Base URL, copyright, theme selection
- **`config/_default/params.toml`**: Theme-specific parameters
- **`config/_default/menus/`**: Navigation menus for each language
- **`layouts/`**: Override theme templates (currently minimal)
- **`static/`**: Add custom static assets

## Deployment

### Manual Deployment

```bash
# Build the site
hugo --minify

# The output is in the `public/` directory
# Deploy the contents of `public/` to your web server
```

### Automated Deployment

The project includes a deployment script that:

1. Pulls the latest changes from git
2. Builds the site with Hugo
3. Reloads the nginx server

```bash
# Run the deployment script
./deploy.sh
```

**Note**: Ensure nginx is properly configured to serve from the `public/` directory.

### CI/CD Integration

For automated deployment with GitHub Actions or similar CI/CD platforms:

```yaml
# Example: GitHub Actions workflow
- name: Checkout repository
  uses: actions/checkout@v3
  with:
    submodules: recursive  # Important for theme submodule

- name: Setup Hugo
  uses: peaceiris/actions-hugo@v2
  with:
    hugo-version: 'latest'

- name: Build site
  run: hugo --minify

- name: Deploy
  # Add your deployment step here
```

## Git Submodule Management

This project uses git submodules for theme management. When cloning:

```bash
# Clone with submodules
git clone --recurse-submodules https://github.com/yourusername/hugo-blog.git

# Or initialize after cloning
git submodule update --init --recursive
```

Common submodule operations:

```bash
# Update all submodules
git submodule update --remote --merge

# Check submodule status
git submodule status

# Remove a submodule (if needed)
git submodule deinit themes/hugo-clarity
git rm themes/hugo-clarity
```

## Development Workflow

### Local Development

```bash
# Start development server with draft posts
hugo server -D

# Start with specific port
hugo server --port 1313

# Build to production
hugo --minify
```

### Commit Convention

Follow conventional commit format:

- `docs(scope):` - Documentation changes
- `feat(scope):` - New features
- `fix(scope):` - Bug fixes
- `chore(scope):` - Maintenance tasks

Examples:

```bash
git commit -m "docs(post/git): add Git Submodule complete guide"
git commit -m "fix(config): update base URL for production"
git commit -m "feat(theme): add custom shortcode for videos"
```

## Theme Customization Strategy

The project keeps custom layouts minimal to simplify theme updates:

- **Use `config/_default/params.toml`** for theme configuration
- **Override in `layouts/`** only when necessary
- **Keep the theme as a submodule** for easy updates
- **Document custom changes** in `CLAUDE.md`

## Useful Resources

- [Hugo Documentation](https://gohugo.io/documentation/)
- [hugo-clarity Theme](https://github.com/chipzoller/hugo-clarity)
- [Hugo Forums](https://discourse.gohugo.io/)
- [Markdown Syntax Guide](https://www.markdownguide.org/)

## License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

## Author

**Shaun** - [https://www.dukenan.top](https://www.dukenan.top)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

For more detailed project instructions, see [CLAUDE.md](CLAUDE.md).
