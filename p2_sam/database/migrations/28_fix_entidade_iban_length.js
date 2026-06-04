"use strict";

// IBANs can be up to 34 characters (Portuguese IBANs are 25, e.g. PT50 + 21).
// The column was VARCHAR(23), so any real IBAN overflowed under STRICT_TRANS_TABLES
// and aborted entity creation (business/institution/patron) with ER_DATA_TOO_LONG.
module.exports = {
 async up(queryInterface) {
  await queryInterface.sequelize.query(
   "ALTER TABLE `entidade` MODIFY COLUMN `iban` VARCHAR(34) NULL"
  );
 },

 async down(queryInterface) {
  await queryInterface.sequelize.query(
   "ALTER TABLE `entidade` MODIFY COLUMN `iban` VARCHAR(23) NULL"
  );
 },
};
