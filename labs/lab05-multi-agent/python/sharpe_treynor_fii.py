"""
========================================================
  Índices de Sharpe e Treynor para Carteira de FIIs
========================================================
Requisitos: pip install pandas numpy yfinance matplotlib seaborn
"""

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")


# ─────────────────────────────────────────────
#  CONFIGURAÇÕES
# ─────────────────────────────────────────────

# Sua carteira de FIIs com pesos (devem somar 1.0)
CARTEIRA = {
    "BTLG11.SA": 0.20,
    "XPML11.SA": 0.15,
    "HGRU11.SA": 0.15,
    "KNRI11.SA": 0.15,
    "MCCI11.SA": 0.15,
    "RCRB11.SA": 0.20,
}

BENCHMARK    = "IFIX.SA"       # Índice de referência (pode trocar por ^BVSP)
SELIC_ANUAL  = 0.1375          # Taxa Selic atual (~13,75% ao ano)
PERIODO_ANOS = 2               # Janela histórica de análise
PERIODO_DIAS = PERIODO_ANOS * 252


# ─────────────────────────────────────────────
#  1. COLETA DE DADOS
# ─────────────────────────────────────────────

def baixar_dados(tickers: list, benchmark: str, anos: int) -> tuple[pd.DataFrame, pd.Series]:
    """Baixa preços ajustados e retorna retornos diários."""
    fim   = datetime.today()
    inicio = fim - timedelta(days=anos * 365)

    print(f"\n📥 Baixando dados de {inicio.date()} até {fim.date()}...")

    todos = tickers + [benchmark]
    precos = yf.download(todos, start=inicio, end=fim, auto_adjust=True)["Close"]
    precos.dropna(how="all", inplace=True)

    retornos_ativos = precos[tickers].pct_change().dropna()
    retornos_bench  = precos[benchmark].pct_change().dropna()

    # Alinhar índices
    idx = retornos_ativos.index.intersection(retornos_bench.index)
    return retornos_ativos.loc[idx], retornos_bench.loc[idx]


# ─────────────────────────────────────────────
#  2. RETORNO DA CARTEIRA
# ─────────────────────────────────────────────

def calcular_retorno_carteira(retornos: pd.DataFrame, pesos: dict) -> pd.Series:
    """Retorno diário ponderado da carteira."""
    tickers_validos = [t for t in pesos if t in retornos.columns]
    w = np.array([pesos[t] for t in tickers_validos])
    w = w / w.sum()  # renormaliza caso algum ticker não tenha dados
    return retornos[tickers_validos].dot(w).rename("Carteira")


# ─────────────────────────────────────────────
#  3. ÍNDICE DE SHARPE
# ─────────────────────────────────────────────

def calcular_sharpe(retornos_diarios: pd.Series, selic_anual: float) -> dict:
    """
    Sharpe = (Retorno Anualizado - Taxa Livre de Risco) / Volatilidade Anualizada
    """
    rf_diario        = (1 + selic_anual) ** (1 / 252) - 1
    excesso          = retornos_diarios - rf_diario

    retorno_anual    = (1 + retornos_diarios.mean()) ** 252 - 1
    volatilidade     = retornos_diarios.std() * np.sqrt(252)
    sharpe           = (retorno_anual - selic_anual) / volatilidade

    return {
        "Retorno Anualizado":   retorno_anual,
        "Volatilidade Anual":   volatilidade,
        "Excesso de Retorno":   retorno_anual - selic_anual,
        "Índice de Sharpe":     sharpe,
    }


# ─────────────────────────────────────────────
#  4. ÍNDICE DE TREYNOR + BETA
# ─────────────────────────────────────────────

def calcular_beta(retornos_ativo: pd.Series, retornos_bench: pd.Series) -> float:
    """Beta = Cov(ativo, mercado) / Var(mercado)"""
    cov_matrix = np.cov(retornos_ativo, retornos_bench)
    return cov_matrix[0, 1] / cov_matrix[1, 1]


def calcular_treynor(retornos_carteira: pd.Series,
                     retornos_bench: pd.Series,
                     selic_anual: float) -> dict:
    """
    Treynor = (Retorno Anualizado - Taxa Livre de Risco) / Beta
    """
    beta          = calcular_beta(retornos_carteira, retornos_bench)
    retorno_anual = (1 + retornos_carteira.mean()) ** 252 - 1
    treynor       = (retorno_anual - selic_anual) / beta

    return {
        "Beta":              beta,
        "Retorno Anualizado": retorno_anual,
        "Índice de Treynor": treynor,
    }


# ─────────────────────────────────────────────
#  5. ANÁLISE INDIVIDUAL POR ATIVO
# ─────────────────────────────────────────────

def analisar_ativos(retornos: pd.DataFrame,
                    retornos_bench: pd.Series,
                    selic_anual: float) -> pd.DataFrame:
    """Calcula Sharpe, Treynor e Beta para cada ativo individualmente."""
    resultados = []
    for ticker in retornos.columns:
        r    = retornos[ticker].dropna()
        sh   = calcular_sharpe(r, selic_anual)
        tr   = calcular_treynor(r, retornos_bench, selic_anual)
        resultados.append({
            "Ticker":            ticker.replace(".SA", ""),
            "Retorno Anual (%)": round(sh["Retorno Anualizado"] * 100, 2),
            "Volatilidade (%)":  round(sh["Volatilidade Anual"] * 100, 2),
            "Beta":              round(tr["Beta"], 3),
            "Sharpe":            round(sh["Índice de Sharpe"], 3),
            "Treynor (%)":       round(tr["Índice de Treynor"] * 100, 3),
        })
    return pd.DataFrame(resultados).set_index("Ticker")


# ─────────────────────────────────────────────
#  6. CLASSIFICAÇÃO DE QUALIDADE
# ─────────────────────────────────────────────

def classificar_sharpe(valor: float) -> str:
    if valor >= 1.0:   return "🟢 Excelente"
    if valor >= 0.5:   return "🟡 Bom"
    if valor >= 0.0:   return "🟠 Fraco"
    return "🔴 Negativo"

def classificar_treynor(valor: float) -> str:
    if valor >= 0.10:  return "🟢 Excelente"
    if valor >= 0.05:  return "🟡 Bom"
    if valor >= 0.0:   return "🟠 Fraco"
    return "🔴 Negativo"


# ─────────────────────────────────────────────
#  7. VISUALIZAÇÃO
# ─────────────────────────────────────────────

def plotar_dashboard(df_ativos: pd.DataFrame,
                     retorno_carteira: pd.Series,
                     retorno_bench: pd.Series,
                     sharpe_cart: dict,
                     treynor_cart: dict):

    sns.set_theme(style="darkgrid", palette="muted")
    fig = plt.figure(figsize=(16, 12))
    fig.patch.set_facecolor("#0f1117")
    gs  = gridspec.GridSpec(3, 2, figure=fig, hspace=0.45, wspace=0.35)

    cor_titulo = "white"
    cor_eixo   = "#aaaaaa"

    def estilizar(ax, titulo):
        ax.set_facecolor("#1c1e26")
        ax.set_title(titulo, color=cor_titulo, fontsize=12, fontweight="bold", pad=10)
        ax.tick_params(colors=cor_eixo)
        for spine in ax.spines.values():
            spine.set_edgecolor("#333344")

    # ── 1. Retorno Acumulado ──────────────────
    ax1 = fig.add_subplot(gs[0, :])
    cum_cart  = (1 + retorno_carteira).cumprod() - 1
    cum_bench = (1 + retorno_bench).cumprod() - 1
    ax1.plot(cum_cart.index,  cum_cart * 100,  color="#4fc3f7", lw=2,   label="📦 Carteira")
    ax1.plot(cum_bench.index, cum_bench * 100, color="#ef9a9a", lw=1.5, label="📊 Benchmark", linestyle="--")
    ax1.set_ylabel("Retorno Acumulado (%)", color=cor_eixo)
    ax1.legend(facecolor="#1c1e26", labelcolor="white")
    estilizar(ax1, "Retorno Acumulado: Carteira vs Benchmark")

    # ── 2. Sharpe por Ativo ───────────────────
    ax2 = fig.add_subplot(gs[1, 0])
    cores = ["#4fc3f7" if v >= 0 else "#ef9a9a" for v in df_ativos["Sharpe"]]
    bars  = ax2.barh(df_ativos.index, df_ativos["Sharpe"], color=cores)
    ax2.axvline(0, color="white", lw=0.8, linestyle="--")
    ax2.set_xlabel("Índice de Sharpe", color=cor_eixo)
    for bar, val in zip(bars, df_ativos["Sharpe"]):
        ax2.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                 f"{val:.2f}", va="center", color="white", fontsize=9)
    estilizar(ax2, "Índice de Sharpe por Ativo")

    # ── 3. Treynor por Ativo ──────────────────
    ax3 = fig.add_subplot(gs[1, 1])
    cores2 = ["#81c784" if v >= 0 else "#ef9a9a" for v in df_ativos["Treynor (%)"]]
    bars2  = ax3.barh(df_ativos.index, df_ativos["Treynor (%)"], color=cores2)
    ax3.axvline(0, color="white", lw=0.8, linestyle="--")
    ax3.set_xlabel("Índice de Treynor (%)", color=cor_eixo)
    for bar, val in zip(bars2, df_ativos["Treynor (%)"]):
        ax3.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                 f"{val:.2f}%", va="center", color="white", fontsize=9)
    estilizar(ax3, "Índice de Treynor por Ativo")

    # ── 4. Risco x Retorno (Scatter) ──────────
    ax4 = fig.add_subplot(gs[2, 0])
    sc = ax4.scatter(df_ativos["Volatilidade (%)"], df_ativos["Retorno Anual (%)"],
                     s=df_ativos["Sharpe"].abs() * 200, alpha=0.8,
                     c=df_ativos["Sharpe"], cmap="RdYlGn")
    for i, row in df_ativos.iterrows():
        ax4.annotate(i, (row["Volatilidade (%)"], row["Retorno Anual (%)"]),
                     textcoords="offset points", xytext=(6, 4),
                     color="white", fontsize=8)
    ax4.set_xlabel("Volatilidade (%)", color=cor_eixo)
    ax4.set_ylabel("Retorno Anual (%)", color=cor_eixo)
    plt.colorbar(sc, ax=ax4, label="Sharpe").ax.yaxis.label.set_color("white")
    estilizar(ax4, "Risco vs Retorno (tamanho = |Sharpe|)")

    # ── 5. Beta por Ativo ─────────────────────
    ax5 = fig.add_subplot(gs[2, 1])
    cores3 = ["#ffb74d" if b > 1 else "#4fc3f7" for b in df_ativos["Beta"]]
    ax5.barh(df_ativos.index, df_ativos["Beta"], color=cores3)
    ax5.axvline(1, color="white", lw=0.8, linestyle="--")
    ax5.set_xlabel("Beta", color=cor_eixo)
    estilizar(ax5, "Beta por Ativo (linha = mercado = 1)")

    # ── Título geral ──────────────────────────
    sh_val  = round(sharpe_cart["Índice de Sharpe"], 3)
    tr_val  = round(treynor_cart["Índice de Treynor"] * 100, 3)
    beta_val = round(treynor_cart["Beta"], 3)
    fig.suptitle(
        f"📊 Análise da Carteira FII  |  Sharpe: {sh_val}  |  Treynor: {tr_val}%  |  Beta: {beta_val}",
        color="white", fontsize=14, fontweight="bold", y=0.98
    )

    plt.savefig("/mnt/user-data/outputs/dashboard_fii.png", dpi=150,
                bbox_inches="tight", facecolor=fig.get_facecolor())
    print("\n✅ Dashboard salvo: dashboard_fii.png")
    plt.show()


# ─────────────────────────────────────────────
#  8. RELATÓRIO FINAL
# ─────────────────────────────────────────────

def imprimir_relatorio(sharpe_cart: dict, treynor_cart: dict, df_ativos: pd.DataFrame):
    sh  = sharpe_cart["Índice de Sharpe"]
    tr  = treynor_cart["Índice de Treynor"]
    beta = treynor_cart["Beta"]

    print("\n" + "="*55)
    print("       📋 RELATÓRIO DA CARTEIRA FII")
    print("="*55)
    print(f"  Retorno Anualizado : {sharpe_cart['Retorno Anualizado']*100:.2f}%")
    print(f"  Volatilidade Anual : {sharpe_cart['Volatilidade Anual']*100:.2f}%")
    print(f"  Beta da Carteira   : {beta:.3f}")
    print(f"  Selic (rf)         : {SELIC_ANUAL*100:.2f}%")
    print("-"*55)
    print(f"  Índice de Sharpe   : {sh:.3f}  → {classificar_sharpe(sh)}")
    print(f"  Índice de Treynor  : {tr*100:.3f}% → {classificar_treynor(tr)}")
    print("="*55)

    print("\n📊 Análise por Ativo:")
    print(df_ativos.to_string())

    print("\n📌 Interpretação:")
    if sh > 1:
        print("  ✅ Sharpe > 1: Carteira bem remunerada pelo risco total.")
    elif sh > 0.5:
        print("  🟡 Sharpe entre 0,5 e 1: Retorno adequado para o risco.")
    else:
        print("  ⚠️  Sharpe < 0,5: Carteira não remunera bem o risco total.")

    if beta < 0.8:
        print("  🛡️  Beta baixo: Carteira defensiva — menos sensível ao mercado.")
    elif beta < 1.2:
        print("  ⚖️  Beta próximo de 1: Carteira acompanha o mercado.")
    else:
        print("  ⚡ Beta alto: Carteira agressiva — amplifica movimentos do mercado.")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    tickers = list(CARTEIRA.keys())

    # 1. Dados
    ret_ativos, ret_bench = baixar_dados(tickers, BENCHMARK, PERIODO_ANOS)

    # 2. Retorno da carteira ponderada
    ret_carteira = calcular_retorno_carteira(ret_ativos, CARTEIRA)

    # 3. Métricas da carteira
    sharpe_cart  = calcular_sharpe(ret_carteira, SELIC_ANUAL)
    treynor_cart = calcular_treynor(ret_carteira, ret_bench, SELIC_ANUAL)

    # 4. Análise individual
    df_ativos = analisar_ativos(ret_ativos, ret_bench, SELIC_ANUAL)

    # 5. Relatório e visualização
    imprimir_relatorio(sharpe_cart, treynor_cart, df_ativos)
    plotar_dashboard(df_ativos, ret_carteira, ret_bench, sharpe_cart, treynor_cart)
