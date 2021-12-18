
# return map(itemgetter_default(*self.items_of_interest, default=self.default), items)

# def itemgetter_default(*attrs, **kwargs):
#     default = kwargs.pop('default', None)
#     if kwargs:
#         raise TypeError(f"itemgetter_default() got unexpected keyword argument(s): %r", sorted(kwargs))
#
#     def fn(item):
#         getter = lambda attr: item.get(attr, default)
#         return tuple(map(getter, attrs))
#
#     return fn

# class Number(object):
#
#     def __init__(self, minval=None, maxval=None):
#         self.minval = minval
#         self.maxval = maxval
#
#     def __set_name__(self, owner, name):
#         self.private_name = f'_{name}'
#
#     def __get__(self, instance, owner):
#         return getattr(instance, self.private_name)
#
#     def __set__(self, instance, value):
#         self.validate(value)
#         setattr(instance, self.private_name, value)
#
#     def validate(self, value):
#         if not isinstance(value, int):
#             raise TypeError(f"Expected {value!r} to be and int")
#         if self.minval is not None and value < self.minval:
#             raise ValueError(f"Expected {value!r} to be at least {self.minval}")
#         if self.maxval is not None and value > self.maxval:
#             raise ValueError(f"Expected {value!r} to be at most {self.maxval}")

# class SensorValue(object):
#
#     def __init__(self, ident: int, fn: str, tp: str):
#         self.ident = ident
#         self.fn = fn
#         self.tp = tp
#
#     def __str__(self):
#         return f"({self.ident}, '{self.tp}', '{self.fn}')"
#
#
# class APIParamValue(object):
#
#     def __init__(self, ident: int, api_key: str, api_id: str, api_fn: str,
#                  last_acquisition: datetime):
#         self.ident = ident
#         self.api_key = api_key
#         self.api_id = api_id
#         self.api_fn = api_fn
#         self.last_acquisition = last_acquisition
#
#     def __str__(self):
#         sql_timestamp = self.last_acquisition.strftime('%Y-%m-%d %H:%M:%S')
#         return f"({self.ident}, '{self.api_key}', '{self.api_id}', '{self.api_fn}', '{sql_timestamp}')"


# class InsertQuery(object):
#
#     def __init__(self, table: str, cols: List[str], schema="level0_raw"):
#         self.values = set()
#         self.cols = cols
#         self.header = f"INSERT INTO {schema}.{table} (" + ','.join(
#             f"{v}" for v in cols) + ") VALUES "
#
#     def add(self, value):
#         if not isinstance(value, str):
#             raise TypeError(f"{self.__class__.__name__} got {type(value)} required str or SensorValue")
#         self.values.add(value)
#
#     def __str__(self):
#         return self.header + ','.join(f"{v}" for v in self.values) + ';'
