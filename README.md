<div align="center">
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

Este repositório é responsável pela **geração de dados sintéticos realistas** para popular as bases de dados do SAM em ambiente de desenvolvimento e testes. Os dados são gerados em Python com a biblioteca [Faker](https://faker.readthedocs.io/) (locale `pt_PT`) e exportados em formato **JSON** e **CSV**, prontos a ser injetados via seeders Sequelize (MySQL) e Mongoose (MongoDB).

Os dados cobrem as duas bases de dados do projeto:

- **MySQL** — dados relacionais e transacionais: entidades, doações, pedidos, lockers, painéis digitais, etc.
- **MongoDB** — dados de alto volume e estrutura variável: telemetria IoT, auditoria financeira, logs de interação, notificações e vouchers.

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

A interoperabilidade é assegurada pela camada de aplicação: os documentos MongoDB armazenam os identificadores únicos das entidades SQL, permitindo cruzamento de informação quando necessário.

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
| 5     | `Entidade`                | 150            | Mecena + Negocio + Instituicao     |
| 6     | `Contacto`                | 150            | Entidade                           |
| 7     | `Doacao`                  | 200            | Mecena                             |
| 8     | `Painel_Digital`          | 30             | Localidade                         |
| 9     | `Locker_Inteligente`      | 30             | Localidade                         |
| 10    | `Cidadao`                 | 100            | —                                  |
| 11    | `Bens_E_Servicos`         | ~73 (estático) | —                                  |
| 12    | `Pedido`                  | 100            | Entidade                           |
| 13    | `Pedido_Bens_E_Servicos`  | 150            | Pedido + Bens_E_Servicos           |
| 14    | `Bens_E_Servicos_Negocio` | 100            | Negocio + Bens_E_Servicos          |
| 15    | `Lead`                    | 100            | Painel + Pedido + Locker + Cidadao |

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

**Localidade** — os códigos postais são gerados com `faker.postcode()` e validados contra a base GeoNames via [pgeocode](https://pgeocode.readthedocs.io/). Códigos inválidos são descartados e regenerados. As coordenadas geográficas reais ficam disponíveis internamente (prefixo `_`) para uso por outras entidades, mas não são exportadas.

**NIFs/NIPCs** — cada entidade gera o seu próprio identificador fiscal com o prefixo correto:

- `Mecena`: `1`, `2`, `5` ou `9` (maioria `9` — pessoas coletivas)
- `Negocio`: `5` ou `9` (maioria `9` — empresas privadas)
- `Instituicao`: `5` ou `9` (entidades públicas e coletivas sem fins lucrativos)

**Entidade** — não gera NIFs próprios. Agrega os NIFs de `Mecena`, `Negocio` e `Instituicao` e cria o `email_login` (formato `primeiro.ultimo@dominio` para pessoas, `nomedaorganizacao@dominio` para organizações), `password`, `iban` e endereço para cada um.

**Bens_E_Servicos** — geração estática a partir de dois dicionários: `BENS_POR_CATEGORIA` e `SERVICOS_POR_CATEGORIA`. Cada entrada é única e serve como PK da tabela. O campo `tipo_bem` mapeia para o ENUM do model: `"bem"` ou `"servico"`.

**Cidadao** — o campo `reason` só é gerado quando `blocked = 1`; cidadãos não bloqueados não têm motivo de bloqueio.

**Lead** — referencia apenas pedidos cujo `tipo_bem_servico` corresponde a um item com `tipo_bem = "bem"`. Serviços podem existir em `Pedido_Bens_Servicos`, mas não são escolhidos para gerar leads.

**Financial_Log** — cada doação gera exatamente um log financeiro, partilhando a mesma data. Garante cobertura total de auditoria sem registos órfãos.

**Datas** — geradas dinamicamente com base em `datetime.now()` (data do seed), com distribuição mista: 30 % concentradas nas últimas 2 semanas, 70 % espalhadas organicamente ao longo de 2 anos.

---

## Stack Tecnológica

### Geração de dados — Python

| Tecnologia                                   | Versão | Para quê                                               |
| -------------------------------------------- | ------ | ------------------------------------------------------ |
| [Python](https://www.python.org/)            | 3.10+  | Linguagem principal                                    |
| [Faker](https://faker.readthedocs.io/)       | —      | Geração de dados sintéticos realistas (locale `pt_PT`) |
| [pgeocode](https://pgeocode.readthedocs.io/) | —      | Validação de códigos postais e geocoordenadas          |
| [SQLAlchemy](https://www.sqlalchemy.org/)    | —      | Dependência de exportação                              |
| [PyYAML](https://pyyaml.org/)                | —      | Dependência de configuração                            |

### Seeders e base de dados — Node.js

| Tecnologia                                          | Versão | Para quê                              |
| --------------------------------------------------- | ------ | ------------------------------------- |
| [Node.js](https://nodejs.org/)                      | 18+    | Runtime para os seeders               |
| [Sequelize](https://sequelize.org/) + sequelize-cli | 6      | ORM, migrations e seeder SQL          |
| [Mongoose](https://mongoosejs.com/)                 | 8      | ODM e seeder NoSQL                    |
| [mysql2](https://github.com/sidorares/node-mysql2)  | 3      | Driver MySQL para o Sequelize         |
| [dotenv](https://github.com/motdotla/dotenv)        | —      | Carregamento de variáveis de ambiente |

---

## Estrutura do Repositório

```
p2-SAM-data-generator/
├── p2_sam/
│   ├── __main__.py                        # Ponto de entrada — orquestra toda a geração
│   ├── utils/
│   │   └── dates.py                       # Distribuição temporal orgânica partilhada
│   ├── entities/
│   │   ├── localidade/                    # Geradores SQL
│   │   ├── entidade/
│   │   ├── mecena/
│   │   ├── doacao/
│   │   ├── negocio/
│   │   ├── instituicao/
│   │   ├── contacto/
│   │   ├── pedido/
│   │   ├── bens_servicos/
│   │   ├── painel_digital/
│   │   ├── locker/
│   │   ├── cidadao/
│   │   ├── lead/
│   │   └── nosql/                         # Geradores MongoDB
│   ├── exporters/
│   │   ├── csv_exporter.py
│   │   ├── json_exporter.py
│   │   └── mongodb_exporter.py
│   └── database/
│       ├── models/                        # Models Sequelize (MySQL)
│       ├── migrations/                    # Migrations Sequelize (MySQL)
│       ├── seeders/
│       │   ├── seed_sql_from_output.js    # Importa output/*.json para MySQL
│       │   └── seed_nosql_from_output.js  # Importa output/nosql_*.json para MongoDB
│       ├── nosql/
│       │   ├── connections.js             # Ligação MongoDB/Mongoose
│       │   └── schemas/                   # Schemas Mongoose
│       ├── config/
│       │   └── database.js                # Configuração Sequelize
│       └── package.json                   # Scripts npm de seed
├── output/                                # Ficheiros gerados (JSON + CSV) — não versionado
├── tests/
│   └── codigo_postal_rua.py
├── pyproject.toml
└── README.md
```

---

## Instalação

### Pré-requisitos

- [Python](https://www.python.org/) >= 3.10
- [Node.js](https://nodejs.org/) >= 18
- MySQL 8 (para importar os dados SQL)
- MongoDB 7 (para importar os dados NoSQL)

### Passos

```bash
git clone https://github.com/amorima/p2-SAM-data-generator.git
cd p2-SAM-data-generator

# Criar e ativar ambiente virtual
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

```bash
# Ativar o ambiente virtual (se ainda não estiver ativo)
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows

# Correr o gerador completo
python -m p2_sam
```

O terminal mostra o progresso da geração de cada entidade. Para alterar as quantidades, editar as chamadas em `p2_sam/__main__.py`:

```python
localidades = generate_localidades(n=100)
mecenas     = generate_mecenas(n=50)
doacoes     = generate_doacoes(n=200, mecenas=mecenas)
# ...
```

---

## Output

Após a execução, a pasta `output/` contém os ficheiros gerados:

```
output/
├── # MySQL — par JSON + CSV por entidade
├── localidade.json            / localidade.csv
├── entidade.json              / entidade.csv
├── mecena.json                / mecena.csv
├── doacao.json                / doacao.csv
├── negocio.json               / negocio.csv
├── instituicao.json           / instituicao.csv
├── contacto.json              / contacto.csv
├── pedido.json                / pedido.csv
├── bens_servicos.json         / bens_servicos.csv
├── pedido_bens_servicos.json  / pedido_bens_servicos.csv
├── bens_servicos_negocio.json / bens_servicos_negocio.csv
├── painel_digital.json        / painel_digital.csv
├── locker.json                / locker.csv
├── cidadao.json               / cidadao.csv
├── lead.json                  / lead.csv
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

## Importação para a Base de Dados

Antes de importar, gerar os ficheiros em `output/`:

```bash
python -m p2_sam
```

### 1. Configurar a chave SSH (apenas uma vez)

O MySQL e o MongoDB não estão expostos diretamente — o acesso é feito via **túnel SSH**. Para evitar introduzir a password em cada sessão, usa autenticação por chave.

Correr no **PowerShell do Windows** (não no WSL):

```powershell
# Gerar a chave dedicada para o tunnel SAM
ssh-keygen -t ed25519 -f "$HOME\.ssh\sam_tunnel" -C "sam-seed-tunnel"

# Registar a chave pública no servidor (pede a password uma última vez)
Get-Content "$HOME\.ssh\sam_tunnel.pub" | ssh utilizador@servidor "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

### 2. Abrir o túnel (MySQL + MongoDB numa ligação)

Num terminal **PowerShell** separado, abrir ambas as portas de uma vez:

```powershell
ssh -i "$HOME\.ssh\sam_tunnel" -L 3307:localhost:3306 -L 27018:localhost:27017 utilizador@servidor -N
```

O `-N` mantém o túnel ativo sem executar comandos. Não fechar este terminal durante a importação.

### 3. Configurar o `.env`

Criar (ou editar) o ficheiro `.env` na raiz do repositório:

```env
# MySQL
DB_HOST=127.0.0.1
DB_PORT=3307
DB_NAME=nome_da_base
DB_USER=utilizador
DB_PASSWORD=password

# MongoDB
MONGODB_URI=mongodb://127.0.0.1:27018/nome_da_base_mongo
MONGODB_DB_NAME=nome_da_base_mongo
MONGODB_USER=utilizador
MONGODB_PASSWORD=password
MONGODB_AUTH_SOURCE=nome_da_base_mongo
```

### 4. Correr as migrations e os seeders

```bash
cd p2_sam/database

# Criar as tabelas (só necessário na primeira vez)
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

## Variáveis de Ambiente

| Variável              | Descrição                                         |
| --------------------- | ------------------------------------------------- |
| `DB_USER`             | Utilizador MySQL                                  |
| `DB_PASSWORD`         | Password MySQL                                    |
| `DB_NAME`             | Nome da base de dados MySQL                       |
| `DB_HOST`             | Host MySQL (por defeito `127.0.0.1`)              |
| `MONGODB_URI`         | URI de ligação ao MongoDB                         |
| `MONGODB_DB_NAME`     | Nome da base de dados MongoDB                     |
| `MONGODB_USER`        | Utilizador MongoDB                                |
| `MONGODB_PASSWORD`    | Password MongoDB                                  |
| `MONGODB_AUTH_SOURCE` | Base de dados de autenticação MongoDB             |
| `SEED_CLEAR`          | `true` (padrão) — limpa os dados antes de inserir |
| `OUTPUT_DIR`          | Caminho alternativo para a pasta `output/`        |

---

## Outros Repositórios

| Repositório                                                               | Descrição                                |
| ------------------------------------------------------------------------- | ---------------------------------------- |
| [p2-sam-frontend](https://github.com/amorima/p2-sam-frontend)             | Front-end da plataforma (Nuxt 4 + Vue 3) |
| [p2-sam-backend](https://github.com/amorima/p2-sam-backend)               | API REST e base de dados                 |
| [p2-SAM-data-generator](https://github.com/amorima/p2-SAM-data-generator) | Este repositório                         |

---

## Estado do Projeto

- [x] Geração de 15 entidades MySQL com dependências ordenadas
- [x] Geração de 5 coleções MongoDB com referências a PKs SQL
- [x] Exportação para JSON e CSV
- [x] Seeder SQL via Sequelize com suporte a migrations
- [x] Seeder NoSQL via Mongoose com schemas validados
- [x] Distribuição temporal orgânica com concentração nas últimas 2 semanas
- [x] Validação de códigos postais reais via GeoNames / pgeocode
- [ ] Testes unitários para os geradores

---

<div align="center">
  <sub>Desenvolvido para fins académicos · ESMAD - Politécnico do Porto · 2024/2025</sub>
</div>
