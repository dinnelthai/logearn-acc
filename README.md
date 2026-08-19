# LogEarn Knowledge Base

Static bilingual knowledge base. Serve the repository through an HTTP server; full-text search uses generated JSON indexes and does not run directly from `file://` URLs.

## Content workflow

1. Edit the Chinese and English HTML pages.
2. Put screenshots in `shots/` and reference them as files; do not embed base64 images.
3. Rebuild search and run checks:

```bash
python3 build_search.py
python3 check_site.py
```

For a local preview:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/`.
