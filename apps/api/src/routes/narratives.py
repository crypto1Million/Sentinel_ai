from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def narratives():

    return {

        "trending": [

            "AI",

            "ANIMAL",

            "POLITICAL"
        ]
    }


@router.get("/{name}")
async def narrative(
    name: str
):

    return {

        "name": name,

        "momentum": 0,

        "tokens": []
    }