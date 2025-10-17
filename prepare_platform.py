import pandas as pd

# File Tiki
df_tiki = pd.read_csv("tiki_clean.csv", encoding="utf-8-sig")
df_tiki["platform"] = "Tiki"
df_tiki.to_csv("tiki_clean_platform.csv", index=False, encoding="utf-8-sig")

# File Hasaki
df_hasaki = pd.read_csv("hasaki_clean.csv", encoding="utf-8-sig")
df_hasaki["platform"] = "Hasaki"
df_hasaki.to_csv("hasaki_clean_platform.csv", index=False, encoding="utf-8-sig")
