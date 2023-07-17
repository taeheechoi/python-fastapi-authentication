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


### Reference
- https://medium.com/python-in-plain-english/building-a-restful-api-with-fastapi-secure-signup-and-login-functionality-included-45cdbcb36106