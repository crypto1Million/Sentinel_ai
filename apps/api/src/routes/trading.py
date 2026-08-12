from fastapi import APIRouter

router = APIRouter()


@router.get("/quote")
async def quote(

    input_mint: str,

    output_mint: str,

    amount: int

):

    return {

        "input_mint": input_mint,

        "output_mint": output_mint,

        "amount": amount
    }


@router.post("/swap")
async def swap():

    return {

        "status": "pending",

        "message": "Swap endpoint"
    }