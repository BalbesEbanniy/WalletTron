from decimal import Decimal
from unittest.mock import patch, Mock
from main import get_wallet_info, WalletResponse, WalletRequest
import pytest

@pytest.mark.asyncio
@patch('main.client.get_account_resource')
@patch('main.client.get_account_balance')


async def test_get_wallet_info(mock_get_balance, mock_get_resource):
    mock_get_resource.return_value = {
        'NetLimit': 12345,
        'TotalEnergyWeight': 67890
    }
    mock_get_balance.return_value = Decimal("100.5")

    mock_db = Mock()
    mock_db.execute = Mock()
    mock_db.commit = Mock()


    request = WalletRequest(address = 'TM3sTVyahiGWYktKg8G6miHpTzRurKDt7b')

    response: WalletResponse = await get_wallet_info(db=mock_db, request = request)

    assert response.address == "TM3sTVyahiGWYktKg8G6miHpTzRurKDt7b"
    assert response.bandwidth == 12345
    assert response.energy == 67890
    assert response.trx_balance == Decimal("100.5")

    mock_db.execute.assert_called_once()
    mock_db.commit.assert_called_once()