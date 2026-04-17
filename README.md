# SAM — Gerador de Dados Sintéticos

> Repositório de geração de dados para o projeto **Sistema de Apoio Municipal (SAM)** — plataforma híbrida (Web + IoT) que conecta mecenas, negócios, instituições de solidariedade e cidadãos num ecossistema de doação urbana.

Projeto académico desenvolvido no âmbito da Licenciatura em Tecnologias e Sistemas de Informação para a Web — Politécnico do Porto (ESMAD), Grupo 02.

---

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Arquitetura de Dados](#arquitetura-de-dados)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Entidades Geradas](#entidades-geradas)
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
- **MongoDB** — dados não relacionais de telemetria IoT, auditoria financeira e logs de interação

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

**MongoDB** armazena dados de alto volume e estrutura variável: telemetria dos equipamentos IoT, auditoria de pagamentos e logs de comportamento dos utilizadores nos painéis digitais.

---

## Estrutura do Repositório

```
p2-SAM-data-generator/
├── p2_sam/
│   ├── __main__.py                  # Ponto de entrada — orquestra toda a geração
│   ├── entities/
│   │   ├── localidade/
│   │   │   ├── generator.py         # Gera códigos postais válidos via GeoNames
│   │   │   └── schema.py
│   │   ├── entidade/
│   │   │   ├── generator.py         # Agrega NIFs de mecenas, negócios e instituições
│   │   │   └── schema.py
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
│   │   │   └── generator.py
│   │   ├── pedido_bens_servico/
│   │   │   └── generator.py
│   │   ├── painel_digital/
│   │   │   └── generator.py
│   │   ├── locker/
│   │   │   └── generator.py
│   │   ├── cidadao/
│   │   │   └── generator.py
│   │   └── lead/
│   │       └── generator.py
│   └── exporters/
│       ├── csv_exporter.py          # Exporta qualquer entidade para CSV
│       └── json_exporter.py         # Exporta qualquer entidade para JSON
├── models/                          # Models Sequelize (MySQL)
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
├── config/
│   └── database.js                  # Configuração da ligação Sequelize
├── output/                          # Ficheiros gerados (JSON + CSV) — não versionado
├── tests/
│   └── codigo_postal_rua.py         # Testes isolados
├── pyproject.toml
└── README.md
```

---

## Entidades Geradas

A geração segue a ordem de dependências — entidades sem dependências são criadas primeiro, as que referenciam outras são criadas depois.

| Ordem | Entidade | Quantidade | Dependências |
|-------|----------|-----------|--------------|
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
| 11 | `Bens_E_Servicos` | 50 | — |
| 12 | `Pedido` | 100 | Entidade |
| 13 | `Pedido_Bens_E_Servicos` | 150 | Pedido + Bens_E_Servicos |
| 14 | `Bens_E_Servicos_Negocio` | 100 | Negocio + Bens_E_Servicos |
| 15 | `Lead` | 100 | Painel + Pedido + Locker + Cidadao |

### Notas de geração

**Localidade** — os códigos postais são gerados com `faker.postcode()` (locale `pt_PT`) e validados contra a base GeoNames via [pgeocode](https://pgeocode.readthedocs.io/). Códigos inválidos são descartados e regenerados. As coordenadas geográficas reais ficam disponíveis internamente (prefixo `_`) para uso por outras entidades, mas não são exportadas nesta tabela.

**NIFs/NIPCs** — cada entidade gera o seu próprio identificador fiscal com o prefixo correto:
- `Mecena`: `1`, `2`, `5` ou `9` (maioria `9` — pessoas coletivas)
- `Negocio`: `5` ou `9` (maioria `9` — empresas privadas)
- `Instituicao`: `5` ou `9` (entidades públicas e coletivas sem fins lucrativos)

**Entidade** — não gera NIFs próprios. Agrega os NIFs já gerados por `Mecena`, `Negocio` e `Instituicao`, e cria para cada um o `email_login` (formato `primeiro.ultimo@dominio` para pessoas, `nomedaorganizacao@dominio` para organizações), `password`, `iban` e `codigo_postal`.

---

## Pré-requisitos

- Python 3.11+
- Node.js 18+ (para os models Sequelize)

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
localidades = generate_localidades(n=100)   # alterar n
mecenas     = generate_mecenas(n=50)
doacoes     = generate_doacoes(n=200, mecenas=mecenas)
# ...
```

---

## Output

Após a execução, a pasta `output/` contém um par de ficheiros por entidade:

```
output/
├── localidade.json / localidade.csv
├── entidade.json   / entidade.csv
├── mecena.json     / mecena.csv
├── doacao.json     / doacao.csv
├── negocio.json    / negocio.csv
├── instituicao.json / instituicao.csv
├── contacto.json   / contacto.csv
├── pedido.json     / pedido.csv
├── bens_servicos.json / bens_servicos.csv
├── pedido_bens_servicos.json / pedido_bens_servicos.csv
├── bens_servicos_negocio.json / bens_servicos_negocio.csv
├── painel_digital.json / painel_digital.csv
├── locker.json     / locker.csv
├── cidadao.json    / cidadao.csv
└── lead.json       / lead.csv
```

A pasta `output/` está no `.gitignore` — os ficheiros gerados não são versionados.

---

## Migração para a Base de Dados

Os ficheiros JSON gerados podem ser consumidos pelos seeders Sequelize para popular a base de dados MySQL. O padrão de importação em cada seeder é:

```javascript
const data = require('../../output/localidade.json');
await Localidade.bulkCreate(data, { ignoreDuplicates: true });
```

A ordem de inserção deve respeitar as foreign keys — a mesma ordem da tabela de entidades acima.

Os models Sequelize estão na pasta `models/` e a configuração da ligação à base de dados em `config/database.js`.