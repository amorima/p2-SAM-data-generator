<div align="center">
  <img src="https://sam.netdw.tech/logo_big.svg" alt="SAM - Sistema de Apoio Municipal" width="160" />

  <h1>SAM — Gerador de Dados Sintéticos</h1>
  <p><em>Geração e injeção de dados realistas para o projeto Sistema de Apoio Municipal</em></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+" />
    <img src="https://img.shields.io/badge/Faker-pt__PT-FF6B6B?style=for-the-badge&logo=python&logoColor=white" alt="Faker pt_PT" />
    <img src="https://img.shields.io/badge/Node.js-18+-339933?style=for-the-badge&logo=node.js&logoColor=white" alt="Node.js 18+" />
    <img src="https://img.shields.io/badge/Sequelize-6-52B0E7?style=for-the-badge&logo=sequelize&logoColor=white" alt="Sequelize 6" />
    <img src="https://img.shields.io/badge/Mongoose-8-880000?style=for-the-badge&logo=mongodb&logoColor=white" alt="Mongoose 8" />
    <img src="https://img.shields.io/badge/MySQL-8-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL 8" />
    <img src="https://img.shields.io/badge/MongoDB-7-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB 7" />
  </p>

  <p>
    <a href="https://github.com/amorima/p2-sam-frontend">
      <img src="https://img.shields.io/badge/GitHub-Front--end-181717?style=flat-square&logo=github" alt="Repositório Front-end" />
    </a>
    <a href="https://github.com/amorima/p2-sam-backend">
      <img src="https://img.shields.io/badge/GitHub-Back--end-181717?style=flat-square&logo=github" alt="Repositório Back-end" />
    </a>
    <a href="https://github.com/amorima/p2-SAM-data-generator">
      <img src="https://img.shields.io/badge/GitHub-Gerador_de_Dados-181717?style=flat-square&logo=github" alt="Repositório Data Generator" />
    </a>
  </p>
</div>

---

## Contexto Académico

Projeto Interdisciplinar WebPII desenvolvido no âmbito da:

> **Licenciatura em Tecnologias e Sistemas de Informação para a Web**  
> Escola Superior de Media Artes e Design (ESMAD)  
> Politécnico do Porto

Unidades curriculares envolvidas:

| Unidade Curricular       | Âmbito no projeto                                         |
| ------------------------ | --------------------------------------------------------- |
| Engenharia de Software   | Arquitetura, modelação e boas práticas de desenvolvimento |
| Base de Dados            | Modelação de dados, esquema relacional e persistência     |
| Programação Web II       | Implementação do back-end e integração com API REST       |
| Projeto II               | Gestão de projeto, documentação e entrega                 |
| Testes e Performance Web | Testes funcionais, de performance e de usabilidade        |

### Docentes

- Prof. Doutor Lino Rui dos Santos Oliveira
- Prof. Manuel Jorge de Abreu Antunes Lima
- Prof. Diogo Filipe de Bastos Sousa Ribeiro
- Prof.ª Inês Sofia Antunes Moura Reis
- Prof.ª Viviana da Costa Neto Henriques
- Prof.ª Doutora Teresa Cristina de Sousa Azevedo Terroso
- Prof. António Francisco da Costa Machado

---

## Sobre o Projeto

Este repositório é responsável pela **geração de dados sintéticos realistas** para popular as bases de dados do SAM em ambiente de desenvolvimento e testes. Os dados são gerados em Python com a biblioteca [Faker](https://faker.readthedocs.io/) (locale `pt_PT`) e exportados em formato **JSON** e **CSV**, prontos a ser injetados via seeders Node.js que usam Sequelize (MySQL) e Mongoose (MongoDB).

O processo é dividido em duas fases:

1. **Geração** — Python produz os dados em memória, respeitando a ordem das dependências entre entidades, e exporta para `output/`
2. **Injeção** — Node.js lê os ficheiros `output/*.json` e injeta-os nas bases de dados via Sequelize (SQL) e Mongoose (NoSQL)

---

## Arquitetura de Dados

O SAM usa uma arquitetura híbrida com duas bases de dados:

```
Dispositivos IoT / Frontend Web
           │
    Backend / API SAM
     ┌──────┴──────┐
   MySQL        MongoDB
(estruturado) (não estruturado)
```

**MySQL** armazena dados transacionais e de negócio: entidades, mecenas, doações, pedidos, lockers e painéis.

**MongoDB** armazena dados de alto volume e estrutura variável: telemetria IoT, auditoria de pagamentos, logs de comportamento nos painéis digitais, notificações e vouchers.

A interoperabilidade é assegurada pela camada de aplicação: os documentos MongoDB armazenam os identificadores únicos das entidades SQL, permitindo cruzamento de informação.

---

## Entidades Geradas

### MySQL

A geração segue a ordem das dependências — entidades sem dependências são criadas primeiro.

| Ordem | Entidade                  | Quantidade     | Dependências                       |
| ----- | ------------------------- | -------------- | ---------------------------------- |
| 1     | `Localidade`              | 100            | —                                  |
| 2     | `Mecena`                  | 50             | —                                  |
| 3     | `Negocio`                 | 50             | Localidade                         |
| 4     | `Instituicao`             | 50             | Localidade                         |
| 5     | `Entidade`                | 150 + fixtures | Mecena + Negocio + Instituicao     |
| 6     | `Localidade_Entidade`     | 150            | Entidade + Localidade              |
| 7     | `Contacto`                | 150            | Entidade                           |
| 8     | `Doacao`                  | 200            | Mecena                             |
| 9     | `Painel_Digital`          | 30             | Localidade                         |
| 10    | `Locker_Inteligente`      | 30             | Localidade                         |
| 11    | `Cidadao`                 | 100            | —                                  |
| 12    | `Bens_E_Servicos`         | ~73 (estático) | —                                  |
| 13    | `Pedido`                  | 100            | Entidade                           |
| 14    | `Pedido_Bens_E_Servicos`  | 150            | Pedido + Bens_E_Servicos           |
| 15    | `Bens_E_Servicos_Negocio` | 100            | Negocio + Bens_E_Servicos          |
| 16    | `Lead`                    | 100            | Painel + Pedido + Locker + Cidadao |

### MongoDB

As coleções NoSQL são geradas após toda a geração SQL, pois referenciam PKs das tabelas relacionais.

| Coleção            | Quantidade         | Referência SQL                                           |
| ------------------ | ------------------ | -------------------------------------------------------- |
| `locker_telemetry` | 200                | `locker_inteligente.id_locker` / `painel.id_dispositivo` |
| `financial_log`    | 1 por doação (200) | `doacao.id_doacao`                                       |
| `interaction_log`  | 300                | `painel.id_dispositivo`                                  |
| `notification`     | 150                | `leads.id_lead`                                          |
| `vouchers`         | 100                | `entidade.nif_nipc` + `negocio.nif_nipc`                 |

---

## Notas de Geração

**Localidade** — os códigos postais são gerados com `faker.postcode()` e validados contra a base GeoNames via [pgeocode](https://pgeocode.readthedocs.io/). Códigos inválidos são descartados e regenerados. As coordenadas geográficas ficam disponíveis internamente (prefixo `_`) para uso por outras entidades, mas não são exportadas.

**NIFs/NIPCs** — cada entidade gera o seu próprio identificador fiscal com o prefixo correto:

- `Mecena`: `1`, `2`, `5` ou `9` (maioria `9` — pessoas coletivas)
- `Negocio`: `5` ou `9` (maioria `9` — empresas privadas)
- `Instituicao`: `5` ou `9` (entidades públicas e coletivas sem fins lucrativos)

**Entidade** — não gera NIFs próprios. Agrega os NIFs de `Mecena`, `Negocio` e `Instituicao` e cria o `email_login` (formato `primeiro.ultimo@dominio` para pessoas, `nomedaorganizacao@dominio` para organizações), `password`, `iban` e endereço para cada um.

**Bens_E_Servicos** — geração estática a partir de dois dicionários: `BENS_POR_CATEGORIA` e `SERVICOS_POR_CATEGORIA`. Cada entrada é única e serve como PK da tabela. O campo `tipo_bem` mapeia para o ENUM do model: `"bem"` ou `"servico"`.

**Lead** — referencia apenas pedidos cujo `tipo_bem_servico` corresponde a um item com `tipo_bem = "bem"`. Serviços podem existir em `Pedido_Bens_Servicos`, mas não são escolhidos para gerar leads.

**Financial_Log** — cada doação gera exatamente um log financeiro, partilhando a mesma data. Garante cobertura total de auditoria sem registos órfãos.

**Datas** — geradas dinamicamente com base em `datetime.now()` (data do seed), com distribuição mista: 30 % concentradas nas últimas 2 semanas, 70 % espalhadas organicamente ao longo de 2 anos.

---

## Fixtures de Teste

O seeder injeta automaticamente entidades com NIFs fixos para suporte às coleções Postman e testes de integração. As passwords são hasheadas com bcrypt (10 rounds) durante o seeding.

| NIF         | Role          | Email                       | Password           |
| ----------- | ------------- | --------------------------- | ------------------ |
| `199999999` | `patron`      | `test.patron@sam.pt`        | `Test@Patron1`     |
| `599999997` | `business`    | `test.business@sam.pt`      | `Empresa@2024`     |
| `599999998` | `institution` | `test.institution@sam.pt`   | `Test@Institution1` |

O administrador é criado com os valores das variáveis `ADMIN_NIF`, `ADMIN_EMAIL` e `ADMIN_PASSWORD` definidas no `.env`.

Existe também um bem/serviço de tipo fixo (`ZZZ_Teste_Chain`) e um pedido PENDENTE associado à instituição `599999998`, garantindo um fluxo de aprovação completo e reprodutível nos testes.

---

## Stack Tecnológica

### Geração de dados — Python

| Tecnologia                                   | Versão | Para quê                                               |
| -------------------------------------------- | ------ | ------------------------------------------------------ |
| [Python](https://www.python.org/)            | 3.10+  | Linguagem principal                                    |
| [Faker](https://faker.readthedocs.io/)       | —      | Geração de dados sintéticos realistas (locale `pt_PT`) |
| [pgeocode](https://pgeocode.readthedocs.io/) | —      | Validação de códigos postais e geocoordenadas reais    |
| [SQLAlchemy](https://www.sqlalchemy.org/)    | —      | Dependência transitiva dos exporters                   |
| [PyYAML](https://pyyaml.org/)                | —      | Dependência transitiva de configuração                 |

### Seeders e base de dados — Node.js

| Tecnologia                                          | Versão | Para quê                                     |
| --------------------------------------------------- | ------ | -------------------------------------------- |
| [Node.js](https://nodejs.org/)                      | 18+    | Runtime para os seeders                      |
| [Sequelize](https://sequelize.org/) + sequelize-cli | 6      | ORM, migrations e seeder SQL (MySQL)         |
| [Mongoose](https://mongoosejs.com/)                 | 8      | ODM e seeder NoSQL (MongoDB)                 |
| [mysql2](https://github.com/sidorares/node-mysql2)  | 3      | Driver MySQL para o Sequelize                |
| [bcryptjs](https://github.com/dcodeIO/bcrypt.js)    | 2      | Hash de passwords nas fixtures de teste      |
| [dotenv](https://github.com/motdotla/dotenv)        | —      | Carregamento de variáveis de ambiente        |

---

## Estrutura do Repositório

```
p2-SAM-data-generator/
├── p2_sam/
│   ├── __main__.py                        # Ponto de entrada — orquestra toda a geração
│   ├── utils/
│   │   └── dates.py                       # Distribuição temporal orgânica partilhada
│   ├── entities/
│   │   ├── localidade/generator.py        # Validação de código postal via pgeocode
│   │   ├── doacao/generator.py            # Gera NIFs de mecenas e doações
│   │   ├── negocio/generator.py           # Empresas parceiras com localização geográfica
│   │   ├── instituicao/generator.py       # Instituições sociais com coordenadas GPS
│   │   ├── entidade/generator.py          # Agrega todos os NIFs em registos de entidade
│   │   ├── contacto/generator.py          # Contactos únicos por entidade
│   │   ├── localidade_entidade/           # Relação entidade → localidade
│   │   ├── painel_digital/generator.py    # Quiosques com coordenadas geográficas
│   │   ├── locker/generator.py            # Cacifos inteligentes com código único
│   │   ├── cidadao/generator.py           # Cidadãos com contacto e fixture Postman
│   │   ├── bens_servicos/generator.py     # Catálogo estático de bens e serviços
│   │   ├── pedido/generator.py            # Pedidos de necessidade com distribuição de estados
│   │   ├── pedido_bens_servico/           # Itens por pedido (apenas bens físicos para leads)
│   │   ├── bens_e_servicos_negocio/       # Ofertas de negócios com desconto realista
│   │   ├── lead/generator.py              # Leads (reservas de bens do painel)
│   │   └── nosql/
│   │       ├── locker_telemetry/          # Telemetria IoT de lockers e painéis
│   │       ├── financial/                 # Logs de auditoria de pagamentos (1 por doação)
│   │       ├── interaction/               # Sessões de navegação no painel do cidadão
│   │       ├── notification/              # Notificações enviadas aos utilizadores
│   │       └── voucher/                   # Vouchers emitidos por entidades
│   ├── exporters/
│   │   ├── csv_exporter.py                # Exportação para CSV (tabelas SQL)
│   │   ├── json_exporter.py               # Exportação para JSON (SQL + NoSQL)
│   │   └── mongodb_exporter.py            # Exportação para JSON com prefixo nosql_
│   └── database/
│       ├── config/database.js             # Configuração Sequelize (MySQL)
│       ├── models/                        # 15 models Sequelize
│       ├── migrations/                    # 32 migrations Sequelize (schema completo)
│       ├── seeders/
│       │   ├── seed_sql_from_output.js    # Importa output/*.json para MySQL
│       │   └── seed_nosql_from_output.js  # Importa output/nosql_*.json para MongoDB
│       ├── nosql/
│       │   ├── connections.js             # Ligação MongoDB/Mongoose
│       │   └── schemas/                   # 5 schemas Mongoose com índices
│       └── package.json                   # Scripts npm de seed
├── output/                                # Ficheiros gerados (JSON + CSV) — não versionado
├── pyproject.toml                         # Dependências Python
└── .env.example                           # Template de variáveis de ambiente
```

---

## Instalação

### Pré-requisitos

- [Python](https://www.python.org/) >= 3.10
- [Node.js](https://nodejs.org/) >= 18
- MySQL 8 acessível (local ou via túnel SSH)
- MongoDB 7 acessível (local ou via túnel SSH)

### Passos

```bash
git clone https://github.com/amorima/p2-SAM-data-generator.git
cd p2-SAM-data-generator

# Criar e ativar ambiente virtual Python
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows

# Instalar dependências Python
pip install -e .

# Instalar dependências Node (seeders)
cd p2_sam/database
npm install
cd ../..
```

---

## Utilização

### 1. Gerar os dados

```bash
# Ativar o ambiente virtual (se ainda não estiver ativo)
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows

python -m p2_sam
```

O terminal mostra o progresso passo a passo (21 etapas). Para alterar as quantidades, editar as chamadas em `p2_sam/__main__.py`:

```python
localidades = generate_localidades(n=100)
mecenas     = generate_mecenas(n=50)
doacoes     = generate_doacoes(n=200, mecenas=mecenas)
# ...
```

### 2. Importar para a base de dados

#### 2a. Configurar o `.env`

Criar (ou editar) o ficheiro `.env` na raiz do repositório (ver [Variáveis de Ambiente](#variáveis-de-ambiente)).

#### 2b. Abrir o túnel SSH (se as bases de dados forem remotas)

O MySQL e o MongoDB não estão expostos diretamente — o acesso é feito via **túnel SSH**. Para autenticação por chave (sem password em cada sessão):

```powershell
# Gerar a chave dedicada (apenas uma vez)
ssh-keygen -t ed25519 -f "$HOME\.ssh\sam_tunnel" -C "sam-seed-tunnel"

# Registar a chave no servidor (pede a password uma última vez)
Get-Content "$HOME\.ssh\sam_tunnel.pub" | ssh utilizador@servidor "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

Num terminal separado, abrir ambas as portas:

```powershell
ssh -i "$HOME\.ssh\sam_tunnel" -L 3307:localhost:3306 -L 27018:localhost:27017 utilizador@servidor -N
```

O `-N` mantém o túnel ativo sem executar comandos. Não fechar este terminal durante a importação.

#### 2c. Correr as migrations e os seeders

```bash
cd p2_sam/database

# Criar as tabelas (só necessário na primeira vez ou após reset)
npx sequelize-cli db:migrate

# Importar SQL e NoSQL em sequência
npm run seed:all
```

Ou separadamente:

```bash
npm run seed:sql    # apenas MySQL
npm run seed:nosql  # apenas MongoDB
```

Por defeito, os dados existentes são limpos antes de cada importação. Para inserir sem limpar:

```bash
SEED_CLEAR=false npm run seed:all
```

---

## Output

Após a execução do gerador, a pasta `output/` contém:

```
output/
├── # MySQL — par JSON + CSV por entidade
├── localidade.json / .csv
├── entidade.json / .csv
├── negocio.json / .csv
├── instituicao.json / .csv
├── contacto.json / .csv
├── doacao.json / .csv
├── painel_digital.json / .csv
├── locker.json / .csv
├── cidadao.json / .csv
├── bens_servicos.json / .csv
├── pedido.json / .csv
├── pedido_bens_servicos.json / .csv
├── bens_servicos_negocio.json / .csv
├── lead.json / .csv
├── localidade_entidade.json / .csv
│
└── # MongoDB — apenas JSON, prefixado com nosql_
    ├── nosql_locker_telemetry.json
    ├── nosql_financial_log.json
    ├── nosql_interaction_log.json
    ├── nosql_notification.json
    └── nosql_vouchers.json
```

> A pasta `output/` está no `.gitignore` — os ficheiros gerados não são versionados.

---

## Variáveis de Ambiente

| Variável              | Descrição                                                                |
| --------------------- | ------------------------------------------------------------------------ |
| `DB_HOST`             | Host MySQL (por defeito `127.0.0.1`)                                     |
| `DB_PORT`             | Porta MySQL (por defeito `3306`; usar `3307` quando acedido via túnel)   |
| `DB_NAME`             | Nome da base de dados MySQL                                              |
| `DB_USER`             | Utilizador MySQL                                                         |
| `DB_PASSWORD`         | Password MySQL                                                           |
| `DB_DIALECT`          | Dialecto Sequelize — usar `mysql`                                        |
| `MONGODB_URI`         | URI de ligação ao MongoDB (ex: `mongodb://127.0.0.1:27018/nome_bd`)      |
| `MONGODB_DB_NAME`     | Nome da base de dados MongoDB                                            |
| `MONGODB_USER`        | Utilizador MongoDB                                                       |
| `MONGODB_PASSWORD`    | Password MongoDB                                                         |
| `MONGODB_AUTH_SOURCE` | Base de dados de autenticação MongoDB                                    |
| `ADMIN_NIF`           | NIF do administrador a criar no seed                                     |
| `ADMIN_EMAIL`         | Email de login do administrador                                          |
| `ADMIN_PASSWORD`      | Password do administrador (em texto simples — é hasheada pelo seeder)   |
| `ADMIN_NAME`          | Nome do administrador (por defeito `Administrador SAM`)                  |
| `SEED_CLEAR`          | `true` (padrão) — limpa os dados antes de inserir; `false` para acumular |
| `OUTPUT_DIR`          | Caminho alternativo para a pasta `output/`                               |

---

## Outros Repositórios

| Repositório                                                               | Descrição                               |
| ------------------------------------------------------------------------- | --------------------------------------- |
| [p2-sam-frontend](https://github.com/amorima/p2-sam-frontend)             | Front-end da plataforma (Nuxt 4 + Vue 3)|
| [p2-sam-backend](https://github.com/amorima/p2-sam-backend)               | API REST (Express + MySQL + MongoDB)    |
| [p2-SAM-data-generator](https://github.com/amorima/p2-SAM-data-generator) | Este repositório                        |

---

## Estado do Projeto

- [x] Geração de 16 entidades MySQL com dependências ordenadas (21 etapas)
- [x] Geração de 5 coleções MongoDB com referências a PKs SQL
- [x] Exportação para JSON e CSV
- [x] Seeder SQL via Sequelize com suporte a migrations (32 migrations)
- [x] Seeder NoSQL via Mongoose com schemas e índices validados
- [x] Fixtures de teste com NIFs fixos para as coleções Postman
- [x] Hash de passwords de fixtures com bcrypt no seeder
- [x] Distribuição temporal orgânica com concentração nas últimas 2 semanas
- [x] Validação de códigos postais reais via GeoNames / pgeocode
- [x] Suporte a re-seed sem limpeza (`SEED_CLEAR=false`)

---

<div align="center">
  <sub>Desenvolvido para fins académicos · ESMAD - Politécnico do Porto · 2025/2026</sub>
</div>
