from bustag.main import recommend


def test_recommend():
    count, recommend_count = recommend()
    assert count > 0
