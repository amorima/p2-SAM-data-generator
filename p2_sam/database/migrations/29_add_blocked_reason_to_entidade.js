"use strict";

async function columnExists(queryInterface, table, column) {
  const [[{ cnt }]] = await queryInterface.sequelize.query(`
    SELECT COUNT(*) as cnt
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = :table
      AND COLUMN_NAME = :column
  `, { replacements: { table, column } });
  return cnt > 0;
}

module.exports = {
  async up(queryInterface, Sequelize) {
    if (!await columnExists(queryInterface, "entidade", "blocked")) {
      await queryInterface.addColumn("entidade", "blocked", {
        type: Sequelize.TINYINT,
        allowNull: false,
        defaultValue: 0,
        after: "role",
      });
    }

    if (!await columnExists(queryInterface, "entidade", "reason")) {
      await queryInterface.addColumn("entidade", "reason", {
        type: Sequelize.STRING(255),
        allowNull: true,
        defaultValue: null,
        after: "blocked",
      });
    }
  },

  async down(queryInterface) {
    await queryInterface.removeColumn("entidade", "reason");
    await queryInterface.removeColumn("entidade", "blocked");
  },
};
