import pandas as pd

s = pd.Series([1, 2, 3, 2, 1, 3, 3, 4, 5, 4, 5, 6, 5, 4])


value_counts = s.value_counts().sum()

print(value_counts)