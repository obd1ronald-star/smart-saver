from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import urllib.parse

app = FastAPI(title="Smart Saver API")

# Allow browser apps (Lovable) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to your Lovable domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def shoprite_links(query: str) -> dict:
    q = urllib.parse.quote_plus(query)
    return {
        "search": f"https://www.shoprite.com/results?q={q}",
        "circular": "https://www.shoprite.com/circulars",
        "coupons": "https://www.shoprite.com/digital-coupon",
        "promotions": "https://www.shoprite.com/Promotions",
    }

@app.get("/")
def root():
    return {"message": "Smart Saver backend is running 🚀"}

@app.get("/test")
def test():
    return {"status": "ok"}

@app.get("/search")
def search(query: str = Query(..., min_length=2)):
    """
    MVP v0:
    - Walmart/Amazon: mock prices (for now)
    - ShopRite: safe link-outs to circular/coupons/search
    """
    results = [
        {
            "store": "Walmart",
            "product": f'{query} (mock)',
            "price": 4.99,
            "unit": None,
            "delivery": "Free",
            "coupon": None,
        },
        {
            "store": "Amazon",
            "product": f'{query} (mock)',
            "price": 5.49,
            "unit": None,
            "delivery": "Free",
            "coupon": "Save $0.50 (mock)",
        },
        {
            "store": "ShopRite",
            "product": f'ShopRite results for "{query}"',
            "price": None,
            "unit": None,
            "delivery": "In-store / pickup (store-specific)",
            "coupon": "Check digital coupons & circular",
            "links": shoprite_links(query),
            "note": "ShopRite pricing varies by location. Use links for current deals.",
        },
    ]

    # Best deal = lowest numeric price only (ignores ShopRite price=None)
    priced = [r for r in results if isinstance(r.get("price"), (int, float))]
    best = min(priced, key=lambda r: r["price"]) if priced else None

    return {"query": query, "best": best, "results": results}
