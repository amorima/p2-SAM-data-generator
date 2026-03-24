const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const t = sequelize.define(
  "t",
  {
   codigo_postal: {
    type: DataTypes.STRING(45),
    primarykey: true,
   },
  },
  {
   tableName: "",
   timestamps: false,
  }
 );

 t.associate = (models) => {
  // Cada doação pertence a um mecenas
  t.belongsTo(models.tb, {
   foreignKey: "",
   as: "",
  });
 };

 return t;
};
