"""Подставляет актуальные годы в анонс и копирайт при сборке сайта."""

from __future__ import annotations

import datetime
import re


def on_config(config, **kwargs):
    year = datetime.date.today().year
    config.extra["study_year_start"] = year
    config.extra["study_year_end"] = year + 1

    if config.copyright:
        config.copyright = re.sub(r"©\s*\d{4}", f"© {year}", config.copyright)

    return config
