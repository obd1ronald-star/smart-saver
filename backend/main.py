from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Smart Saver backend is running 🚀"
    }

@app.get("/test")
def test():
    return {
        "status": "ok",
        "store": "Walmart",
        "example_product": "Lactaid Whole Milk",
        "price": 4.99,
        "delivery": "Free"
    }
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow your Lovable site (later) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later we’ll restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Smart Saver backend is running 🚀"}

@app.get("/test")
def test():
    return {
        "status": "ok",
        "store": "Walmart",
        "example_product": "Lactaid Whole Milk",
        "price": 4.99,
        "delivery": "Free",
    }

@app.get("/search")
def search(query: str = Query(..., min_length=2)):
    """
    MVP v0: Mock results (fake data).
    Next: replace mock with real store prices.
    """
    mock_results = [
        {
            "store": "Walmart",
            "product": "Lactaid Whole Milk, 64 fl oz",
            "price": 4.99,
            "unit": "64 fl oz",
            "delivery": "Free",
            "coupon": None,
        },
        {
            "store": "Amazon",
            "product": "Lactaid Whole Milk, 64 fl oz",
            "price": 5.49,
            "unit": "64 fl oz",
            "delivery": "Free",
            "coupon": "Save $0.50 (mock)",
        },
        {
            "store": "ShopRite",
            "product": "Lactaid Whole Milk, 64 fl oz",
            "price": 4.79,
            "unit": "64 fl oz",
            "delivery": "Pickup",
            "coupon": "Digital coupon (mock)",
        },
    ]

    best = min(mock_results, key=lambda x: x["price"])

    return {
        "query": query,
        "best": best,
        "results": mock_results,
    }
import urllib.parse

def shoprite_links(query: str) -> dict:
    q = urllib.parse.quote_plus(query)
    return {
        "search": f"https://www.shoprite.com/results?q={q}",
        "circular": "https://www.shoprite.com/circulars",
        "coupons": "https://www.shoprite.com/digital-coupon",
        "promotions": "https://www.shoprite.com/Promotions",
    }
sr = shoprite_links(query)

shoprite_result = {
    "store": "ShopRite",
    "product": f'ShopRite results for "{query}"',
    "price": None,
    "unit": None,
    "delivery": "Pickup (store-specific)",
    "coupon": "See ShopRite digital coupons / circular",
    "links": sr,
    "note": "ShopRite pricing varies by store; use links for current deals."
}

results.append(shoprite_result)