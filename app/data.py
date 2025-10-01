"""Static data store for product prices across areas and stores."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class StorePrice:
    """Represents the price of a product in a specific store."""

    store_name: str
    price: float


@dataclass(frozen=True)
class ProductListing:
    """Represents a product available in an area with prices from different stores."""

    product_id: str
    name: str
    category: str
    prices: List[StorePrice]


# Demo dataset mimicking scraped price data grouped by area.
# In a real application these would likely come from a database or API.
AREAS: Dict[str, List[ProductListing]] = {
    "downtown": [
        ProductListing(
            product_id="coffee-beans-1kg",
            name="Premium Coffee Beans 1kg",
            category="Grocery",
            prices=[
                StorePrice(store_name="Bean Palace", price=17.5),
                StorePrice(store_name="SuperMart Central", price=16.99),
                StorePrice(store_name="Budget Grocers", price=15.75),
            ],
        ),
        ProductListing(
            product_id="almond-milk-1l",
            name="Organic Almond Milk 1L",
            category="Dairy Alternatives",
            prices=[
                StorePrice(store_name="SuperMart Central", price=4.69),
                StorePrice(store_name="Budget Grocers", price=3.99),
            ],
        ),
        ProductListing(
            product_id="dish-soap-500ml",
            name="Eco Dish Soap 500ml",
            category="Household",
            prices=[
                StorePrice(store_name="HomeEssentials", price=2.5),
                StorePrice(store_name="Budget Grocers", price=2.19),
            ],
        ),
    ],
    "uptown": [
        ProductListing(
            product_id="coffee-beans-1kg",
            name="Premium Coffee Beans 1kg",
            category="Grocery",
            prices=[
                StorePrice(store_name="Cafe Collective", price=18.0),
                StorePrice(store_name="Uptown Organics", price=17.25),
            ],
        ),
        ProductListing(
            product_id="oat-milk-1l",
            name="Oat Milk 1L",
            category="Dairy Alternatives",
            prices=[
                StorePrice(store_name="Uptown Organics", price=4.5),
                StorePrice(store_name="Healthy Harvest", price=4.35),
            ],
        ),
        ProductListing(
            product_id="granola-500g",
            name="Crunchy Granola 500g",
            category="Grocery",
            prices=[
                StorePrice(store_name="Healthy Harvest", price=5.95),
                StorePrice(store_name="SuperMart Uptown", price=5.5),
                StorePrice(store_name="Uptown Organics", price=5.75),
            ],
        ),
    ],
}
