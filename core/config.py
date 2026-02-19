from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

PASTA_ENTRADA = BASE_DIR / "arquivos_entrada"
PASTA_SAIDA = BASE_DIR / "relatorios_excel"
PASTA_PROCESSADOS = BASE_DIR / "arquivos_processados"


def configurar_ambiente():
    for pasta in [PASTA_ENTRADA, PASTA_SAIDA, PASTA_PROCESSADOS]:
        pasta.mkdir(exist_ok=True)
