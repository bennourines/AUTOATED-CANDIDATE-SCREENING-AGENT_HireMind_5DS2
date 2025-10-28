def record_feedback(entity: str, entity_id: int, feedback: str) -> dict:
    return {"status": "recorded", "entity": entity, "id": entity_id}
