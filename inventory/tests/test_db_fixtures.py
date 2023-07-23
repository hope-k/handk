

def test_inventory_category_fixture(
    db,
    category_factory,
):
    category = category_factory()
    assert category
