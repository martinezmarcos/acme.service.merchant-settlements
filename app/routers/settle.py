from datetime import datetime
from fastapi import APIRouter
from app.acme_payments_api.transactions import get_merchant_transactions_by_date

router = APIRouter(tags=["settle"])


@router.get("/settle/{merchant_id}")
async def wex_webhook_reciever(merchant_id: str, date: str = datetime.now().date()):  # NOQA
    # NOTE (marcos): the default date str is todays date as YY-MM-DD
    transactions = await get_merchant_transactions_by_date(merchant_id, date)
    print(len(transactions))
    return {"success": merchant_id}
