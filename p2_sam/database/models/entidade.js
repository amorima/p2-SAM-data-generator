const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const Entidade = sequelize.define(
  "Entidade",
  {
   nif_nipc: {
    type: DataTypes.STRING(9),
    primaryKey: true,
    allowNull: false,
   },
   email_login: {
    type: DataTypes.STRING(45),
    allowNull: false,
    unique: true,
   },
   password: {
    type: DataTypes.STRING(255),
    allowNull: false,
   },
   nome_entidade: {
    type: DataTypes.STRING(45),
    allowNull: false,
   },
   iban: {
    type: DataTypes.STRING(23),
    allowNull: true,
    unique: true,
   },
   codigo_postal: {
    type: DataTypes.STRING(8),
    allowNull: false,
   },
   profile_pic: {
    type: DataTypes.STRING(255),
    allowNull: true,
   },
   role: {
    type: DataTypes.ENUM("patron", "business", "institution", "admin"),
    allowNull: false,
   },
  },
  {
   tableName: "entidade",
   timestamps: false,
  },
 );

 Entidade.associate = (models) => {
  // Herança — uma Entidade pode ser um destes três tipos
  Entidade.hasOne(models.Mecena, {
   foreignKey: "nif_nipc",
   as: "mecena",
  });
  Entidade.hasOne(models.Negocio, {
   foreignKey: "nif_nipc",
   as: "negocio",
  });
  Entidade.hasOne(models.Instituicao, {
   foreignKey: "nif_nipc",
   as: "instituicao",
  });

  // Contactos
  Entidade.hasMany(models.Contacto, {
   foreignKey: "entidade_nif_nipc",
   as: "contactos",
  });

  // Localidade — many-to-many via tabela de ligação
  Entidade.belongsToMany(models.Localidade, {
   through: models.Localidade_Entidade,
   foreignKey: "entidade_nif_nipc",
   otherKey: "localidade_codigo_postal",
   as: "localidades",
  });
 };

 return Entidade;
};
