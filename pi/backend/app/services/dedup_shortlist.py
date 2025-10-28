def deduplicate(candidates: list[dict]) -> list[dict]:
    seen = set()
    result = []
    for c in candidates:
        key = (c.get("email"), c.get("name"))
        if key in seen:
            continue
        seen.add(key)
        result.append(c)
    return result
