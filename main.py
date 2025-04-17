from decimal import Decimal
from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session
from app.models.walletmodel import Wallet
from sqlalchemy import insert
from tronpy import Tron
from tronpy.exceptions import AddressNotFound
from tronpy.keys import is_base58check_address
from typing import Dict, Annotated, List
from app.backend.db_depends import get_db


app = FastAPI()
client = Tron()

# address validation
class WalletRequest(BaseModel):
    address: str
    @field_validator("address", mode='after')
    def validate_tron_address(cls, v:str) -> str:
        if not is_base58check_address(v):
            raise ValueError("Invalid tron address format")
        return v

# pydantic models for response/saving in db
class WalletResponse(BaseModel):
    address: str
    bandwidth: int
    energy: int
    trx_balance: Decimal


class WalletOut(BaseModel):
    id: int
    address: str
    bandwidth: int
    energy: int
    balance: float
# handler, that receive address and return account data by WalletResponse model/saving in db
@app.post('/wallet_info', response_model=WalletResponse)
async def get_wallet_info(db: Annotated[Session, Depends(get_db)], request: WalletRequest) -> WalletResponse:
    address: str = request.address

    try:
        account_info: Dict = client.get_account_resource(address)
        balance: Decimal = client.get_account_balance(address)
    except AddressNotFound:
        raise HTTPException(status_code=404, detail="Wallet address not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    #
    db.execute(insert(Wallet).values(address = request.address,
                                     bandwidth = account_info.get('NetLimit', 0),
                                     energy = account_info.get('TotalEnergyWeight', 0),
                                     balance = balance))
    db.commit()
    return WalletResponse(
        address=address,
        bandwidth=account_info.get('NetLimit', 0),
        energy=account_info.get("TotalEnergyWeight", 0),
        trx_balance=balance
    )
# handler that return records from db, depends on offset(pagination)
@app.get('/wallets', response_model=List[WalletOut])
async def get_wallets(
        db: Session = Depends(get_db),
        limit: int = Query(5, ge=1, le=100),
        offset: int = Query(0, ge = 0)
):
    wallets = db.query(Wallet).offset(offset).limit(limit).all()
    return wallets
