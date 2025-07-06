-- phpMyAdmin SQL Dump
-- version 5.2.1
-- Tiempo de generación: 06-07-2025 a las 15:32:30
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

--
-- Volcado de datos para la tabla `datos`
--

INSERT INTO `datos` (`dat_id`, `var_id`, `fue_id`, `fecha`, `valor`) VALUES
(17, 1, 1, '2025-07-05 13:00:00', 36.20),
(18, 1, 1, '2025-07-05 13:00:00', 36.20),
(19, 2, 1, '2025-07-05 14:00:00', 37.00),
(20, 5, 1, '2025-07-05 14:00:00', 38.10),
(21, 5, 1, '2025-07-05 16:00:00', 36.90);

--
-- Volcado de datos para la tabla `evento`
--

INSERT INTO `evento` (`eve_id`, `var_id`, `fecha`, `descripcion`, `validado`) VALUES
(8, 1, '2025-07-05 13:00:00', 'Riesgo por temp. MAXIMAS: 36.2 ºC', 0),
(9, 1, '2025-07-05 13:00:00', 'Riesgo por temp. MAXIMAS: 36.2 ºC', 0),
(10, 2, '2025-07-05 14:00:00', 'Riesgo por temp. MAXIMAS: 37.0 ºC', 0),
(11, 5, '2025-07-05 14:00:00', 'Riesgo por temp. MAXIMAS: 38.1 ºC', 0),
(12, 5, '2025-07-05 16:00:00', 'Riesgo por temp. MAXIMAS: 36.9 ºC', 0);

--
-- Volcado de datos para la tabla `fuente`
--

INSERT INTO `fuente` (`fue_id`, `nombre`, `descripcion`, `url_api`, `api_key`, `tiempo_real`, `intervalo`, `activo`) VALUES
(1, 'AEMET OpenData', 'API de la AEMET con datos públicos', 'https://opendata.aemet.es/opendata/', '', 0, NULL, 1),
(2, 'SAIH del Júcar', 'Servicio Automático de Información Hidrológica del', 'https://saih.chj.es/chj/saih/glayer?t=a', '', 0, NULL, 1);

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`usu_id`, `nombre`, `apellidos`, `usuario`, `password`, `email`, `telefono`, `not_via_email`, `not_via_sms`, `fecha_alta`, `activo`, `admin`) VALUES
(1, 'Alberto', 'López Navarro', 'aaln16', '202cb962ac59075b964b07152d234b70', 'alberto@example.com', '600123123', 1, 0, '2025-06-11 21:45:26', 1, 1),
(2, 'Beatriz', 'Bea Romero', 'bbea22', 'e74295df48ec1d594b7236a1f5f4c9f2', 'beatriz@example.com', '600111222', 1, 1, '2025-06-11 21:45:26', 1, 0),
(3, 'Carlos', 'Cano Ruiz', 'carlos9', 'be1bc8b99c6b90b7b5085b1d6e38fcfd', 'carlos@example.com', '600333444', 0, 1, '2025-06-11 21:45:26', 1, 0),
(4, 'Diana', 'Ramírez Tovar', 'dianar3', '7b9f82ef53c70c5b35a418af3e17733b', 'diana@example.com', '600555666', 1, 0, '2025-06-11 21:45:26', 1, 0),
(5, 'Elena', 'Navas Gil', 'eln555', '0e7e3e478efb17f683389ffb71c4ed1d', 'elena@example.com', '600777888', 0, 0, '2025-06-11 21:45:26', 1, 0);

--
-- Volcado de datos para la tabla `variable`
--

INSERT INTO `variable` (`var_id`, `zon_id`, `codigo`, `nombre`, `unidad`, `descripcion`, `limite_max`, `limite_min`, `fecha_creacion`, `activo`) VALUES
(1, 1, 'tamax', 'Temperatura máxima', 'ºC', 'Temp. máxima en La Mancha AB', 36.00, NULL, '2025-06-14 10:00:12', 1),
(2, 2, 'tamax', 'Temperatura máxima', 'ºC', 'Temp. máxima en Alcaráz y Segura', 36.00, NULL, '2025-06-14 10:00:12', 1),
(3, 3, 'tamax', 'Temperatura máxima', 'ºC', 'Temp. máxima en Hellin y Almansa', 36.00, NULL, '2025-06-14 10:00:12', 1),
(4, 4, 'tamax', 'Temperatura máxima', 'ºC', 'Temp. máxima en Montes del Norte y Anchuras', 38.00, NULL, '2025-06-14 10:00:12', 1),
(5, 5, 'tamax', 'Temperatura máxima', 'ºC', 'Temp. máxima en La Mancha CR', 36.00, NULL, '2025-06-14 10:00:12', 1),
(6, 6, 'tamax', 'Temperatura máxima', 'ºC', 'Temp. máxima en Valle del Guadiana', 38.00, NULL, '2025-06-14 10:00:12', 1),
(7, 7, 'tamax', 'Temperatura máxima', 'ºC', 'Temp. máxima en Sierras de Alcudia y Madrona', 38.00, NULL, '2025-06-14 10:00:12', 1),
(8, 8, 'tamax', 'Temperatura máxima', 'ºC', 'Temp. máxima en Alcarria Conquense', 36.00, NULL, '2025-06-14 10:00:12', 1),
(9, 9, 'tamax', 'Temperatura máxima', 'ºC', 'Temp. máxima en Serrania de Cuenca', 34.00, NULL, '2025-06-14 10:00:12', 1),
(10, 10, 'tamax', 'Temperatura máxima', 'ºC', 'Temp. máxima en La Mancha conquense', 36.00, NULL, '2025-06-14 10:00:12', 1),
(11, 11, 'tamax', 'Temperatura máxima', 'ºC', 'Temp. máxima en Serrania de GU', 34.00, NULL, '2025-06-14 10:00:12', 1),
(12, 12, 'tamax', 'Temperatura máxima', 'ºC', 'Temp. máxima en Parameras de Molina', 34.00, NULL, '2025-06-14 10:00:12', 1),
(13, 13, 'tamax', 'Temperatura máxima', 'ºC', 'Temp. máxima en Alcarria de Guadalajara', 36.00, NULL, '2025-06-14 10:00:12', 1),
(14, 14, 'tamax', 'Temperatura máxima', 'ºC', 'Temp. máxima en Sierra de San Vicente', 36.00, NULL, '2025-06-14 10:00:12', 1),
(15, 15, 'tamax', 'Temperatura máxima', 'ºC', 'Temp. máxima en Valle del Tajo', 38.00, NULL, '2025-06-14 10:00:12', 1),
(16, 16, 'tamax', 'Temperatura máxima', 'ºC', 'Temp. máxima en Montes de Toledo', 36.00, NULL, '2025-06-14 10:00:12', 1),
(17, 17, 'tamax', 'Temperatura máxima', 'ºC', 'Temp. máxima en La Mancha toledana', 38.00, NULL, '2025-06-14 10:00:12', 1);

--
-- Volcado de datos para la tabla `zona`
--

INSERT INTO `zona` (`zon_id`, `codigo`, `nombre`, `provincia`, `descripcion`, `mapa`) VALUES
(1, '680201', 'La Mancha albaceteña', 'Albacete', 'Zona de avisos meteorológicos', NULL),
(2, '680202', 'Alcaraz y Segura', 'Albacete', 'Zona de avisos meteorológicos', NULL),
(3, '680203', 'Hellín y Almansa', 'Albacete', 'Zona de avisos meteorológicos', NULL),
(4, '681301', 'Montes del norte y Anchur', 'Ciudad Real', 'Zona de avisos meteorológicos', NULL),
(5, '681302', 'La Mancha de Ciudad Real', 'Ciudad Real', 'Zona de avisos meteorológicos', NULL),
(6, '681303', 'Valle del Guadiana', 'Ciudad Real', 'Zona de avisos meteorológicos', NULL),
(7, '681304', 'Sierras de Alcudia y Madr', 'Ciudad Real', 'Zona de avisos meteorológicos', NULL),
(8, '681601', 'Alcarria conquense', 'Cuenca', 'Zona de avisos meteorológicos', NULL),
(9, '681602', 'Serranía de Cuenca', 'Cuenca', 'Zona de avisos meteorológicos', NULL),
(10, '681603', 'La Mancha conquense', 'Cuenca', 'Zona de avisos meteorológicos', NULL),
(11, '681901', 'Serranía de Guadalajara', 'Guadalajara', 'Zona de avisos meteorológicos', NULL),
(12, '681902', 'Parameras de Molina', 'Guadalajara', 'Zona de avisos meteorológicos', NULL),
(13, '681903', 'Alcarria de Guadalajara', 'Guadalajara', 'Zona de avisos meteorológicos', NULL),
(14, '684501', 'Sierra de San Vicente', 'Toledo', 'Zona de avisos meteorológicos', NULL),
(15, '684502', 'Valle del Tajo', 'Toledo', 'Zona de avisos meteorológicos', NULL),
(16, '684503', 'Montes de Toledo', 'Toledo', 'Zona de avisos meteorológicos', NULL),
(17, '684504', 'La Mancha toledana', 'Toledo', 'Zona de avisos meteorológicos', NULL);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
