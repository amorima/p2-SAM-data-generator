# SAM — Gerador de Dados Sintéticos

> Repositório de geração de dados para o projeto **Sistema de Apoio Municipal (SAM)** — plataforma híbrida (Web + IoT) que conecta mecenas, negócios, instituições de solidariedade e cidadãos num ecossistema de doação urbana.

Projeto académico desenvolvido no âmbito da Licenciatura em Tecnologias e Sistemas de Informação para a Web — Politécnico do Porto (ESMAD), Grupo 02.

---

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Arquitetura de Dados](#arquitetura-de-dados)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Entidades Geradas](#entidades-geradas)
- [Notas de Geração](#notas-de-geração)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Utilização](#utilização)
- [Output](#output)
- [Migração para a Base de Dados](#migração-para-a-base-de-dados)

---

## Sobre o Projeto

Este repositório é responsável pela **geração de dados sintéticos realistas** para popular as bases de dados do SAM em ambiente de desenvolvimento e testes. Os dados são gerados em Python com a biblioteca [Faker](https://faker.readthedocs.io/) (locale `pt_PT`) e exportados em formato **JSON** e **CSV**.

Os dados gerados cobrem as duas bases de dados do projeto:

- **MySQL** — dados relacionais e transacionais (entidades, doações, pedidos, lockers, etc.)
- **MongoDB** — dados não relacionais de telemetria IoT, auditoria financeira, logs de interação, notificações e vouchers

---

## Arquitetura de Dados

O SAM utiliza uma arquitetura híbrida:

```
Dispositivos IoT / Frontend Web
           │
    Backend / API SAM
     ┌──────┴──────┐
   MySQL        MongoDB
(estruturado) (não estruturado)
```

**MySQL** armazena dados transacionais e de negócio: entidades, mecenas, doações, pedidos, lockers e painéis.

**MongoDB** armazena dados de alto volume e estrutura variável: telemetria dos equipamentos IoT, auditoria de pagamentos, logs de comportamento dos utilizadores nos painéis digitais, notificações e vouchers.

A interoperabilidade entre as duas bases de dados é assegurada pela camada de aplicação (Backend). Os documentos MongoDB armazenam os identificadores únicos (PKs) das entidades SQL, permitindo o cruzamento de informação sempre que necessário.

---

## Estrutura do Repositório

```
p2-SAM-data-generator/
├── p2_sam/
│   ├── __main__.py                        # Ponto de entrada — orquestra toda a geração
│   ├── entities/
│   │   ├── localidade/
│   │   │   └── generator.py               # Gera códigos postais válidos via GeoNames
│   │   ├── entidade/
│   │   │   └── generator.py               # Agrega NIFs de mecenas, negócios e instituições
│   │   ├── mecena/
│   │   │   └── generator.py
│   │   ├── doacao/
│   │   │   └── generator.py
│   │   ├── negocio/
│   │   │   └── generator.py
│   │   ├── instituicao/
│   │   │   └── generator.py
│   │   ├── contacto/
│   │   │   └── generator.py
│   │   ├── pedido/
│   │   │   └── generator.py
│   │   ├── bens_servicos/
│   │   │   └── generator.py               # Dicionário estático de bens e serviços
│   │   ├── pedido_bens_servico/
│   │   │   └── generator.py
│   │   ├── painel_digital/
│   │   │   └── generator.py
│   │   ├── locker/
│   │   │   └── generator.py
│   │   ├── cidadao/
│   │   │   └── generator.py
│   │   ├── lead/
│   │   │   └── generator.py
│   │   └── nosql/
│   │       ├── locker_telemetry_generator.py
│   │       ├── financial_log_generator.py  # Um log por cada doação gerada
│   │       ├── interaction_log_generator.py
│   │       ├── notification_generator.py
│   │       └── voucher_generator.py
│   └── exporters/
│       ├── csv_exporter.py                # Exporta qualquer entidade para CSV
│       ├── json_exporter.py               # Exporta qualquer entidade para JSON
│       └── mongodb_exporter.py            # Exporta coleções NoSQL para JSON
├── models/                                # Models Sequelize (MySQL)
│   ├── index.js
│   ├── entidade.js
│   ├── mecenas.js
│   ├── doacao.js
│   ├── negocio.js
│   ├── instituicao.js
│   ├── localidade.js
│   ├── localidade_entidade.js
│   ├── contacto.js
│   ├── pedido.js
│   ├── bens_e_servico.js
│   ├── bens_e_servicos_negocio.js
│   ├── pedido_bens_e_servicos.js
│   ├── painel.js
│   ├── locker_inteligente.js
│   └── lead.js
├── migrations/                            # Migrations Sequelize (MySQL)
│   ├── 01-create-localidade.js
│   ├── 02-create-entidade.js
│   ├── 03-create-localidade-entidade.js
│   ├── 04-create-mecena.js
│   ├── 05-create-doacao.js
│   ├── 06-create-negocio.js
│   ├── 07-create-instituicao.js
│   ├── 08-create-contacto.js
│   ├── 09-create-bens-e-servico.js
│   ├── 10-create-bens-e-servicos-negocio.js
│   ├── 11-create-pedido.js
│   ├── 12-create-pedido-bens-e-servicos.js
│   ├── 13-create-painel.js
│   ├── 14-create-locker-inteligente.js
│   ├── 15-create-cidadao.js
│   └── 16-create-lead.js
├── seeders/                               # Seeders Sequelize (MySQL)
│   ├── 01-seed-localidade.js
│   ├── 02-seed-entidade.js
│   └── 03-seed-localidade-entidade.js
├── config/
│   └── database.js                        # Configuração da ligação Sequelize
├── output/                                # Ficheiros gerados (JSON + CSV) — não versionado
├── tests/
│   └── codigo_postal_rua.py               # Testes isolados
├── pyproject.toml
└── README.md
```

---

## Entidades Geradas

### MySQL

A geração segue a ordem de dependências — entidades sem dependências são criadas primeiro, as que referenciam outras são criadas depois.

| Ordem | Entidade | Quantidade | Dependências |
|-------|----------|------------|--------------|
| 1 | `Localidade` | 100 | — |
| 2 | `Mecena` | 50 | — |
| 3 | `Negocio` | 50 | Localidade |
| 4 | `Instituicao` | 50 | Localidade |
| 5 | `Entidade` | 150 | Mecena + Negocio + Instituicao |
| 6 | `Contacto` | 150 | Entidade |
| 7 | `Doacao` | 200 | Mecena |
| 8 | `Painel_Digital` | 30 | Localidade |
| 9 | `Locker_Inteligente` | 30 | Localidade |
| 10 | `Cidadao` | 100 | — |
| 11 | `Bens_E_Servicos` | ~55 (estático) | — |
| 12 | `Pedido` | 100 | Entidade |
| 13 | `Pedido_Bens_E_Servicos` | 150 | Pedido + Bens_E_Servicos |
| 14 | `Bens_E_Servicos_Negocio` | 100 | Negocio + Bens_E_Servicos |
| 15 | `Lead` | 100 | Painel + Pedido + Locker + Cidadao |

### MongoDB

As coleções NoSQL são geradas após toda a geração SQL, pois referenciam PKs das tabelas relacionais.

| Coleção | Quantidade | Referência SQL |
|---------|------------|----------------|
| `locker_telemetry` | 200 | `locker_inteligente.id_locker` / `painel.id_dispositivo` |
| `financial_log` | 1 por doação (200) | `doacao.id_doacao` |
| `interaction_log` | 300 | `painel.id_dispositivo` |
| `notification` | 150 | `leads.id_lead` |
| `vouchers` | 100 | `entidade.nif_nipc` + `negocio.nif_nipc` |

---

## Notas de Geração

**Localidade** — os códigos postais são gerados com `faker.postcode()` (locale `pt_PT`) e validados contra a base GeoNames via [pgeocode](https://pgeocode.readthedocs.io/). Códigos inválidos são descartados e regenerados. As coordenadas geográficas reais ficam disponíveis internamente (prefixo `_`) para uso por outras entidades, mas não são exportadas nesta tabela.

**NIFs/NIPCs** — cada entidade gera o seu próprio identificador fiscal com o prefixo correto:
- `Mecena`: `1`, `2`, `5` ou `9` (maioria `9` — pessoas coletivas)
- `Negocio`: `5` ou `9` (maioria `9` — empresas privadas)
- `Instituicao`: `5` ou `9` (entidades públicas e coletivas sem fins lucrativos)

**Entidade** — não gera NIFs próprios. Agrega os NIFs já gerados por `Mecena`, `Negocio` e `Instituicao`, e cria para cada um o `email_login` (formato `primeiro.ultimo@dominio` para pessoas, `nomedaorganizacao@dominio` para organizações), `password`, `iban` e endereço.

**Bens_E_Servicos** — geração estática a partir de dois dicionários: `BENS_POR_CATEGORIA` e `SERVICOS_POR_CATEGORIA`. Cada entrada é única e serve como PK da tabela. Os valores não têm acentos nem maiúsculas para compatibilidade com a BD. O campo `tipo` mapeia para o ENUM do model: `"bem"` ou `"servico"`.

**Financial_Log** — cada doação gera exatamente um log financeiro, partilhando a mesma data. Garante cobertura total de auditoria sem registos órfãos.

---

## Pré-requisitos

- Python 3.11+
- Node.js 18+ (para os models, migrations e seeders Sequelize)

---

## Instalação

```bash
# Clonar o repositório
git clone https://github.com/amorima/p2-SAM-data-generator.git
cd p2-SAM-data-generator

# Criar e ativar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# ou
.venv\Scripts\activate     # Windows

# Instalar dependências Python
pip install -e .
```

As dependências principais são `faker`, `pgeocode` e `pandas`, declaradas no `pyproject.toml`.

---

## Utilização

```bash
# Ativar o ambiente virtual (se ainda não estiver ativo)
source .venv/bin/activate

# Correr o gerador completo
python -m p2_sam
```

O terminal mostra o progresso da geração de cada entidade, incluindo número de tentativas, taxa de sucesso e tempo decorrido.

Para alterar as quantidades geradas, editar as chamadas em `p2_sam/__main__.py`:

```python
localidades  = generate_localidades(n=100)
mecenas      = generate_mecenas(n=50)
doacoes      = generate_doacoes(n=200, mecenas=mecenas)
# ...
```

---

## Output

Após a execução, a pasta `output/` contém os ficheiros gerados:

```
output/
├── # MySQL — par JSON + CSV por entidade
├── localidade.json           / localidade.csv
├── entidade.json             / entidade.csv
├── mecena.json               / mecena.csv
├── doacao.json               / doacao.csv
├── negocio.json              / negocio.csv
├── instituicao.json          / instituicao.csv
├── contacto.json             / contacto.csv
├── pedido.json               / pedido.csv
├── bens_servicos.json        / bens_servicos.csv
├── pedido_bens_servicos.json / pedido_bens_servicos.csv
├── bens_servicos_negocio.json / bens_servicos_negocio.csv
├── painel_digital.json       / painel_digital.csv
├── locker.json               / locker.csv
├── cidadao.json              / cidadao.csv
├── lead.json                 / lead.csv
│
└── # MongoDB — apenas JSON, prefixado com nosql_
    ├── nosql_locker_telemetry.json
    ├── nosql_financial_log.json
    ├── nosql_interaction_log.json
    ├── nosql_notification.json
    └── nosql_vouchers.json
```

A pasta `output/` está no `.gitignore` — os ficheiros gerados não são versionados.

---

## Migração para a Base de Dados

### MySQL — Sequelize

Correr as migrations para criar as tabelas:

```bash
npx sequelize-cli db:migrate
```

Correr os seeders para popular a base de dados com os dados gerados:

```bash
npx sequelize-cli db:seed:all
```

A ordem de execução respeita automaticamente as foreign keys pela numeração dos ficheiros (`01-`, `02-`, etc.).

### MongoDB

Os ficheiros `nosql_*.json` podem ser importados diretamente com o `mongoimport`:

```bash
mongoimport --db sam --collection locker_telemetry --file output/nosql_locker_telemetry.json --jsonArray
mongoimport --db sam --collection financial_log     --file output/nosql_financial_log.json     --jsonArray
mongoimport --db sam --collection interaction_log   --file output/nosql_interaction_log.json   --jsonArray
mongoimport --db sam --collection notification      --file output/nosql_notification.json      --jsonArray
mongoimport --db sam --collection vouchers          --file output/nosql_vouchers.json          --jsonArray
```