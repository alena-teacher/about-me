"""Подставляет текущий и следующий год в анонс при сборке сайта."""

from __future__ import annotations

import datetime


def on_config(config, **kwargs):
    year = datetime.date.today().year
    config.extra["study_year_start"] = year
    config.extra["study_year_end"] = year + 1
    return config
