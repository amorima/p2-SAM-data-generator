const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const Contacto = sequelize.define(
  "Contacto",
  {
   contacto: {
    type: DataTypes.STRING(45),
    primarykey: true,
   },
   entidade_nif_nipc: {
    type: DataTypes.STRING(45),
    allowNull: false,
   },
   nome_contacto: {
    type: DataTypes.STRING(100),
    allowNull: false,
   },
   descricao: {
    type: DataTypes.STRING(500),
    allowNull: false,
   },
  },
  {
   tableName: "Contacto",
   timestamps: false,
  }
 );

 Contacto.associate = (models) => {
  // Cada doação pertence a um mecenas
  Contacto.belongsTo(models.Entidade, {
   foreignKey: "entidade_nif_nipc",
   as: "entidade",
  });
 };

 return Contacto;
};
