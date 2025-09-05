import datetime as dt


MOSCOW_TZ = dt.timezone(dt.timedelta(hours=3))


def datetime_to_moscow_proper_date(
    t: dt.datetime | dt.date | str | None,
) -> str:
    if t is None:
        return "Не указано"

    if isinstance(t, str):
        try:
            t = dt.datetime.fromisoformat(t)
        except ValueError:
            return "Не указано"

    if isinstance(t, dt.datetime):
        if t.tzinfo is None:
            t = t.replace(tzinfo=dt.timezone.utc)
        t = t.astimezone(MOSCOW_TZ)
        return t.strftime("%d.%m.%Y")

    if isinstance(t, dt.date):
        return t.strftime("%d.%m.%Y")

    return "Не указано"
