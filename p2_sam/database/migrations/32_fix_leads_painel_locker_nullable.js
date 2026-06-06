"use strict";

// The db.config.js ALTER TABLE for id_painel/id_locker fails at runtime because
// MySQL refuses MODIFY COLUMN when a FK references the column in some configurations.
// This migration drops the FKs, makes the columns nullable, then restores the FKs.
module.exports = {
  async up(queryInterface) {
    const sq = queryInterface.sequelize;

    for (const col of ["id_painel", "id_locker"]) {
      // Find FK(s) on this column
      const [fks] = await sq.query(`
        SELECT CONSTRAINT_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = 'leads'
          AND COLUMN_NAME = :col
          AND REFERENCED_TABLE_NAME IS NOT NULL
      `, { replacements: { col } });

      for (const { CONSTRAINT_NAME } of fks) {
        await sq.query(`ALTER TABLE \`leads\` DROP FOREIGN KEY \`${CONSTRAINT_NAME}\``);
      }

      await sq.query(`ALTER TABLE \`leads\` MODIFY \`${col}\` INT NULL`);

      // Restore FKs
      for (const { CONSTRAINT_NAME } of fks) {
        const refTable = col === "id_painel" ? "painel" : "locker_inteligente";
        const refCol   = col === "id_painel" ? "id_dispositivo" : "id_locker";
        try {
          await sq.query(`
            ALTER TABLE \`leads\`
            ADD CONSTRAINT \`${CONSTRAINT_NAME}\`
            FOREIGN KEY (\`${col}\`) REFERENCES \`${refTable}\` (\`${refCol}\`)
            ON DELETE CASCADE ON UPDATE CASCADE
          `);
        } catch (e) {
          console.warn(`[migration 32] Could not restore FK ${CONSTRAINT_NAME}: ${e.message}`);
        }
      }
    }
  },

  async down(queryInterface) {
    const sq = queryInterface.sequelize;
    await sq.query("ALTER TABLE `leads` MODIFY `id_painel` INT NOT NULL");
    await sq.query("ALTER TABLE `leads` MODIFY `id_locker` INT NOT NULL");
  },
};
