import json
import re
from pathlib import Path

from playwright.sync_api import expect, sync_playwright


# ---------------------------------
# Extract category dynamically from URL
# Example:
# https://ekantipur.com/entertainment/...
# → entertainment
# ---------------------------------
def category_from_href(href: str | None) -> str:
    if not href:
        return "unknown"

    try:
        parts = href.split("/")
        return parts[3] if len(parts) > 3 else "unknown"
    except:
        return "unknown"


# ---------------------------------
# Extract image from entertainment card
# Handles lazy-loaded images safely
# ---------------------------------
def image_url_from_card(card) -> str | None:
    img = card.locator(".category-image img").first
    img.scroll_into_view_if_needed()

    try:
        # wait until image src is valid URL
        expect(img).to_have_attribute("src", re.compile(r"^https?://"), timeout=15000)
        return img.get_attribute("src")
    except Exception:
        # fallback if image already loaded
        return img.get_attribute("src") or None


# ---------------------------------
# Extract cartoon image from homepage slider
# ---------------------------------
def cartoon_image_url(slide) -> str | None:
    slide.scroll_into_view_if_needed()
    img = slide.locator("img").first

    try:
        expect(img).to_have_attribute("src", re.compile(r"^https?://"), timeout=15000)
        src = img.get_attribute("src")
        if src:
            return src
    except Exception:
        pass

    # fallback method
    src = img.get_attribute("src")
    if src and src.startswith("http"):
        return src

    # another fallback for loading links
    a = slide.locator("a.loading-img")
    if a.count() > 0:
        href = a.first.get_attribute("href")
        if href and href.startswith("http"):
            return href

    return None


# ---------------------------------
# MAIN SCRAPER FUNCTION
# ---------------------------------
def main() -> None:
    out_path = Path("output.json")

    with sync_playwright() as p:
        # launch browser in headless mode
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_default_timeout(60000)

        # =========================
        # STEP 1: ENTERTAINMENT NEWS
        # =========================
        page.goto("https://ekantipur.com/entertainment", wait_until="domcontentloaded")
        page.wait_for_selector(".category-inner-wrapper", timeout=30000)

        cards = page.locator(".category-inner-wrapper")
        total = cards.count()
        n = min(5, total)

        entertainment_news = []

        for i in range(n):
            card = cards.nth(i)

            # extract title
            title_a = card.locator(".category-description h2 a").first
            title = title_a.inner_text().strip()

            # extract article link
            href = title_a.get_attribute("href")

            # extract image
            image_url = image_url_from_card(card)

            # extract author if available
            author_loc = card.locator(".author-name a")
            author = (
                author_loc.first.inner_text().strip()
                if author_loc.count() > 0
                else None
            )

            # store article data
            entertainment_news.append({
                "title": title,
                "image_url": image_url,
                "category": category_from_href(href),
                "author": author,
            })

        # =========================
        # STEP 2: CARTOON OF THE DAY
        # =========================
        page.goto("https://ekantipur.com", wait_until="domcontentloaded")
        page.wait_for_selector(".cartoon-slider .swiper-slide", timeout=30000)

        # get active slide
        active = page.locator(".cartoon-slider .swiper-slide-active")
        slide = active.first if active.count() > 0 else page.locator(".swiper-slide").first

        # cartoon title (alt text)
        img = slide.locator("img").first
        alt = (img.get_attribute("alt") or "").strip()

        # cartoon data
        cartoon_of_the_day = {
            "title": alt or None,
            "image_url": cartoon_image_url(slide),
            "author": None,  # not always available on site
        }

        # =========================
        # FINAL OUTPUT STRUCTURE
        # =========================
        payload = {
            "entertainment_news": entertainment_news,
            "cartoon_of_the_day": cartoon_of_the_day,
        }

        # convert to JSON
        text = json.dumps(payload, ensure_ascii=False, indent=2)

        # print output in terminal
        print(text)

        # save to file
        out_path.write_text(text, encoding="utf-8")

        browser.close()


# run script
if __name__ == "__main__":
    main()
