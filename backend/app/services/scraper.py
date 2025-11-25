import httpx
import re
from selectolax.parser import HTMLParser

async def fetch_page(url: str) -> str | None:
    """Fetch the HTML content of a webpage asynchronously."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
            if response.status_code == 200:
                return response.text
            return None
    except Exception:
        return None
    
def extract_price(html: str) -> float | None:
    """Extract the price from the HTML content using Selectolax."""
    
    tree = HTMLParser(html=html)
    
    # Scan for common price patterns
    price_regex = re.compile(r"[$€£₦]\s?[\d,]+(?:\.\d+)?")
    match = price_regex.search(tree.text())
    
    if match:
        price_str = match.group(0)
        # Clean and convert to float
        price_cleaned = re.sub(r"[^\d.]", "", price_str)
        try:
            return float(price_cleaned)
        except ValueError:
            return None
        
    # try DOM-based extraction if regex fails
    for cls in ["price", "current-price", "product-price", "amount", "cost"]:
        node = tree.css_first(f".{cls}")
        if node:
            price_text = node.text()
            price_cleaned = re.sub(r"[^\d.]", "", price_text)
            try:
                return float(price_cleaned)
            except ValueError:
                pass
            
    return None