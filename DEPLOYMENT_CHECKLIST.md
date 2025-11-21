# Checklist de Deploy Rápido

## Antes de Fazer o Deploy

- [ ] `back-end/.env` contém `API_KEY`
- [ ] `back-end/.env` contém `GROQ_API_KEY`
- [ ] `back-end/.env` contém `NOMIC_KEY`
- [ ] Credenciais AWS configuradas (`aws configure`)
- [ ] Dependências Node.js instaladas em `rag-cdk-infra/` (`npm install`)

## Deploy do Backend

```bash
cd rag-cdk-infra
cdk bootstrap  # Necessário apenas uma vez por conta/região AWS
cdk deploy
```

## Após o Deploy

Copie os valores de saída:
```
Outputs:
RagCdkInfraStack.ApiGatewayUrl = https://xxxxxxxxxx.execute-api.sa-east-1.amazonaws.com/prod/
RagCdkInfraStack.ApiKeyId = xxxxxxxxxxxxx
```

## Configurar Frontend

1. Crie o arquivo `front-end/.env.local`:
```bash
BACKEND_URL=https://xxxxxxxxxx.execute-api.sa-east-1.amazonaws.com/prod
BACKEND_API_KEY=SUA_API_KEY
```

2. Inicie o frontend localmente:
```bash
cd front-end
npm run dev
```

## Deploy do Frontend na Vercel

1. **Instale a Vercel CLI** (se ainda não tiver):
```bash
npm install -g vercel
```

2. **Faça login na Vercel**:
```bash
vercel login
```

3. **Deploy do frontend**:
```bash
cd front-end
vercel
```

4. **Configure as variáveis de ambiente na Vercel**:
   - Acesse o dashboard da Vercel: https://vercel.com/dashboard
   - Selecione seu projeto
   - Vá em "Settings" → "Environment Variables"
   - Adicione as seguintes variáveis:
     - `BACKEND_URL`: `https://xxxxxxxxxx.execute-api.sa-east-1.amazonaws.com/prod`
     - `BACKEND_API_KEY`: `sua_api_key_do_backend_env`

5. **Faça um novo deploy após configurar variáveis**:
```bash
vercel --prod
```

## Testar o Deploy

```bash
# Substitua SUA_API_KEY e SUA_URL_API pelos valores reais
curl -H "x-api-key: SUA_API_KEY" SUA_URL_API/health
```

Resposta esperada: `{"ok":true}`

## Solução de Problemas

**403 Forbidden** - Verifique se a API key está correta no header `x-api-key`
**500 Internal Server Error** - Verifique os logs do Lambda: `cd rag-cdk-infra && ./check-logs.sh`
**Variáveis de ambiente não carregadas** - Certifique-se de que `back-end/.env` existe e contém todas as chaves necessárias
