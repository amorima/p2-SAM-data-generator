const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const Contacto = sequelize.define(
  "contacto",
  {
   contacto: {
    type: DataTypes.STRING(45),
    primaryKey: true,
   },
   entidade_nif_nipc: {
    type: DataTypes.STRING(9),
    allowNull: false,
   },
   nome_contacto: {
    type: DataTypes.STRING(100),
    allowNull: false,
   },
   descricao: {
    type: DataTypes.STRING(255),
    allowNull: false,
   },
  },
  {
   tableName: "contacto",
   timestamps: false,
  },
 );

 Contacto.associate = (models) => {
  // Contacto pertence a entidade
  Contacto.belongsTo(models.Entidade, {
   foreignKey: "entidade_nif_nipc",
   as: "entidade",
  });
 };

 return Contacto;
};
