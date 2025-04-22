-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         11.7.2-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.10.0.7000
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para usuarios
CREATE DATABASE IF NOT EXISTS `usuarios` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci */;
USE `usuarios`;

-- Volcando estructura para tabla usuarios.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id_usuario` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `rol` varchar(50) DEFAULT NULL,
  `fecha_registro` timestamp NOT NULL,
  `nombre_usuario` varchar(50) NOT NULL,
  `nombres` varchar(50) NOT NULL,
  `apellidos` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  PRIMARY KEY (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Volcando datos para la tabla usuarios.usuarios: ~3 rows (aproximadamente)
INSERT INTO `usuarios` (`id_usuario`, `rol`, `fecha_registro`, `nombre_usuario`, `nombres`, `apellidos`, `email`, `contraseña`) VALUES
	(10, 'usuario', '2025-04-21 21:50:19', 'penebola', 'angel eduardo', 'cegarra taborda', 'angeleduardocegarrataborda@gmail.com', '$2b$12$igGlnOhl2B5/YKrk1d.EkeQArfXluvAaDR7ZRZUxQc4JBQyp9feVO'),
	(11, 'usuario', '2025-04-21 23:28:54', 'nini', 'ninibeth gisselle', 'orejarena sandoval', 'ninibeth@gmail.com', '$2b$12$Ki0nD0Oo6RkOWOBdx3rmGeDJb73KBl00eBVJqYwbaT/5d3X0H53se'),
	(12, 'usuario', '2025-04-22 15:40:46', 'leonardo', 'leonardo andre', 'torres moreno', 'leonardo@gmail.com', '$2b$12$rNa8/Uuc9Bm9prHv7Yt3Z.vZi8ZvHZtc/YyuViLwrUgdqjJoqcF5m');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
