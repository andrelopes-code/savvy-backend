from datetime import datetime, timezone


def update_model_timestamp(_mapper, _connection, target):
    """Updates model.updated_at field before update the model"""
    target.updated_at = datetime.now(timezone.utc)
