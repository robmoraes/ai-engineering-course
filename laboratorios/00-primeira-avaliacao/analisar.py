"""Compare uma regra fixa com rótulos sintéticos; nenhum modelo é treinado."""

import argparse
import csv
import math
from pathlib import Path


def numero_nao_negativo(texto):
    valor = float(texto)
    if not math.isfinite(valor) or valor < 0:
        raise argparse.ArgumentTypeError("informe um número finito não negativo")
    return valor


def carregar_janelas(caminho):
    janelas = []
    with caminho.open(encoding="utf-8", newline="") as arquivo:
        for linha_csv, linha in enumerate(csv.DictReader(arquivo), start=2):
            try:
                requisicoes = int(linha["requisicoes"])
                erros = int(linha["erros_5xx"])
                latencia = float(linha["latencia_p95_ms"])
                falhas_jornada = int(linha["falhas_jornada_em_10"])
                incidente = int(linha["incidente"])
                if not (
                    requisicoes > 0
                    and 0 <= erros <= requisicoes
                    and math.isfinite(latencia)
                    and latencia >= 0
                    and 0 <= falhas_jornada <= 10
                    and incidente in (0, 1)
                ):
                    raise ValueError("contagens, latência ou rótulo inválidos")
                if incidente != int(falhas_jornada >= 2):
                    raise ValueError("rótulo diverge do critério sintético da jornada")
                janelas.append({
                    "inicio": linha["inicio_janela_utc"],
                    "erros_pct": 100 * erros / requisicoes,
                    "latencia_ms": latencia,
                    "incidente": bool(incidente),
                })
            except (KeyError, TypeError, ValueError) as erro:
                raise ValueError(f"CSV, linha {linha_csv}: {erro}") from erro
    if not janelas:
        raise ValueError("o CSV precisa conter pelo menos uma janela")
    return janelas


def classificar(incidente, alerta):
    if incidente:
        return "TP" if alerta else "FN"
    return "FP" if alerta else "TN"


def exibir_fracao(nome, numerador, denominador, motivo_indefinicao):
    if denominador == 0:
        print(f"{nome}: não definida ({motivo_indefinicao})")
    else:
        percentual = 100 * numerador / denominador
        print(f"{nome}: {percentual:.1f}% ({numerador}/{denominador})")


def avaliar(nome, rotulos, alertas):
    matriz = {"TP": 0, "FP": 0, "FN": 0, "TN": 0}
    for incidente, alerta in zip(rotulos, alertas):
        matriz[classificar(incidente, alerta)] += 1
    tp, fp, fn, tn = (matriz[chave] for chave in ("TP", "FP", "FN", "TN"))
    print(f"\n{nome}")
    print("                   Incidente real   Sem incidente")
    print(f"Alerta emitido          TP={tp:<4}         FP={fp}")
    print(f"Sem alerta             FN={fn:<4}         TN={tn}")
    exibir_fracao("Precisão", tp, tp + fp, "nenhum alerta emitido")
    exibir_fracao("Recall", tp, tp + fn, "nenhum incidente rotulado")
    exibir_fracao("Acurácia", tp + tn, len(rotulos), "nenhuma janela")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "csv", nargs="?", type=Path,
        default=Path(__file__).with_name("janelas.csv"),
        help="CSV de entrada; padrão: janelas.csv ao lado deste script",
    )
    parser.add_argument("--limiar-erros-pct", type=numero_nao_negativo, default=5.0)
    parser.add_argument("--limiar-latencia-ms", type=numero_nao_negativo, default=600.0)
    args = parser.parse_args()
    try:
        janelas = carregar_janelas(args.csv)
    except (OSError, ValueError) as erro:
        parser.error(str(erro))

    print(
        f"Regra: erros_5xx >= {args.limiar_erros_pct:.2f}% OU "
        f"latencia_p95 >= {args.limiar_latencia_ms:.1f} ms."
    )
    print(f"Janelas avaliadas: {len(janelas)}\n")
    print("Início UTC             Erros (%)   p95 (ms)   Rótulo   Alerta   Resultado")
    rotulos = []
    alertas = []
    for janela in janelas:
        # Apenas estas duas medidas entram na regra de alerta.
        alerta = (
            janela["erros_pct"] >= args.limiar_erros_pct
            or janela["latencia_ms"] >= args.limiar_latencia_ms
        )
        incidente = janela["incidente"]
        rotulos.append(incidente)
        alertas.append(alerta)
        resultado = classificar(incidente, alerta)
        print(
            f"{janela['inicio']}   {janela['erros_pct']:>8.2f}   "
            f"{janela['latencia_ms']:>8.1f}   {int(incidente):>6}   "
            f"{int(alerta):>6}   {resultado}"
        )

    avaliar("Regra fixa", rotulos, alertas)
    avaliar("Referência: sempre normal", rotulos, [False] * len(rotulos))


if __name__ == "__main__":
    main()
