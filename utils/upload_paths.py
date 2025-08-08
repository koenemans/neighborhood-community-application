"""Utilities for generating unique upload paths for media files."""

from __future__ import annotations

import os
import uuid
from typing import Callable

from django.utils import timezone


def hashed_upload_path(prefix: str) -> Callable[[object, str], str]:
    """Return a callable for ``upload_to`` that adds a unique hash to filenames.

    The resulting path has the form ``"{prefix}/YYYY/MM/DD/<name>_<hash><ext>"``
    where ``<hash>`` is a random hexadecimal string ensuring uniqueness.

    Parameters
    ----------
    prefix:
        Directory prefix where the file should be stored (e.g. ``"news/posters"``).

    Returns
    -------
    Callable[[object, str], str]
        Function suitable for Django's ``upload_to`` argument.
    """

    def uploader(instance: object, filename: str) -> str:
        # Determine date path based on ``created_at`` if available, otherwise now.
        created = getattr(instance, "created_at", None) or timezone.now()
        date_path = created.strftime("%Y/%m/%d")

        base, ext = os.path.splitext(filename)
        file_hash = uuid.uuid4().hex
        return f"{prefix}/{date_path}/{base}_{file_hash}{ext}"

    return uploader

