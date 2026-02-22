# Study Hub

A beautiful, config-driven study platform for deep-diving into software engineering topics. Built as a single-page app with zero dependencies — just HTML, CSS, and vanilla JS.

**Live:** [https://sarankumar18.github.io/study-hub](https://sarankumar18.github.io/study-hub)

## Topics

| Topic | Documents | Focus |
|-------|-----------|-------|
| **Java Internals** | 7 | JVM, concurrency, I/O, JDBC deep dives |
| **System Design** | 9 | Networking, protocols, databases, caching, microservices |
| **Operating Systems** | 5 | Processes, memory management, file systems |

## Features

- **Multi-topic support** — switch between topics with one click
- **Progress tracking** — mark sections as done, track per-doc and per-topic progress (saved in localStorage)
- **Cross-topic search** — search across all topics simultaneously
- **Code copy buttons** — one-click copy on every code block
- **Reading time estimates** — per-document reading time
- **Scroll progress bar** — visual indicator at the top of the page
- **Table of contents** — auto-generated, scrollspy-highlighted
- **Keyboard shortcuts** — `/` to search, `Esc` to close, arrow keys to navigate
- **Mobile responsive** — hamburger menu with slide-out sidebar
- **Dark theme** — easy on the eyes for long study sessions

## Running Locally

```bash
# Clone the repo
git clone https://github.com/Sarankumar18/study-hub.git
cd study-hub

# Start a local server (Python 3)
python3 -m http.server 3000

# Open in browser
open http://localhost:3000
```

## Adding a New Topic

Edit `index.html` and add an entry to the `TOPICS` array:

```javascript
{
  id: 'my-topic',
  title: 'My Topic',
  subtitle: 'Short description',
  icon: 'M',
  color: '#e879f9',
  basePath: 'my-topic/',
  documents: [
    { id: 'roadmap', title: 'Roadmap', icon: 'R', file: 'MY-ROADMAP.md' },
    { id: '00', title: 'Phase 0 — Basics', icon: '0', file: 'internals/00-basics.md' },
  ],
},
```

Then add your markdown files to `my-topic/`. That's it — the UI, progress, and search all wire up automatically.

## Tech

- Single `index.html` — no build step, no framework
- [marked.js](https://github.com/markedjs/marked) for Markdown rendering
- [highlight.js](https://highlightjs.org/) for syntax highlighting
- GitHub Pages for hosting
