# The @dataclass decorator reduces boilerplate code by automatically adding common methods like __init__, __repr__, and __eq__ based on the class attributes.
```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

p1 = Point(1, 2)
p2 = Point(1, 2)

print(p1)  # Output: Point(x=1, y=2)
print(p1 == p2)  # Output: True
```

get_calories_from_api()
``` python

[{'food_name': 'Big Mac', 'brand_name': "McDonald's", 'serving_qty': 1, 'serving_unit': 'Serving', 'serving_weight_grams': None, 'nf_metric_qty': 215, 'nf_metric_uom': 'g', 'nf_calories': 590, 'nf_total_fat': 34, 'nf_saturated_fat': 11, 'nf_cholesterol': 85, 'nf_sodium': 1050, 'nf_total_carbohydrate': 46, 'nf_dietary_fiber': 3, 'nf_sugars': 9, 'nf_protein': 25, 'nf_potassium': None, 'nf_p': None, 'full_nutrients': [{'attr_id': 203, 'value': 25}, {'attr_id': 204, 'value': 34}, {'attr_id': 205, 'value': 46}, {'attr_id': 208, 'value': 590}, {'attr_id': 269, 'value': 9}, {'attr_id': 291, 'value': 3}, {'attr_id': 307, 'value': 1050}, {'attr_id': 601, 'value': 85}, {'attr_id': 605, 'value': 1}, {'attr_id': 606, 'value': 11}], 'nix_brand_name': "McDonald's", 'nix_brand_id': '513fbc1283aa2dc80c000053', 'nix_item_name': 'Big Mac', 'nix_item_id': '513fc9e73fe3ffd40300109f', 'metadata': {}, 'source': 8, 'ndb_no': None, 'tags': None, 'alt_measures': None, 'lat': None, 'lng': None, 'photo': {'thumb': 'https://d2eawub7utcl6.cloudfront.net/images/nix-apple-grey.png', 'highres': None, 'is_user_uploaded': False}, 'note': None, 'class_code': None, 'brick_code': None, 'tag_id': None, 'updated_at': '2023-06-21T18:41:12+00:00', 'nf_ingredient_statement': None}]
```

### Reference
- https://medium.com/python-in-plain-english/building-a-restful-api-with-fastapi-secure-signup-and-login-functionality-included-45cdbcb36106