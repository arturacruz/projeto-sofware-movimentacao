import requests
from app_service import calcular_valor, criar_objeto_movimentacao, validar_campos
from unittest.mock import patch, MagicMock

def test_validar_campos_completos():
    data = {
        "cpf_comprador": "123",
        "cpf_vendedor": "456",
        "ticker": "PETR4",
        "quantidade": 10
    }
    assert validar_campos(data) is None

def test_validar_campos_incompletos():
    data = {
        "cpf_comprador": "123",
        "cpf_vendedor": "456",
        "ticker": "PETR4" 
    }
    assert validar_campos(data) is not None

@patch('app_service.requests.get')
def test_calcular_valor_ok(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "ticker": "PETR4", "lastValue": 100
    }
    mock_get.return_value = mock_resp

    value, err = calcular_valor("PETR4", 2);
    assert err is None
    assert value == 200

@patch('app_service.requests.get')
def test_calcular_valor_not_found(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 404
    mock_get.return_value = mock_resp

    value, err = calcular_valor("PETR4", 2)
    assert err is not None
    assert value is None

@patch('app_service.requests.get')
def test_calcular_valor_connection_error(mock_get):
    mock_resp = MagicMock()
    mock_resp.side_effect = requests.RequestException
    mock_get.side_effect = mock_resp

    value, err = calcular_valor("PETR4", 2)
    assert err is not None
    assert "Erro de conexão:" in err
    assert value is None

@patch('app_service.requests.get')
def test_criar_objeto_movimentacao(mock_get):
    data = {
        "cpf_comprador": "123",
        "cpf_vendedor": "456",
        "ticker": "PETR4",
        "quantidade": 10
    }
    assert validar_campos(data) is None

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "ticker": "PETR4", "lastValue": 100
    }
    mock_get.return_value = mock_resp

    value, err = calcular_valor("PETR4", 2);
    assert err is None
    assert value == 200

    valid_obj = {
        "cpf_comprador": data["cpf_comprador"],
        "cpf_vendedor": data["cpf_vendedor"],
        "ticker": data["ticker"],
        "quantidade": data["quantidade"],
        "valor_movimentacao": value
    }

    assert criar_objeto_movimentacao(data, value) == valid_obj
