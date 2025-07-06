-- phpMyAdmin SQL Dump
-- version 5.2.1
-- Versión del servidor: 9.1.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `meteo_db`
--
CREATE DATABASE IF NOT EXISTS `meteo_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `meteo_db`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `datos`
--

DROP TABLE IF EXISTS `datos`;
CREATE TABLE IF NOT EXISTS `datos` (
  `dat_id` int NOT NULL AUTO_INCREMENT,
  `var_id` int NOT NULL,
  `fue_id` int NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `valor` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`dat_id`),
  KEY `var_id` (`var_id`),
  KEY `fue_id` (`fue_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `evento`
--

DROP TABLE IF EXISTS `evento`;
CREATE TABLE IF NOT EXISTS `evento` (
  `eve_id` int NOT NULL AUTO_INCREMENT,
  `var_id` int NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `descripcion` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `validado` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`eve_id`),
  KEY `var_id` (`var_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `fuente`
--

DROP TABLE IF EXISTS `fuente`;
CREATE TABLE IF NOT EXISTS `fuente` (
  `fue_id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(25) COLLATE utf8mb4_general_ci NOT NULL,
  `descripcion` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `url_api` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `api_key` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tiempo_real` tinyint(1) NOT NULL DEFAULT '0',
  `intervalo` int DEFAULT NULL,
  `activo` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`fue_id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notificacion`
--

DROP TABLE IF EXISTS `notificacion`;
CREATE TABLE IF NOT EXISTS `notificacion` (
  `not_id` int NOT NULL AUTO_INCREMENT,
  `eve_id` int NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `entrega` tinyint(1) DEFAULT NULL,
  `lectura` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`not_id`),
  KEY `eve_id` (`eve_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recomendacion`
--

DROP TABLE IF EXISTS `recomendacion`;
CREATE TABLE IF NOT EXISTS `recomendacion` (
  `rec_id` int NOT NULL AUTO_INCREMENT,
  `var_id` int DEFAULT NULL,
  `texto` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `enlace` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`rec_id`),
  KEY `var_id` (`var_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `regla`
--

DROP TABLE IF EXISTS `regla`;
CREATE TABLE IF NOT EXISTS `regla` (
  `reg_id` int NOT NULL AUTO_INCREMENT,
  `var_id` int NOT NULL,
  `descripcion` varchar(50) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Descripciónd o definición de la regla',
  `fecha` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `regla` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `automatica` tinyint(1) NOT NULL DEFAULT '0',
  `activo` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`reg_id`),
  KEY `var_id` (`var_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `suscripcion`
--

DROP TABLE IF EXISTS `suscripcion`;
CREATE TABLE IF NOT EXISTS `suscripcion` (
  `sus_id` int NOT NULL AUTO_INCREMENT,
  `var_id` int NOT NULL,
  `usu_id` int NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `activo` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`sus_id`),
  UNIQUE KEY `var_id` (`var_id`,`usu_id`),
  KEY `usu_id` (`usu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

DROP TABLE IF EXISTS `usuario`;
CREATE TABLE IF NOT EXISTS `usuario` (
  `usu_id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `apellidos` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `usuario` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(32) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'md5 de la contraseña de los usuarios',
  `email` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `telefono` varchar(15) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `not_via_email` tinyint(1) NOT NULL DEFAULT '0',
  `not_via_sms` tinyint(1) NOT NULL DEFAULT '0',
  `fecha_alta` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `activo` tinyint(1) NOT NULL DEFAULT '0',
  `admin` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'admin = 1, usuario es administrador del sistema',
  PRIMARY KEY (`usu_id`),
  UNIQUE KEY `usuario` (`usuario`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `variable`
--

DROP TABLE IF EXISTS `variable`;
CREATE TABLE IF NOT EXISTS `variable` (
  `var_id` int NOT NULL AUTO_INCREMENT,
  `zon_id` int DEFAULT NULL,
  `codigo` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nombre` varchar(25) COLLATE utf8mb4_general_ci NOT NULL,
  `unidad` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `descripcion` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `limite_max` decimal(10,2) DEFAULT NULL,
  `limite_min` decimal(10,2) DEFAULT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `activo` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`var_id`),
  KEY `zon_id` (`zon_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `zona`
--

DROP TABLE IF EXISTS `zona`;
CREATE TABLE IF NOT EXISTS `zona` (
  `zon_id` int NOT NULL AUTO_INCREMENT,
  `codigo` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `nombre` varchar(25) COLLATE utf8mb4_general_ci NOT NULL,
  `provincia` varchar(25) COLLATE utf8mb4_general_ci NOT NULL,
  `descripcion` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `mapa` blob COMMENT 'Campo para los bytes de la imagen del mapa de la zona de interés',
  PRIMARY KEY (`zon_id`),
  UNIQUE KEY `codigo` (`codigo`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `datos`
--
ALTER TABLE `datos`
  ADD CONSTRAINT `datos_ibfk_1` FOREIGN KEY (`var_id`) REFERENCES `variable` (`var_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `datos_ibfk_2` FOREIGN KEY (`fue_id`) REFERENCES `fuente` (`fue_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `evento`
--
ALTER TABLE `evento`
  ADD CONSTRAINT `evento_ibfk_1` FOREIGN KEY (`var_id`) REFERENCES `variable` (`var_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `notificacion`
--
ALTER TABLE `notificacion`
  ADD CONSTRAINT `notificacion_ibfk_1` FOREIGN KEY (`eve_id`) REFERENCES `evento` (`eve_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `recomendacion`
--
ALTER TABLE `recomendacion`
  ADD CONSTRAINT `recomendacion_ibfk_1` FOREIGN KEY (`var_id`) REFERENCES `variable` (`var_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Filtros para la tabla `regla`
--
ALTER TABLE `regla`
  ADD CONSTRAINT `regla_ibfk_1` FOREIGN KEY (`var_id`) REFERENCES `variable` (`var_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `suscripcion`
--
ALTER TABLE `suscripcion`
  ADD CONSTRAINT `suscripcion_ibfk_1` FOREIGN KEY (`var_id`) REFERENCES `variable` (`var_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `suscripcion_ibfk_2` FOREIGN KEY (`usu_id`) REFERENCES `usuario` (`usu_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `variable`
--
ALTER TABLE `variable`
  ADD CONSTRAINT `variable_ibfk_1` FOREIGN KEY (`zon_id`) REFERENCES `zona` (`zon_id`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
