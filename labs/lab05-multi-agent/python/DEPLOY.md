# 🚀 Deploy no Render — FII Portfolio Analyzer

Guia completo para fazer deploy da API FastAPI no [Render](https://render.com/).

## 📋 Pré-requisitos

1. **Conta no Render**: Crie uma conta gratuita em [render.com](https://render.com/)
2. **Repositório Git**: Projeto deve estar em um repositório Git (GitHub, GitLab, ou Bitbucket)
3. **API Key do LLM**: Chave da API do Google AI Studio (recomendado) ou outro provedor

## 🔑 Obter API Key (Gratuita)

### Opção 1: Google AI Studio (Recomendado)

1. Acesse [aistudio.google.com](https://aistudio.google.com/)
2. Faça login com sua conta Google
3. Clique em "Get API Key"
4. Copie a chave gerada
5. **Tier gratuito**: 60 requisições/minuto, muito generoso!

### Opção 2: Groq (Mais rápido)

1. Acesse [console.groq.com](https://console.groq.com/)
2. Crie uma conta
3. Gere uma API key
4. **Tier gratuito**: Inferência super rápida

## 📦 Arquivos Necessários (Já Criados)

O projeto já inclui os arquivos necessários para deploy:

- ✅ **render.yaml** — Configuração do serviço Render
- ✅ **requirements.txt** — Dependências Python
- ✅ **main.py** — Aplicação FastAPI
- ✅ **.gitignore** — Arquivos ignorados pelo Git

## 🎯 Passo a Passo do Deploy

### 1️⃣ Preparar o Repositório Git

Se ainda não estiver em um repositório Git:

```bash
# Na pasta do projeto
cd /mnt/dados/projetos/taller/ai_training/labs/lab05-multi-agent/python

# Inicializar Git (se necessário)
git init

# Adicionar arquivos
git add .

# Commit
git commit -m "Preparar projeto para deploy no Render"

# Criar repositório no GitHub e fazer push
git remote add origin https://github.com/seu-usuario/seu-repo.git
git branch -M main
git push -u origin main
```

### 2️⃣ Criar Web Service no Render

1. **Login no Render**
   - Acesse [dashboard.render.com](https://dashboard.render.com/)
   - Faça login ou crie uma conta

2. **Novo Web Service**
   - Clique em **"New +"** → **"Web Service"**
   - Conecte seu repositório Git (GitHub/GitLab/Bitbucket)
   - Autorize o Render a acessar o repositório

3. **Selecionar Repositório**
   - Encontre e selecione seu repositório
   - O Render detectará automaticamente que é um projeto Python

4. **Configurar o Serviço**
   
   Se o Render não detectar o `render.yaml` automaticamente, configure manualmente:

   | Campo | Valor |
   |-------|-------|
   | **Name** | `fii-portfolio-analyzer` (ou outro nome) |
   | **Region** | `Oregon (US West)` (mais barato) ou escolha o mais próximo |
   | **Branch** | `main` ou `lab05` |
   | **Root Directory** | `labs/lab05-multi-agent/python` ⚠️ **IMPORTANTE: confira o caminho exato no seu repositório!** |
   | **Runtime** | `Python 3` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
   | **Plan** | `Free` |

### 3️⃣ Configurar Variáveis de Ambiente

Na página de configuração do serviço, vá em **"Environment"** e adicione:

#### Variáveis Obrigatórias:

```
GOOGLE_API_KEY=sua-chave-aqui
LLM_PROVIDER=google
```

#### Variáveis Opcionais (já têm valores padrão):

```
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
RATE_LIMIT_RPM=60
RATE_LIMIT_TPM=100000
EMBEDDING_PROVIDER=local
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

**⚠️ IMPORTANTE**: 
- Nunca commite o arquivo `.env` no Git
- Use sempre variáveis de ambiente secretas do Render para API keys

### 4️⃣ Deploy

1. Clique em **"Create Web Service"**
2. O Render vai:
   - Clonar o repositório
   - Instalar dependências (`pip install`)
   - Iniciar a aplicação
   - Gerar uma URL pública (ex: `https://fii-portfolio-analyzer.onrender.com`)

3. Acompanhe os logs para verificar o deploy:
   - Procure por: `Application startup complete`
   - Procure por: `Uvicorn running on http://0.0.0.0:10000`

### 5️⃣ Testar a API

Após o deploy bem-sucedido:

1. **Documentação Interativa**:
   ```
   https://seu-app.onrender.com/docs
   ```

2. **Teste com cURL**:
   ```bash
   curl https://seu-app.onrender.com/analyze \
     -X POST \
     -H "Content-Type: application/json" \
     -d '{
       "patrimony": 100000,
       "monthly_contribution": 1000,
       "horizon_months": 24,
       "current_portfolio": []
     }'
   ```

3. **No navegador**:
   - Abra `https://seu-app.onrender.com/docs`
   - Use a interface Swagger UI para testar

## 🔄 Atualizações Automáticas

O Render faz deploy automático quando você faz push para o branch configurado:

```bash
# Fazer mudanças no código
git add .
git commit -m "Atualizar análise de portfólio"
git push origin main

# Render detecta e faz deploy automaticamente!
```

## 🆓 Limitações do Plano Free

- **Instâncias**: 0.5 GB RAM, 0.5 CPU
- **Horas**: 750 horas/mês (suficiente para 24/7)
- **Sleep após inatividade**: Dorme após 15 min sem requests
- **Cold start**: ~30s no primeiro request após sleep
- **Largura de banda**: 100 GB/mês

**💡 Dica**: Cold start é normal no plano free. O primeiro request pode demorar, mas os seguintes são rápidos.

## 🐛 Troubleshooting

### Deploy falha na instalação de dependências

```bash
# Localmente, teste a instalação
pip install -r requirements.txt

# Se funcionar localmente mas falhar no Render, tente fixar versões:
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Fixar versões das dependências"
git push
```

### Erro "Root directory does not exist"

**Causa**: O caminho do Root Directory está incorreto no Render.

**Solução**:
1. No dashboard do Render, vá em **Settings**
2. Em **Build & Deploy**, encontre **Root Directory**
3. Verifique o caminho exato no seu repositório Git:
   - Se os arquivos estão em `labs/lab05-multi-agent/python`, use esse caminho
   - Se moveu para a raiz, deixe em branco ou use `.`
4. Clique em **Save Changes**
5. Faça um **Manual Deploy** para testar

**Dica**: Use o navegador de arquivos do GitHub/GitLab para confirmar o caminho exato.

### Erro "Module not found"

Verifique se o `Root Directory` está correto (veja erro acima) ou se faltam dependências no `requirements.txt`.

### Porta não escuta corretamente

O Render fornece a variável `$PORT`. Certifique-se de usar:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Não use `--port 8000` fixo!

### API Key não funciona

1. Verifique se adicionou `GOOGLE_API_KEY` nas variáveis de ambiente do Render
2. Teste a chave localmente primeiro:
   ```bash
   export GOOGLE_API_KEY="sua-chave"
   export LLM_PROVIDER="google"
   uvicorn main:app --reload
   ```

### Logs de Erro

No dashboard do Render:
1. Clique no seu serviço
2. Vá em **"Logs"**
3. Procure por erros em vermelho

## 📊 Monitoramento

No dashboard do Render você pode ver:

- **Métricas**: CPU, memória, requests/segundo
- **Logs em tempo real**: stdout/stderr da aplicação
- **Eventos**: Deploys, builds, crashes
- **Health checks**: Status HTTP da aplicação

## 🔒 Segurança

1. **Nunca commite** arquivos `.env` no Git
2. Use **variáveis de ambiente secretas** do Render para API keys
3. Configure **CORS** adequadamente em produção (em `main.py`, pode restringir origins)
4. Considere adicionar **autenticação** se a API for pública

## 💰 Upgrade para Plano Pago (Opcional)

Se precisar de mais recursos:

- **Starter** ($7/mês): RAM/CPU dedicados, sem sleep, builds mais rápidos
- **Standard** ($25/mês): Escala automática, métricas avançadas
- **Pro** ($85/mês): Suporte prioritário, SLA

Para este projeto, o **plano free é suficiente** para testes e demos!

## 🌐 Conectar com Frontend

Se tiver um frontend (React, Vue, etc.), atualize a URL da API:

```javascript
// frontend/src/config.js
const API_URL = process.env.REACT_APP_API_URL || 'https://seu-app.onrender.com';

// Fazer requests
const response = await fetch(`${API_URL}/analyze`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(portfolioData)
});
```

## 🎉 Pronto!

Sua API está no ar! Compartilhe a URL com outras pessoas:

```
https://seu-app.onrender.com/docs
```

---

## 📚 Recursos Adicionais

- [Documentação oficial do Render](https://render.com/docs)
- [Render + FastAPI Tutorial](https://render.com/docs/deploy-fastapi)
- [Python no Render](https://render.com/docs/python-version)
- [Variáveis de ambiente no Render](https://render.com/docs/environment-variables)

---

**Criado para o AI Training Program** 🚀
