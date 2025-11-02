# Hands-on: Gestão de Incidentes (MTTR, RTO e RPO)

Este lab sobe um ambiente simples com **MySQL 8** e uma **API Flask** para demonstrar, na prática, como medir **tempo de detecção/recuperação** e comparar com **RTO/RPO**.

## Requisitos
- Docker e Docker Compose
- curl (para o monitor)

## Subir o ambiente
```bash
docker compose up -d --build
# aguarde o MySQL ficar healthy e a API iniciar
curl http://localhost:8080/health
curl http://localhost:8080/init-db
curl -i http://localhost:8080/txn
curl http://localhost:8080/stats
```

## Medir MTTD/MTTR (monitor simples)
Em um terminal, rode o monitor do /health:
```bash
./scripts/monitor.sh
```

## Simular falha (para observar downtime e recuperação)
Em outro terminal, provoque a falha no banco:
```bash
docker kill mysql-preoday
# o compose vai recriar o container (restart always) – acompanhe o monitor
```
Observe quanto tempo o `/health` fica fora (downtime) e quando volta.
- **MTTD**: tempo até o monitor perceber o DOWN.
- **MTTR**: tempo até voltar a responder 200 (UP).

## Parâmetros de conexão (se quiser testar externamente)
```
db.url=jdbc:mysql://localhost:3306/preoday_api_tests
db.user=preoday
db.pass=preoday
```

## Limpar
```bash
docker compose down -v
```

> Dica: defina um **RTO** de referência (p.ex. 60s) e verifique se a recuperação automática aconteceu dentro da meta.
