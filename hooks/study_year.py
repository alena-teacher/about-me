"""Подставляет актуальные годы в анонс и копирайт при сборке сайта."""

from __future__ import annotations

import datetime
import re


def on_config(config, **kwargs):
    today = datetime.date.today()
    year = today.year
    config.extra["study_year_start"] = year
    config.extra["study_year_end"] = year + 1
    config.extra["build_date"] = today.isoformat()

    if config.copyright:
        config.copyright = re.sub(r"©\s*\d{4}", f"© {year}", config.copyright)

    return config
