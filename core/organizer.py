import re
import shutil
from pathlib import Path

from core.config import PASTA_PROCESSADOS


def mover_e_renomear(caminho_origem: str, dados: dict) -> str:

    cpf_limpo = re.sub(r"\D", "", dados["CPF"])
    nome_limpo = re.sub(r"[^\w]", "_", dados["Nome Completo"])

    novo_nome = f"{cpf_limpo}_{nome_limpo}.pdf"

    destino = Path(PASTA_PROCESSADOS) / novo_nome

    shutil.move(caminho_origem, destino)

    return novo_nome
