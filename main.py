from decimal import Decimal

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import Field, BaseModel, validator, field_validator
from tronpy import Tron
from tronpy.exceptions import AddressNotFound
from tronpy.keys import is_base58check_address
from typing import Dict

app = FastAPI()
client = Tron()


class WalletRequest(BaseModel):
    address: str

    @field_validator("address", mode='before')
    def validate_tron_address(cls, v:str) -> str:
        if not is_base58check_address(v):
            raise ValueError("Invalid tron address format")
        return v


class WalletResponse(BaseModel):
    address: str
    bandwidth: int
    energy: int
    trx_balance: Decimal


@app.post('/wallet_info', response_model=WalletResponse)
async def get_wallet_info(request: WalletRequest) -> WalletResponse:
    address: str = request.address

    try:
        account_info: Dict = client.get_account_resource(address)
        balance: Decimal = client.get_account_balance(address)
    except AddressNotFound:
        raise HTTPException(status_code=404, detail="Wallet address not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    return WalletResponse(
        address=address,
        bandwidth=account_info.get("free_net_used", 0),
        energy = account_info.get("EnergyUsed", 0),
        trx_balance=balance
    )








# @app.get('/')
# async def get_wallets():
#     return {'msg':'all wallets, include paggination'}





# @app.get('/hello/{adress}')
# async def post_wallets(adress: Annotated[str, Path(min_length=10, max_length=100)],
#                        first_name: Annotated[str | None, Query(min_length=2, max_length=10)] = None) -> dict:
#     return {'msg': adress, 'name' : first_name}