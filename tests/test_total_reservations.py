"""Testes adicionais: Total de reservas."""

from helpers import run_cli

def test_total_reservations_equals_rows_csv(tmp_path):
    """O total de reservas é igual ao número de linhas do csv alimentado. (Exceto cabeçalho)"""
    status = ["CONFIRMED", "NO_SHOW", "CANCELLED"]
    reservations = [{"reservation_id": f"R-{i}", "status": status[i%3]} for i in range(250)]

    report = run_cli(
        tmp_path,
        reservations,
    )
    assert report["summary"]["total_reservations"] == 250
    assert report["summary"]["confirmed_reservations"] == 84
    assert report["summary"]["cancelled_reservations"] == 83
    assert report["summary"]["no_show_reservations"] == 83
