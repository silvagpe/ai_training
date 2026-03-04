Eu preciso criar um projeto de conclusão do curso com foco em IA. O que eu estou pensando em fazer é um sistema de avaliação de carteira e projeção de crescimento com base em aportes mensais. O foco será FIIs (fundos imobiliarios)

O que o sistema deve fazer
 - Avaliar os ativos informatos pelo cliente e validar o risco dos papeis. 
 - Sugerir se os papeis se deve manter ou trocar um determinado papel.
 - Para um papel ser bom ele deve cumprir algumas regras 
    - Ter mais de 5 anos de existência
    - Movimentar mais de 1 milhão dia
    - Considerar a lista dos 50 maiores FIIs
    - Tamanho do FII mais de 1 bilhão em carteira
 - O sistema deve sugerir entre 3 a 10 FIIs para uma carteira com base no patrimonio do cliente
    - Se o patrimonio for abaixo de 100 mil - 3 FIIs
    - Se o patrimonio for de 100 até 300 - 5 FIIs
    - Se for acima de 300 mil - de 5 a 10 Fiis
  - A diversificação deve considerar o % de retrono e o tipo de fundo, Tijolo, Papeis, Misto. Não deve-se usar apenas um tipo e dar prefência para papeis do tipo Tijolo.


  Adicionais:
  - Como implementar os Indices Sharpe e Treynor para avaliação da carteira?
  - Como fazer uma comparação de 5 anos entre a carteira selecionada e o IFIX?
    - https://investidor10.com.br/indices/ifix/


# Projeto de Conclusão (Lab 5) — Avaliação de Carteira de FIIs com Projeção

## Objetivo
Construir um sistema multiagente em Python para:
- Avaliar a carteira de FIIs do cliente
- Classificar risco por regras objetivas
- Sugerir manter ou trocar ativos
- Propor carteira recomendada conforme patrimônio
- Projetar crescimento com aportes mensais

## Escopo Funcional (MVP)
1. Avaliação da carteira informada pelo cliente
2. Recomendação de manter ou trocar cada ativo com justificativa
3. Filtro de FIIs elegíveis por regras:
   - Mais de 5 anos de existência
   - Volume médio diário maior que 1 milhão
   - Estar entre os 50 maiores FIIs
   - Patrimônio do FII maior que 1 bilhão
4. Sugestão de quantidade de FIIs por patrimônio do cliente:
   - Até 100 mil: 3 FIIs
   - De 100 mil a 300 mil: 5 FIIs
   - Acima de 300 mil: entre 5 e 10 FIIs
5. Diversificação por tipo (Tijolo, Papel, Misto):
   - Evitar concentração em um único tipo
   - Dar preferência para Tijolo
   - Considerar retorno esperado na composição
6. Projeção de crescimento com aportes mensais (cenário base e conservador)

## Arquitetura (Supervisor Pattern)
- **Supervisor Agent**: coordena o fluxo e sintetiza a resposta final
- **Researcher Agent**: analisa dados da carteira, elegibilidade e risco por regras
- **Writer Agent**: transforma análise em recomendação clara para o cliente
- **Reviewer Agent (opcional)**: revisa consistência e qualidade da resposta

## Dados e Premissas do MVP
- Fonte de dados inicial: snapshot local em JSON
- Sem dependência de API de mercado em tempo real no MVP
- Risco calculado de forma determinística por regras
- Saída com explicabilidade: motivos de aprovação/reprovação por ativo

## Adicionais (Pós-MVP)
1. Implementar índice Sharpe para retorno excedente por volatilidade total
2. Implementar índice Treynor para retorno excedente por risco sistemático (beta)
3. Comparação da carteira recomendada vs IFIX em 5 anos:
   - Retorno acumulado
   - Diferença absoluta e percentual
   - Visualização de série temporal (quando dados estiverem disponíveis)

## Critérios de Sucesso (Lab 5)
- Sistema multiagente funcional (Supervisor + pelo menos 2 Workers)
- Fluxo end-to-end funcionando via endpoint `/run`
- Recomendação final com justificativas claras e rastreáveis por regra


# Arquitetura Sugerida (Python, Lab 5)

## Visão Geral
- Arquitetura em camadas: **API → Orquestração Multiagente → Regras de Negócio → Dados**.
- O **Supervisor** coordena agentes especializados e produz saída final explicável.
- Decisões críticas (manter/trocar, elegibilidade, diversificação) ficam em serviços determinísticos.
- Agentes usam LLM para análise textual e síntese, mas sobre resultados já calculados por regras.
- Projeção, Sharpe/Treynor e comparação com IFIX ficam em módulos independentes.

## Fluxo Recomendado
1. API recebe carteira, patrimônio, aportes e horizonte.
2. Serviço de regras valida elegibilidade e risco por ativo.
3. Supervisor delega:
   - **Researcher**: interpreta resultados e riscos.
   - **Writer**: monta recomendação e alocação final.
   - **Reviewer**: valida consistência.
4. Módulo de projeção calcula crescimento futuro.
5. Módulo de métricas calcula Sharpe, Treynor e comparação com IFIX.
6. Supervisor consolida resposta final estruturada.

## Estrutura de Pastas Sugerida

```text
python/
├── main.py
├── config/
│   └── settings.py
├── api/
│   ├── routes.py
│   └── schemas.py
├── orchestration/
│   ├── supervisor.py
│   └── state.py
├── agents/
│   ├── base.py
│   ├── researcher.py
│   ├── writer.py
│   ├── reviewer.py
│   └── prompts.py
├── domain/
│   ├── entities.py
│   ├── portfolio_rules.py
│   ├── diversification.py
│   └── recommendation.py
├── analytics/
│   ├── projection.py
│   ├── sharpe_treynor.py
│   └── benchmark_ifix.py
├── data/
│   ├── providers/
│   │   ├── fii_snapshot_provider.py
│   │   └── ifix_provider.py
│   └── snapshots/
│       ├── fii_snapshot.json
│       └── ifix_5y.json
│       └── recommended_portfolio.json
├── services/
│   ├── portfolio_service.py
│   └── evaluation_service.py
├── llm/
│   ├── client.py
│   └── factory.py
└── tests/
    ├── test_rules.py
    ├── test_projection.py
    ├── test_supervisor_flow.py
    └── test_api_run.py
```



# Fluxo de Análise e Recomendação — FII Portfolio Analyzer

## Novo Fluxo (Researcher Agent)

### Etapa 1: Comparação da Carteira do Cliente vs Recomendações

```text
Carteira do Cliente
├─ KNCR11 (Kinea Rendimentos)
└─ [outros ativos...]
↓
Cruzar com Carteira Recomendada
├─ XPML11 (XP Malls)
├─ HGLG11 (Pátria Log)
├─ MXRF11 (Maxi Renda)
└─ [outros...]
↓
Para cada ativo do cliente:
┌─ Está em recomendações?
│ ├─ SIM → MANTER (rebalancear peso se necessário)
│ └─ NÃO → VENDER/TROCAR
│
└─ Está em recomendações mas não na carteira?
└─ COMPRAR
```


### Etapa 2: Lógica de Decisão por Ativo

| Cenário | Ação | Justificativa |
|---------|------|--------------|
| Ativo do cliente está na recomendação | **MANTER** | Validado pelas regras e análise |
| Ativo do cliente NÃO está na recomendação | **AVALIAR** | Verificar se não cumpre regras ou baixos retornos |
| Ativo recomendado NÃO está na carteira | **COMPRAR** | Oportunidade de diversificação |
| P/VP desfavorável (ex: > 1,10) | **VENDER/TROCAR** | Superavaliado, trocar por alternativa melhor |

---

## Resultado Esperado

### 1. Análise Consolidada (output do Researcher)

```json
{
  "client_portfolio": {
    "assets": [
      {
        "ticker": "KNCR11",
        "name": "Kinea Rendimentos Imobiliários",
        "current_price": 9.66,
        "allocation_pct": 50.0
      }
    ],
    "total_value_brl": 100000
  },
  "analysis": {
    "hold_assets": [
      {
        "ticker": "KNCR11",
        "action": "MANTER",
        "reason": "Ativo sólido, atende regras mínimas (DY 13.77%, P/VP 1.04)",
        "current_weight": 50.0,
        "recommended_weight": 10.0,
        "rebalance_needed": true
      }
    ],
    "buy_assets": [
      {
        "ticker": "XPML11",
        "action": "COMPRAR",
        "reason": "Recomendado para diversificação em varejo, P/VP 1.00",
        "recommended_weight": 10.0,
        "suggested_allocation_brl": 10000
      },
      {
        "ticker": "HGLG11",
        "action": "COMPRAR",
        "reason": "Diversificação em logística, P/VP abaixo de 1.0",
        "recommended_weight": 5.0,
        "suggested_allocation_brl": 5000
      }
    ]
  }
}