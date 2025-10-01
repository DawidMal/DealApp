"""FastAPI application exposing product price comparisons across stores."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException

from .services import AreaNotFoundError, find_product, get_available_areas, summarize_cheapest_products

app = FastAPI(title="Deal Finder", description="Compare store prices per area", version="0.1.0")


@app.get("/areas")
def list_areas() -> dict:
    """Return available areas for which product data exists."""

    return {"areas": get_available_areas()}


@app.get("/areas/{area}/products")
def get_products(area: str) -> dict:
    """Return products in an area with their cheapest price information."""

    try:
        products = summarize_cheapest_products(area)
    except AreaNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"area": area.lower(), "products": products}


@app.get("/areas/{area}/products/{product_id}")
def get_product(area: str, product_id: str) -> dict:
    """Return cheapest price details for a specific product in an area."""

    try:
        product = find_product(area, product_id)
    except AreaNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found in area '{area}'")
    return product
