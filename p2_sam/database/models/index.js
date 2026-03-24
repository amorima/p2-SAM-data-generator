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

const models = { Entidade, Mecena, Doacao, Contacto, Instituicao, Localidade };

// Chamar os associate de cada model
Object.values(models).forEach((model) => {
 if (model.associate) model.associate(models);
});

module.exports = { sequelize, ...models };
