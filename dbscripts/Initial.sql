SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema week5
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS week5 ;

-- -----------------------------------------------------
-- Schema week5
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS week5 DEFAULT CHARACTER SET utf8 ;
USE week5 ;

-- -----------------------------------------------------
-- Table week5.CountriesCodes
-- -----------------------------------------------------
DROP TABLE IF EXISTS week5.CountriesCodes ;

CREATE TABLE IF NOT EXISTS week5.CountriesCodes (
  Id VARCHAR(5) NOT NULL,
  PRIMARY KEY (Id),
  UNIQUE INDEX Id_UNIQUE (Id ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table week5.CountriesNames
-- -----------------------------------------------------
DROP TABLE IF EXISTS week5.CountriesNames ;

CREATE TABLE IF NOT EXISTS week5.CountriesNames (
  Id INT NOT NULL AUTO_INCREMENT,
  Name VARCHAR(30) NOT NULL,
  CountryCodeId VARCHAR(45) NULL,
  PRIMARY KEY (Id),
  UNIQUE INDEX Name_UNIQUE (Name ASC) VISIBLE,
  INDEX CountryCodeId_idx (CountryCodeId ASC) VISIBLE,
  CONSTRAINT CountryCodeId
    FOREIGN KEY (CountryCodeId)
    REFERENCES week5.CountriesCodes (Id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table week5.Covid
-- -----------------------------------------------------
DROP TABLE IF EXISTS week5.Covid ;

CREATE TABLE IF NOT EXISTS week5.Covid (
  Id INT NOT NULL AUTO_INCREMENT,
  CountryCodeId VARCHAR(5) NULL,
  Confirmed DOUBLE NULL,
  Deaths DOUBLE NULL,
  CreationDate DATE NULL,
  PRIMARY KEY (Id),
  UNIQUE INDEX Id_UNIQUE (Id ASC) VISIBLE,
  INDEX CountryCodeId_idx (CountryCodeId ASC) VISIBLE,
  CONSTRAINT CountryCodeId
    FOREIGN KEY (CountryCodeId)
    REFERENCES week5.CountriesCodes (Id)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;