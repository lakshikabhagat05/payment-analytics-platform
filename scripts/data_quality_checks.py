def validate_transactions(df):
    issues = []

    if df["amount"].isnull().sum() > 0:
        issues.append("NULL_AMOUNTS")

    if (df["amount"] <= 0).sum() > 0:
        issues.append("INVALID_AMOUNTS")

    if df.duplicated().sum() > 0:
        issues.append("DUPLICATES")

    return issues