import app as a
import pandas as pd

out = []
out.append("=== ROUTES ===")
for r in sorted(a.app.url_map.iter_rules(), key=lambda x: x.rule):
    out.append(f"  {r.rule}")

out.append("\n=== DATASET ===")
df = pd.read_csv('dataset/retail_sales.csv')
out.append(f"  Columns: {df.columns.tolist()}")
out.append(f"  Rows: {len(df)}")
out.append(f"  Categories: {df['Category'].unique().tolist()}")

with open("verify.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("Done")
