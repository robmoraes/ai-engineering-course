"""Exercício de manutenção: versão inicial com dois defeitos intencionais."""

import argparse
import json
from pathlib import Path


def validar_evento(evento, origem):
    """Valide o esquema mínimo sem corrigir silenciosamente a entrada."""
    campos = {"servico", "status_http"}
    if not isinstance(evento, dict) or set(evento) != campos:
        raise ValueError(
            f"{origem}: esperado objeto com apenas servico e status_http"
        )
    servico = evento["servico"]
    if not isinstance(servico, str) or not servico or servico != servico.strip():
        raise ValueError(
            f"{origem}: servico deve ser texto não vazio, sem espaços nas extremidades"
        )
    status = evento["status_http"]
    if type(status) is not int or not 100 <= status <= 599:
        raise ValueError(f"{origem}: status_http deve ser inteiro entre 100 e 599")


def ler_eventos(caminho):
    """Leia JSONL em UTF-8; a mensagem de erro preserva a linha física."""
    with Path(caminho).open(encoding="utf-8") as arquivo:
        for numero, linha in enumerate(arquivo, start=1):
            if not linha.strip():
                continue
            try:
                evento = json.loads(linha)
            except json.JSONDecodeError as erro:
                raise ValueError(
                    f"linha {numero}: JSON inválido, coluna {erro.colno}"
                ) from erro
            validar_evento(evento, f"linha {numero}")
            yield evento


def gerar_relatorio(eventos):
    """Resuma um iterável de eventos válidos sem alterar os objetos recebidos."""
    try:
        iterador = iter(eventos)
    except TypeError as erro:
        raise ValueError("eventos deve ser um iterável de objetos") from erro

    acumulados = {}
    for numero, evento in enumerate(iterador, start=1):
        validar_evento(evento, f"evento {numero}")
        servico = evento["servico"]
        if servico not in acumulados:
            acumulados[servico] = {"total_requisicoes": 0, "total_erros": 0}
        acumulados[servico]["total_requisicoes"] += 1
        if evento["status_http"] >= 400:
            acumulados[servico]["total_erros"] += 1

    por_servico = {}
    for servico in sorted(acumulados):
        contagens = acumulados[servico]
        por_servico[servico] = {
            **contagens,
            "taxa_erros": contagens["total_erros"] / contagens["total_requisicoes"],
        }

    total_requisicoes = sum(item["total_requisicoes"] for item in por_servico.values())
    total_erros = sum(item["total_erros"] for item in por_servico.values())
    taxa_erros = (
        sum(item["taxa_erros"] for item in por_servico.values()) / len(por_servico)
        if por_servico else None
    )
    return {
        "estado": "com_dados" if total_requisicoes else "sem_dados",
        "total_requisicoes": total_requisicoes,
        "total_erros": total_erros,
        "taxa_erros": taxa_erros,
        "por_servico": por_servico,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("arquivo", type=Path, help="arquivo JSONL em UTF-8")
    args = parser.parse_args()
    try:
        relatorio = gerar_relatorio(ler_eventos(args.arquivo))
    except (OSError, UnicodeError, ValueError) as erro:
        parser.error(str(erro))
    print(json.dumps(relatorio, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
