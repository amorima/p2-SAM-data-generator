const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const Entidade = sequelize.define("Entidade", {
  nif_nipc: {
   type: DataTypes.INTEGER(9),
   primarykey: true,
   allowNull: false,
  },
  email_login: {
   type: DataTypes.STRING(45),
   allowNull: false,
   unique: true,
  },
  password: {
   type: DataTypes.STRING(45),
   allowNull: false,
  },
  nome_entidade: {
   type: DataTypes.STRING(45),
   allowNull: false,
  },
  iban: {
   type: DataTypes.STRING(23),
   allowNull: false,
   unique: true,
  },
  rua: {
   type: DataTypes.STRING(200),
   allowNull: false,
  },
  n_porta: {
   type: DataTypes.STRING(45),
   allowNull: false,
  },
  codigo_postal: {
   type: DataTypes.STRING(10),
   allowNull: false,
  },
  tableName: "entidade",
  timestamps: false,
 });

 Entidade.associate = (models) => {
  // Cada ator tem apenas uma entidade
  Entidade.hasOne(models.Mecena, {
   foreignKey: "nif_nipc",
   as: "mecena",
  }),
   Entidade.hasOne(models.Negocio, {
    foreignKey: "nif_nipc",
    as: "negocio",
   }),
   Entidade.hasOne(models.Instituicao, {
    foreignKey: "nif_nipc",
    as: "instituicao",
   });
  Entidade.hasMany(models.Contactos, {
   foreignKey: "entidade_nif_nipc",
   as: "contacto",
  });
  // cada entidade tem uma localidade
  Entidade.hasOne(models.Localidade, {
   foreignKey: "codigo_postal",
   as: "localidade",
  });
 };

 return Entidade;
};
