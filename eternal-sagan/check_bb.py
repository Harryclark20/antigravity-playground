import pandas as pd
import pandas_ta as ta
import numpy as np

# Create dummy data
df = pd.DataFrame({'close': np.random.randn(50).cumsum()})
df.ta.bbands(length=20, std=2.0, append=True)
print(df.columns.tolist())
