from __future__ import annotations

from datetime import datetime, timezone

# Fluxer uses the same epoch as Discord: 2015-01-01T00:00:00Z
FLUXER_EPOCH = 1420070400000


def snowflake_to_datetime(snowflake: str | int) -> datetime:
    """Convert a Fluxer Snowflake ID to a datetime.

    Snowflakes encode a timestamp in the upper 42 bits.

    Args:
        snowflake: The Snowflake ID as a string or int.

    Returns:
        A timezone-aware UTC datetime.
    """
    timestamp_ms = (int(snowflake) >> 22) + FLUXER_EPOCH
    return datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)


def datetime_to_snowflake(dt: datetime) -> int:
    """Convert a datetime to a Snowflake ID (useful for pagination).

    This creates a Snowflake with only the timestamp component set.
    Useful for before/after pagination parameters.

    Args:
        dt: A datetime object.

    Returns:
        A Snowflake integer.
    """
    timestamp_ms = int(dt.timestamp() * 1000)
    snowflake = (timestamp_ms - FLUXER_EPOCH) << 22
    return snowflake


def _try_int(value: str | int | None) -> int | None:
    """Safely convert a value to int, or return None."""
    if value is None:
        return None
    return int(value)


def _get_mime_type(filename: str) -> str:
    """Guess MIME type from a filename."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    mime_map = {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
        "webp": "image/webp",
        "mp4": "video/mp4",
        "mp3": "audio/mpeg",
        "ogg": "audio/ogg",
        "wav": "audio/wav",
        "txt": "text/plain",
        "json": "application/json",
        "pdf": "application/pdf",
    }
    return mime_map.get(ext, "application/octet-stream")
