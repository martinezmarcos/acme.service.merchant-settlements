import aiohttp
import backoff

from . import api_endpoint

from datetime import datetime, timedelta, timezone
from dateutil.parser import isoparse


@backoff.on_exception(backoff.expo, Exception, max_tries=5, max_time=10)
async def _make_transactions_request(endoint: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(endoint) as res:
            return await res.json()


async def get_merchant_transactions_by_date(merchant_id: str, date: datetime = datetime.now().date()):
    # NOTE (marcos): created_at__gt/gte query param renders empty result
    following_date = (date + timedelta(days=1)).isoformat()

    transactions = []

    res = await _make_transactions_request(
        api_endpoint + f"/tech_assessment/transactions?merchant={merchant_id}&created_at__lt={following_date}"
    )

    _next = res["next"]
    if len(res["results"]):
        transactions += res["results"]

    while _next is not None:
        res = await _make_transactions_request(_next)

        _next = res["next"]
        if len(res["results"]):
            transactions += res["results"]

    return list(
        filter(
            lambda x: isoparse(x["created_at"]) >= datetime(date.year, date.month, date.day, tzinfo=timezone.utc),
            transactions,
        )
    )
