from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
import shutil
import uvicorn
import pandas as pd
from datetime import datetime
from pathlib import Path

from core.config import configurar_ambiente, PASTA_ENTRADA, PASTA_SAIDA
from core.pdf_processor import extrair_conteudo_pdf
from core.analyzer import analisar_texto
from core.organizer import mover_e_renomear

app = FastAPI(title="Data Manager")
START_TIME = datetime.now()


@app.get("/")
def home():
    return {"mensagem": "API online"}


@app.get("/sistema", response_class=HTMLResponse)
def sistema():
    with open("templates/sistema.html", encoding="utf-8") as f:
        return f.read()


@app.post("/upload")
def upload_pdf(arquivo: UploadFile = File(...)):

    configurar_ambiente()

    destino = PASTA_ENTRADA / arquivo.filename

    with open(destino, "wb") as buffer:
        shutil.copyfileobj(arquivo.file, buffer)

    texto = extrair_conteudo_pdf(destino)

    if not texto:
        return JSONResponse(status_code=400, content={"erro": "PDF vazio"})

    dados = analisar_texto(texto, arquivo.filename)

    novo_nome = mover_e_renomear(destino, dados)

    # 🔹 GERAR EXCEL DO ARQUIVO ÚNICO
    df = pd.DataFrame([dados])

    nome_excel = f"relatorio_unico_{datetime.now():%Y%m%d_%H%M%S}.xlsx"

    caminho_excel = PASTA_SAIDA / nome_excel

    df.to_excel(caminho_excel, index=False)

    return {
        "mensagem": "Arquivo processado com sucesso",
        "novo_nome": novo_nome,
        "relatorio_gerado": nome_excel,
        "dados": dados
    }


@app.post("/processar-lote")
def processar_lote():

    configurar_ambiente()

    arquivos = list(Path(PASTA_ENTRADA).glob("*.pdf"))

    dados_consolidados = []

    for arquivo in arquivos:
        texto = extrair_conteudo_pdf(arquivo)

        if texto:
            dados = analisar_texto(texto, arquivo.name)
            dados_consolidados.append(dados)
            mover_e_renomear(arquivo, dados)

    if dados_consolidados:

        df = pd.DataFrame(dados_consolidados)

        nome_excel = f"relatorio_{datetime.now():%Y%m%d_%H%M%S}.xlsx"

        df.to_excel(PASTA_SAIDA / nome_excel, index=False)

    return {"mensagem": "Lote processado"}



# 🔹 DOWNLOAD ÚLTIMO RELATÓRIO
@app.get("/download-relatorio")
def download_relatorio():
    arquivos = sorted(Path(PASTA_SAIDA).glob("*.xlsx"), reverse=True)

    if not arquivos:
        return {"erro": "Nenhum relatório encontrado"}

    ultimo = arquivos[0]

    return FileResponse(
        path=ultimo,
        filename=ultimo.name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@app.get("/status")
def status():
    uptime = datetime.now() - START_TIME

    total_uploads = len(list(Path(PASTA_ENTRADA).glob("*"))) if Path(PASTA_ENTRADA).exists() else 0
    total_relatorios = len(list(Path(PASTA_SAIDA).glob("*.xlsx"))) if Path(PASTA_SAIDA).exists() else 0

    return JSONResponse({
        "sistema": "online",
        "uploads": total_uploads,
        "relatorios": total_relatorios,
        "uptime": str(uptime).split(".")[0]
    })


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
