from app import services


def test_get_available_areas_sorted():
    areas = services.get_available_areas()
    assert areas == sorted(areas)


def test_summarize_cheapest_products_returns_expected_shape():
    summary = services.summarize_cheapest_products("downtown")
    assert summary, "Expected at least one product"
    first = summary[0]
    assert {"product_id", "name", "category", "cheapest_price", "cheapest_store", "stores"} <= first.keys()


def test_find_product_returns_cheapest_details():
    product = services.find_product("downtown", "almond-milk-1l")
    assert product is not None
    assert product["cheapest_store"] == "Budget Grocers"
    assert product["cheapest_price"] == 3.99


def test_find_product_missing_returns_none():
    product = services.find_product("downtown", "non-existent")
    assert product is None


def test_unknown_area_raises():
    try:
        services.get_products_for_area("unknown")
    except services.AreaNotFoundError as exc:
        assert "Unknown area" in str(exc)
    else:
        raise AssertionError("Expected AreaNotFoundError for unknown area")
