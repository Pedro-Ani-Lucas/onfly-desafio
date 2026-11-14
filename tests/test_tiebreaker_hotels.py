"""Testes adicionais: critério de desempate dos hotéis"""

from helpers import run_cli


def test_tiebreaker_hotels_id(tmp_path):
    """O ranking mostra o desempate de dois hotéis com valores iguais."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-3", "hotel_id": "H03", "hotel_name": "Hotel C", "amount": "1000.00"},
            {"reservation_id": "R-1", "hotel_id": "H01", "hotel_name": "Hotel A", "amount": "800.00"},
            {"reservation_id": "R-2", "hotel_id": "H02", "hotel_name": "Hotel B", "amount": "1000.00"},
            {"reservation_id": "R-4", "hotel_id": "H04", "hotel_name": "Hotel D", "amount": "900.00"},
        ],
        top=3,
    )
    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H02", "H03", "H04"]
    assert [hotel["total_brl"] for hotel in report["top_hotels"]] == ["1000.00", "1000.00", "900.00"]
