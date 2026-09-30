"""Testes do contrato; exatamente dois falham na versão inicial do exercício."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from relatorio import gerar_relatorio, ler_eventos


def evento(servico, status):
    return {"servico": servico, "status_http": status}


class TestRelatorio(unittest.TestCase):
    def test_entrada_vazia(self):
        self.assertEqual(gerar_relatorio([]), {
            "estado": "sem_dados",
            "total_requisicoes": 0,
            "total_erros": 0,
            "taxa_erros": None,
            "por_servico": {},
        })

    def test_apenas_status_5xx_sao_erros(self):
        dados = [evento("api", status) for status in (199, 200, 399, 400, 499, 500, 599)]
        relatorio = gerar_relatorio(dados)
        self.assertEqual(relatorio["total_requisicoes"], 7)
        self.assertEqual(relatorio["total_erros"], 2)
        self.assertEqual(relatorio["por_servico"]["api"]["total_erros"], 2)
        self.assertAlmostEqual(relatorio["taxa_erros"], 2 / 7)

    def test_taxa_global_pondera_requisicoes(self):
        dados = [evento("catalogo", 200) for _ in range(7)]
        dados += [evento("catalogo", 500), evento("pagamentos", 200), evento("pagamentos", 503)]
        relatorio = gerar_relatorio(dados)
        self.assertEqual(relatorio["total_requisicoes"], 10)
        self.assertEqual(relatorio["total_erros"], 2)
        self.assertAlmostEqual(relatorio["por_servico"]["catalogo"]["taxa_erros"], 0.125)
        self.assertAlmostEqual(relatorio["por_servico"]["pagamentos"]["taxa_erros"], 0.5)
        self.assertAlmostEqual(relatorio["taxa_erros"], 0.2)

    def test_agrupamento_e_ordem_por_servico(self):
        dados = [evento("pagamentos", 503), evento("catalogo", 200),
                 evento("pagamentos", 200), evento("catalogo", 500)]
        relatorio = gerar_relatorio(dados)
        self.assertEqual(relatorio["estado"], "com_dados")
        self.assertEqual(relatorio["total_requisicoes"], 4)
        self.assertEqual(relatorio["total_erros"], 2)
        self.assertEqual(relatorio["taxa_erros"], 0.5)
        self.assertEqual(list(relatorio["por_servico"]), ["catalogo", "pagamentos"])
        for resumo in relatorio["por_servico"].values():
            self.assertEqual(resumo, {
                "total_requisicoes": 2, "total_erros": 1, "taxa_erros": 0.5,
            })

    def test_aceita_iterador_sem_alterar_eventos(self):
        dados = [evento("api", 200), evento("api", 201)]
        original = copy.deepcopy(dados)
        relatorio = gerar_relatorio(iter(dados))
        self.assertEqual(dados, original)
        self.assertEqual(relatorio["total_requisicoes"], 2)
        self.assertEqual(relatorio["total_erros"], 0)
        self.assertEqual(relatorio["taxa_erros"], 0.0)

    def test_rejeita_campos_invalidos(self):
        invalidos = [None, [], {}, {"servico": "api"},
                     {"servico": "api", "status_http": 200, "extra": 1}]
        invalidos += [evento(nome, 200) for nome in (None, "", " ", " api", "api ", 12)]
        invalidos += [evento("api", status) for status in (True, False, 200.0, "200", 99, 600, None)]
        for invalido in invalidos:
            with self.subTest(evento=invalido):
                with self.assertRaisesRegex(ValueError, "evento 1"):
                    gerar_relatorio([invalido])
        with self.assertRaisesRegex(ValueError, "iterável"):
            gerar_relatorio(None)

    def test_jsonl_ignora_linhas_vazias_e_informa_linha_invalida(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "entrada.jsonl"
            valido = json.dumps(evento("api", 200))
            caminho.write_text("\n" + valido + "\n   \n", encoding="utf-8")
            self.assertEqual(list(ler_eventos(caminho)), [evento("api", 200)])
            casos = [("{", "linha 3: JSON inválido"),
                     ('{"servico":"api","status_http":700}', "linha 3: status_http")]
            for invalido, mensagem in casos:
                with self.subTest(linha=invalido):
                    caminho.write_text("\n" + valido + "\n" + invalido, encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, mensagem):
                        list(ler_eventos(caminho))

    def test_cli_json_e_erro_sem_relatorio_parcial(self):
        script = Path(__file__).with_name("relatorio.py")
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "entrada.jsonl"
            caminho.write_text(json.dumps(evento("api", 500)) + "\n", encoding="utf-8")
            comando = [sys.executable, "-B", str(script), str(caminho)]
            resultado = subprocess.run(comando, text=True, capture_output=True, check=False)
            self.assertEqual(resultado.returncode, 0, resultado.stderr)
            self.assertEqual(resultado.stderr, "")
            self.assertEqual(json.loads(resultado.stdout), {
                "estado": "com_dados", "total_requisicoes": 1,
                "total_erros": 1, "taxa_erros": 1.0,
                "por_servico": {"api": {
                    "total_requisicoes": 1, "total_erros": 1, "taxa_erros": 1.0,
                }},
            })
            caminho.write_text(json.dumps(evento("api", 200)) + "\n{\n", encoding="utf-8")
            resultado = subprocess.run(comando, text=True, capture_output=True, check=False)
            self.assertEqual(resultado.returncode, 2)
            self.assertEqual(resultado.stdout, "")
            self.assertIn("linha 2", resultado.stderr)
            self.assertNotIn("Traceback", resultado.stderr)


if __name__ == "__main__":
    unittest.main()
