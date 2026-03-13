# rest-api-auth.md

## Objective
Obter e validar autenticação JWT para chamadas REST administrativas.

## When to use
Quando for necessário usar endpoints administrativos via API REST.

## Preconditions
- Credenciais válidas de usuário tenant.
- Endpoint `/api/auth/login` acessível.

## Short steps
1. Fazer `POST /api/auth/login` com username/password.
2. Extrair `token` JWT da resposta.
3. Usar header `X-Authorization: Bearer <token>`.

## Common errors
- Credencial inválida (`401`).
- Header de autorização com formato incorreto.

## Internal references
- `create-device.md`
- `check-device-token.md`

## Out of scope
Integração OAuth e SSO enterprise.
