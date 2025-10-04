from fastapi import FastAPI, Query
from typing import Optional
import uvicorn

app = FastAPI()

# Fake dataset: 100 products
PRODUCTS = [
    {"id": i, "name": f"Product {i}", "price": round(10 + i * 1.1, 2)}
    for i in range(1, 101)
]

# ------------------------
# 1. Limit-Offset Pagination
# ------------------------
@app.get("/products/limit-offset")
def get_products_limit_offset(
    limit: int = Query(10, ge=1, le=50, 
                       description="Number of items to return (max 50)"),
    offset: int = Query(0, ge=0, 
                        description="Number of items to skip")
):
    data = PRODUCTS[offset: offset + limit]
    return {
        "count": len(PRODUCTS),
        "limit": limit,
        "offset": offset,
        "next_offset": offset + limit if offset + limit < len(PRODUCTS) else None,
        "results": data
    }


# ------------------------
# 2. Cursor-Based Pagination
# ------------------------
@app.get("/products/cursor")
def get_products_cursor(
    cursor: Optional[int] = Query(None, 
                                  description="Last seen product ID"),
    limit: int = Query(10, ge=1, le=50, 
                       description="Number of items to return (max 50)")
):
    start_index = 0
    if cursor:
        # Cursor = the last seen product ID
        for i, product in enumerate(PRODUCTS):
            if product["id"] == cursor:
                start_index = i + 1
                break

    data = PRODUCTS[start_index:start_index + limit]
    next_cursor = data[-1]["id"] if data else None

    return {
        "count": len(PRODUCTS),
        "limit": limit,
        "cursor": cursor,
        "next_cursor": next_cursor,
        "results": data
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
