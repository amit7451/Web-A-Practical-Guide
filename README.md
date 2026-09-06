# 📖 Web Guides — Practical Learning Manuscripts

A modern, interactive, tiered reference and learning manuscript series for modern web craftsmanship: **HTML — A Practical Guide**, **CSS — A Working Style Sheet**, and **JavaScript — A Working Script**, built from first principles to advanced browser APIs, layout architectures, asynchronous systems, and Web Components.

![HTML5](https://img.shields.io/badge/HTML5-Living_Standard-orange?style=for-the-badge&logo=html5)
![CSS3](https://img.shields.io/badge/CSS3-Modern_Specs-blue?style=for-the-badge&logo=css3)
![JavaScript](https://img.shields.io/badge/JavaScript-ES2024%2FES6%2B-yellow?style=for-the-badge&logo=javascript)
![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
![Deployment](https://img.shields.io/badge/Deployment-GitHub_Pages-blue?style=for-the-badge&logo=github)

---

## ✨ Features

- **🏛️ Trio Curriculum Paths (96 Topics Total):**
  - **HTML Guide (`html-guide/`):** 28 sequential topics covering semantic outlines, form validation, accessible media, Shadow DOM, Custom Elements, and storage APIs.
  - **CSS Guide (`css-guide/`):** 32 sequential topics covering cascade mechanics, the box model, Flexbox, CSS Grid, custom properties, container queries, cascade layers, and animation.
  - **JS Guide (`js-guide/`):** 36 sequential topics covering variables, DOM manipulation, closures, event loop, promises, async/await, prototypes, browser APIs, design patterns, and engineering testing.
- **📚 Tiered Learning Curriculum:**
  - **Tier I: Beginner** — Syntax, selectors, box model, outlines, and fundamental units.
  - **Tier II: Intermediate** — Responsive layouts, forms, media queries, flexbox, closures, and async patterns.
  - **Tier III: Advanced** — Web Components, Shadow DOM, container queries, prototypal inheritance, and storage.
  - **Tier IV: Reference** — Complete sitemaps, technical interview banks, common anti-patterns & debugging best practices.
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
│       └── deploy.yml          # GitHub Actions automated deployment to GitHub Pages
├── css/
│   └── styles.css              # Core design system, portal styles & syntax highlighting
├── js/
│   └── app.js                  # HTML guide application logic & local storage handler
├── html-guide/
│   └── index.html              # HTML Practical Guide manuscript
├── css-guide/
│   ├── index.html              # CSS Practical Guide manuscript (main entry)
│   └── css-guide.html          # Secondary entry satisfying direct file requests
├── js-guide/
│   ├── index.html              # JavaScript Practical Guide manuscript (main entry)
│   └── js-guide.html           # Secondary entry satisfying direct file requests
├── index.html                  # Main Home Portal entry page (links to all guides)
├── js-guide.html               # Backwards-compatible canonical redirect forwarder
├── 404.html                    # Custom 404 error page with multi-guide routing
├── .gitignore                  # Git ignore rules for clean repository state
└── README.md                   # Repository documentation
```

---

## 🚀 Running Locally

Because **Web Guides** is built using native web standards (Vanilla HTML5, CSS3, and ES6 JavaScript), you do not need complex build tools or bundlers to run it locally.

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
