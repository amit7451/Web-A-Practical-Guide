# 📖 HTML — A Practical Guide & Working Manuscript

A modern, interactive, tiered reference and learning manuscript for **HyperText Markup Language (HTML)** built from first principles to advanced browser APIs and Web Components.

![HTML Guide Preview](https://img.shields.io/badge/HTML5-Living_Standard-orange?style=for-the-badge&logo=html5)
![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
![Deployment](https://img.shields.io/badge/Deployment-GitHub_Pages-blue?style=for-the-badge&logo=github)

---

## ✨ Features

- **📚 Tiered Learning Curriculum:**
  - **Tier I: Beginner** — Core syntax, document outlines, text formatting, links, and image semantics.
  - **Tier II: Intermediate** — Tables, structured forms, audio/video media, and responsive images.
  - **Tier III: Advanced** — Accessible landmarks (ARIA), drag & drop, Web Components (`<template>`, Shadow DOM, Custom Elements), and storage APIs.
  - **Tier IV: Reference** — Complete HTML element sitemap, common anti-patterns & mistakes, and practice projects.
- **⚡ Interactive Search & Filtering:** Filter topics dynamically by title or keyword in real time.
- **✅ Progress Tracking & Persistence:** Mark topics as read with progress bars; progress automatically saves in browser `localStorage`.
- **💻 Syntax-Highlighted Code Blocks:** Copy runnable code examples directly with one-click clipboard copying.
- **⌨️ Keyboard Navigation:** Navigate between sequential topics seamlessly using `<Left>` and `<Right>` arrow keys.
- **📱 Fully Responsive Design:** Clean desktop dual-panel layout with a slide-out drawer on mobile devices.

---

## 📁 Repository Structure

```
Web-Guide/
├── .github/
│   └── workflows/
│       └── deploy.yml      # GitHub Actions automated deployment to GitHub Pages
├── css/
│   └── styles.css          # Core CSS design system & dark mode aesthetics
├── js/
│   └── app.js              # Interactive application logic & local storage handler
├── index.html              # Main website entry point
├── 404.html                # Custom 404 error page for static hosting
├── .gitignore              # Git ignore rules for clean repository state
└── README.md               # Repository documentation
```

---

## 🚀 Running Locally

Because **HTML — A Practical Guide** is built using native web standards (Vanilla HTML5, CSS3, and ES6 JavaScript), you do not need complex build tools or bundlers to run it locally.

### Option 1: Direct File Preview
Simply double-click [`index.html`](index.html) or open it directly in any standard browser (Chrome, Firefox, Safari, Edge).

### Option 2: Local HTTP Server (Recommended)
Running via a local HTTP server ensures full compatibility with browser APIs:

Using Node.js (`npx`):
```bash
npx serve .
```

Or using Python 3:
```bash
python -m http.server 8000
```
Then navigate to `http://localhost:8000` in your web browser.

---

## 🌐 Deploying to GitHub Pages

This repository is pre-configured for automated deployment to **GitHub Pages**.

### Method 1: Automatic Deployment (GitHub Actions - Recommended)
1. Push this repository to your GitHub account on the `main` branch.
2. In your GitHub repository, go to **Settings** → **Pages**.
3. Under **Build and deployment** → **Source**, select **GitHub Actions**.
4. Every push to `main` will automatically trigger `.github/workflows/deploy.yml` and publish your site!

### Method 2: Deploy from Branch
1. Go to **Settings** → **Pages**.
2. Under **Source**, select **Deploy from a branch**.
3. Select `main` branch and `/ (root)` folder, then click **Save**.

---

## 📝 License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute for learning and teaching purposes.
