# create-device.md

## Objective
Criar um device mínimo no ThingsBoard CE para testes de ingestão.

## When to use
Quando iniciar onboarding de um novo device no ambiente Sentivis SIM.

## Preconditions
- Tenant admin com acesso à UI.
- Ambiente ThingsBoard CE acessível.

## Short steps
1. Abrir `Entities > Devices`.
2. Clicar em `+` e informar `Name` e `Device profile`.
3. Salvar e abrir detalhes do device criado.

## Common errors
- Permissão insuficiente do usuário.
- Device profile inexistente.

## Internal references
- `check-device-token.md`
- `rest-api-auth.md`

## Out of scope
Provisionamento em massa e automação avançada.
