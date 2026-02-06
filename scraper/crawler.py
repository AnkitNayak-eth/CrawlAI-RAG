from playwright.sync_api import sync_playwright
from urllib.parse import urljoin, urlparse
import time


# --------------------------------------------------
# Progressive scroll (lazy-load safe)
# --------------------------------------------------
def progressive_scroll(page):
    page.evaluate(
        """
        () => new Promise(resolve => {
            let y = 0;
            const step = 500;
            const interval = setInterval(() => {
                window.scrollBy(0, step);
                y += step;
                if (y >= document.body.scrollHeight) {
                    clearInterval(interval);
                    resolve();
                }
            }, 200);
        })
        """
    )


# --------------------------------------------------
# Wait until DOM stabilizes
# --------------------------------------------------
def wait_for_dom_stability(page, max_checks=10, delay_ms=700):
    last_len = 0
    stable_rounds = 0

    for _ in range(max_checks):
        text = page.evaluate("() => document.body.innerText.length")
        if abs(text - last_len) < 100:
            stable_rounds += 1
            if stable_rounds >= 3:
                return
        else:
            stable_rounds = 0

        last_len = text
        time.sleep(delay_ms / 1000)


# --------------------------------------------------
# EXACT Ctrl+A → Ctrl+C extractor
# --------------------------------------------------
def extract_like_ctrl_a_copy(page):
    return page.evaluate(
        """
        () => {
            const selection = window.getSelection();
            selection.removeAllRanges();

            const range = document.createRange();
            range.selectNodeContents(document.body);
            selection.addRange(range);

            return selection.toString();
        }
        """
    )


# --------------------------------------------------
# Main crawler (COPY-PASTE PERFECT)
# --------------------------------------------------
def crawl_website(start_url: str, max_pages: int = 20):
    visited = set()
    content_hashes = set()
    queue = [start_url]
    pages = []

    domain = urlparse(start_url).netloc

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        # Block heavy resources (safe)
        context.route(
            "**/*",
            lambda route, request: route.abort()
            if request.resource_type in ["image", "media", "font"]
            else route.continue_()
        )

        page = context.new_page()

        while queue and len(visited) < max_pages:
            url = queue.pop(0)
            parsed = urlparse(url)

            if parsed.netloc != domain:
                continue

            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if clean_url.endswith('/'):
                clean_url = clean_url[:-1]
            
            # Skip proxy URLs or external links disguised as internal
            if "medium.com" in clean_url or "http%3A" in clean_url or "https%3A" in clean_url:
                print(f"Skipping external/proxy URL: {clean_url}")
                visited.add(clean_url) # Mark as visited to avoid reprocessing
                continue

            if clean_url in visited:
                continue

            visited.add(clean_url)
            
            try:
                print(f"Crawling: {clean_url}")

                page.goto(clean_url, wait_until="networkidle", timeout=60000)
                page.wait_for_timeout(1000)
                
                # Force render everything
                progressive_scroll(page)
                wait_for_dom_stability(page)

                # 🔥 EXACT browser copy
                copied_text = extract_like_ctrl_a_copy(page)

                # Deduplication check
                import hashlib
                content_hash = hashlib.md5(copied_text.encode('utf-8')).hexdigest()
                if content_hash in content_hashes:
                    print(f"Skipping duplicate content: {clean_url}")
                    continue
                content_hashes.add(content_hash)
                
                # Collect internal links
                links = page.evaluate(
                    """
                    () => {
                        const links = Array.from(document.querySelectorAll('a[href]'));
                        return links.map(a => ({
                            text: a.innerText.trim(),
                            href: a.href,
                            label: a.getAttribute('aria-label') || a.getAttribute('title') || ''
                        }));
                    }
                    """
                )

                # Format links and append to content
                links_text = "\n\nLinks Found:\n"
                unique_links = set()
                
                # For crawling queue
                internal_links = []

                for link in links:
                    href = link['href']
                    text = link['text']
                    label = link['label']
                    
                    # Use label/title if text is empty (common for icons)
                    display_text = text if text else label
                    
                    # Dynamic fallback: Extract domain from URL if no text/label
                    if not display_text:
                        try:
                            parsed_href = urlparse(href)
                            domain_parts = parsed_href.netloc.split('.')
                            # Handle cases like "www.linkedin.com" -> "linkedin" or "x.com" -> "x"
                            if len(domain_parts) >= 2:
                                # Get the main domain name (e.g. 'linkedin' from 'www.linkedin.com')
                                # Simple heuristic: take the part before the TLD
                                domain_name = domain_parts[-2] if domain_parts[-2] not in ['www', 'web'] else domain_parts[-3]
                                display_text = domain_name.capitalize()
                            else:
                                display_text = parsed_href.netloc.capitalize()
                        except Exception:
                            pass
                    
                    # Add to displayed content if we have some identifier
                    if display_text:
                        full_link_str = f"[{display_text}]({href})"
                        if full_link_str not in unique_links:
                            links_text += f"- {full_link_str}\n"
                            unique_links.add(full_link_str)
                    
                    # Collect internal links for crawling
                    internal_links.append(href)

                if copied_text.strip():
                    final_content = (
                        f"URL: {clean_url}\n"
                        f"CONTENT (Ctrl+A → Ctrl+C):\n"
                        f"{copied_text}\n"
                        f"{links_text}"
                    )
                    pages.append(final_content)

                for href in internal_links:
                    p2 = urlparse(href)
                    if p2.netloc == domain:
                        next_url = f"{p2.scheme}://{p2.netloc}{p2.path}"
                        if next_url.endswith('/'):
                            next_url = next_url[:-1]
                        if next_url not in visited:
                            queue.append(next_url)

            except Exception as e:
                print(f"Failed {clean_url}: {e}")

        browser.close()

    return pages
