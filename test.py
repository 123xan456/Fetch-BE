import pandas as pd
from datetime import datetime, timezone

now = datetime.now(timezone.utc)
now = now.strftime('%Y-%m-%dT%H:%M:%SZ')

print(now)  # Output: 2024-12-07T19:07:48.546102+00:00

# df = pd.read_csv("points_sheet.csv")

# points = []
# for record in df.itertuples():
#     payer = [record.timestamp, record.payer, record.points]
#     points.append(payer)
    
# print(df)

# df.to_csv("points_sheet.csv")
    
