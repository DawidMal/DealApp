"""Business logic for aggregating product prices across stores."""
from __future__ import annotations

from dataclasses import asdict
from typing import Dict, Iterable, List, Optional

from .data import AREAS, ProductListing, StorePrice


class AreaNotFoundError(KeyError):
    """Raised when an area is not available in the dataset."""


def get_available_areas() -> List[str]:
    """Return the list of available areas that contain store data."""

    return sorted(AREAS.keys())


def _cheapest_price(prices: Iterable[StorePrice]) -> StorePrice:
    try:
        return min(prices, key=lambda price: price.price)
    except ValueError as exc:
        raise ValueError("Cannot determine cheapest price from an empty list") from exc


def get_products_for_area(area: str) -> List[ProductListing]:
    """Retrieve all product listings for a given area.

    Args:
        area: Area identifier.

    Raises:
        AreaNotFoundError: If the area is not known.
    """

    try:
        return AREAS[area.lower()]
    except KeyError as exc:
        raise AreaNotFoundError(f"Unknown area: {area}") from exc


def summarize_cheapest_products(area: str) -> List[Dict[str, object]]:
    """Return summary data for the cheapest price of each product in an area."""

    listings = get_products_for_area(area)

    summary: List[Dict[str, object]] = []
    for listing in listings:
        cheapest = _cheapest_price(listing.prices)
        summary.append(
            {
                "product_id": listing.product_id,
                "name": listing.name,
                "category": listing.category,
                "cheapest_price": cheapest.price,
                "cheapest_store": cheapest.store_name,
                "stores": [asdict(price) for price in listing.prices],
            }
        )
    return summary


def find_product(area: str, product_id: str) -> Optional[Dict[str, object]]:
    """Find a specific product in an area and return its cheapest price summary."""

    listings = get_products_for_area(area)
    for listing in listings:
        if listing.product_id == product_id:
            cheapest = _cheapest_price(listing.prices)
            return {
                "product_id": listing.product_id,
                "name": listing.name,
                "category": listing.category,
                "cheapest_price": cheapest.price,
                "cheapest_store": cheapest.store_name,
                "stores": [asdict(price) for price in listing.prices],
            }
    return None
