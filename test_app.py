from app import app, df


def client():
    app.config.update(TESTING=True)
    return app.test_client()


def test_health_check():
    response = client().get("/api/health")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ok"
    assert payload["items"] == len(df)


def test_search_returns_expected_contract():
    response = client().get("/api/search")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["count"] == len(df)
    assert isinstance(payload["data"], list)
    assert payload["data"]
    assert set(payload["data"][0]) == {"餐廳區域", "店家", "餐點", "價格", "營業時間"}


def test_budget_filter_and_sort():
    response = client().get("/api/search?budget=80&sort=price_asc")
    assert response.status_code == 200
    payload = response.get_json()
    prices = [item["價格"] for item in payload["data"]]
    assert all(price <= 80 for price in prices)
    assert prices == sorted(prices)


def test_invalid_budget_returns_400():
    response = client().get("/api/search?budget=-1")
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_keyword_search_is_literal_and_safe():
    response = client().get("/api/search?keyword=%5B")
    assert response.status_code == 200
    payload = response.get_json()
    assert "count" in payload
    assert "data" in payload
