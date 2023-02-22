from fastapi import APIRouter, Body

router = APIRouter(tags=["settle"])


@router.get("/settle/{merchant_id}")
async def wex_webhook_reciever(merchant_id: str):  # NOQA
    return {"success": merchant_id}
