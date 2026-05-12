# 🗞️ Ekantipur Entertainment Scraper

> A browser automation script that extracts **top 5 entertainment news articles** and the **Cartoon of the Day** from [ekantipur.com](https://ekantipur.com) — saving structured, Nepali-encoded data to JSON.

---

## 👨‍💻 Author

| | |
|---|---|
| **Name** | Akisha Bhujel |

---

## ✨ Features

- 🎬 Scrapes **top 5 entertainment articles** from the मनोरञ्जन section
- 🖼️ Extracts article **title, image URL, category, and author**
- 🗺️ Dynamically resolves **category from URL** — no hardcoded values
- 🎨 Extracts **Cartoon of the Day** (title + image) from the homepage slider
- ⏳ Handles **lazy-loaded images** via scroll + attribute validation
- 🛡️ Graceful **error handling** for missing elements
- 💾 Outputs **valid JSON** with proper Nepali (Devanagari) encoding

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12+ | Core language |
| [Playwright](https://playwright.dev/python/) | Browser automation |
| `uv` | Fast Python package manager |
| `pathlib` | File I/O |
| `re` | URL/image validation via regex |
| `json` | Structured output |

---

## 📂 Project Structure

```
ekantipur-scraper/
├── scraper.py        # Main automation script
├── output.json       # Scraped output (auto-generated)
├── pyproject.toml    # Project metadata & dependencies
└── uv.lock           # Locked dependency versions
```

---

## ⚙️ Setup & Installation

### 1. Install `uv` (package manager)

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone & install dependencies

```bash
git clone https://github.com/akisavujel/ekantipur-scraper.git
cd ekantipur-scraper
uv sync
uv run playwright install chromium
```

---

## ▶️ Running the Scraper

```bash
uv run python scraper.py
```

The script will:
1. Navigate to `ekantipur.com/entertainment`
2. Extract the top 5 articles
3. Navigate to the homepage and extract the Cartoon of the Day
4. Print JSON to the terminal
5. Save output to `output.json`

---

## 📄 Output Format

```json
{
  "entertainment_news": [
    {
      "title": "Article headline in Nepali",
      "image_url": "https://assets-cdn.ekantipur.com/...",
      "category": "entertainment",
      "author": "लेखकको नाम"
    }
  ],
  "cartoon_of_the_day": {
    "title": "कार्टुनको शीर्षक",
    "image_url": "https://assets-cdn.ekantipur.com/...",
    "author": null
  }
}
```

---

## 🧠 How It Works

### Entertainment News
- Navigates to `/entertainment` and waits for `.category-inner-wrapper` cards to load
- Loops through the first 5 cards, extracting title, href, image, and author
- Scrolls each image into view before extraction to trigger lazy loading
- Validates image `src` against an `https://` regex before returning

### Cartoon of the Day
- Navigates to the homepage and waits for `.cartoon-slider .swiper-slide`
- Targets the `.swiper-slide-active` slide (falls back to the first slide)
- Extracts the image URL with a multi-step fallback chain: `src` → anchor `href`

---

## 🔍 Selector Strategy

Selectors were identified using browser DevTools (F12) on ekantipur.com:

| Data Point | Selector Used |
|---|---|
| Article cards | `.category-inner-wrapper` |
| Article title | `.category-description h2 a` |
| Article image | `.category-image img` |
| Article author | `.author-name a` |
| Cartoon slider | `.cartoon-slider .swiper-slide-active` |
| Cartoon image | `img` (within active slide) |

---

## ⚠️ Known Limitations

- Some articles may have `null` image URLs if images fail to load within the timeout window
- Cartoon author is not always available in the page markup (`null` returned)
- The site's structure may change over time, requiring selector updates

---

## 📚 What I Learned

- Playwright browser automation with Python
- Handling dynamic/lazy-loaded content on real-world news sites
- Structuring scraped data into clean JSON
- Using `uv` for modern Python project management
- Debugging selectors with DevTools on Devanagari-script websites
