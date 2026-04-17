// database/models/index.js
const { Sequelize } = require("sequelize");
const config = require("../config/database.js");

const sequelize = new Sequelize(config);

// Importar todos os models
const Entidade = require("./entidade.js")(sequelize);
const Mecena = require("./mecenas.js")(sequelize);
const Doacao = require("./doacao.js")(sequelize);
const Contacto = require("./contacto.js")(sequelize);
const Instituicao = require("./instituicao.js")(sequelize);
const Localidade = require("./localidade.js")(sequelize);
const Negocio = require("./negocios.js")(sequelize);
const Localidade_Entidade = require("./localidade_entidade.js")(sequelize);
const Bens_E_Servico = require("./bens_e_servico.js")(sequelize);
const Locker_Inteligente = require("./locker_inteligente.js")(sequelize);
const Bens_E_Servicos_Negocio = require("./bens_e_servicos_negocio.js")(
 sequelize
);
const Pedido = require("./pedido.js")(sequelize);
const Pedido_Bens_E_Servicos = require("./pedido_bens_e_servicos.js")(
 sequelize
);
const Lead = require("./lead.js")(sequelize);
const Painel = require("./painel.js")(sequelize);

const models = {
 Entidade,
 Mecena,
 Doacao,
 Contacto,
 Instituicao,
 Localidade,
 Negocio,
 Localidade_Entidade,
 Bens_E_Servico,
 Bens_E_Servicos_Negocio,
 Pedido,
 Pedido_Bens_E_Servicos,
 Lead,
 Locker_Inteligente,
 Painel,
};

// Chamar os associate de cada model
Object.values(models).forEach((model) => {
 if (model.associate) model.associate(models);
});

module.exports = { sequelize, ...models };
