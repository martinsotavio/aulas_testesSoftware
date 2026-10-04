"""Conversão dos textos digitados nos formulários para os tipos usados nas regras."""
from datetime import date
from decimal import Decimal, InvalidOperation

from app.regras import RegraVioladaError


def ler_valor(texto: str) -> Decimal:
    """Aceita '1234.56', '1234,56' e '1.234,56'."""
    texto = (texto or "").strip()
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    try:
        valor = Decimal(texto)
    except InvalidOperation:
        raise RegraVioladaError("Valor inválido.") from None
    if not valor.is_finite():
        raise RegraVioladaError("Valor inválido.")
    return valor.quantize(Decimal("0.01"))


def ler_data(texto: str) -> date:
    try:
        return date.fromisoformat((texto or "").strip())
    except ValueError:
        raise RegraVioladaError("Data inválida.") from None


def ler_inteiro(texto: str, padrao: int = 1) -> int:
    texto = (texto or "").strip()
    if not texto:
        return padrao
    try:
        return int(texto)
    except ValueError:
        raise RegraVioladaError("Número inválido.") from None
