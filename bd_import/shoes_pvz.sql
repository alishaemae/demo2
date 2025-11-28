-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: shoes
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `pvz`
--

DROP TABLE IF EXISTS `pvz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pvz` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `index` bigint NOT NULL,
  `city` varchar(255) NOT NULL,
  `street` varchar(255) NOT NULL,
  `number` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pvz`
--

LOCK TABLES `pvz` WRITE;
/*!40000 ALTER TABLE `pvz` DISABLE KEYS */;
INSERT INTO `pvz` VALUES (1,420151,'Лесной','Вишневая',32),(2,125061,'Лесной','Подгорная',8),(3,630370,'Лесной','Шоссейная',24),(4,400562,'Лесной','Зеленая',32),(5,614510,'Лесной','Маяковского',47),(6,410542,'Лесной','Светлая',46),(7,620839,'Лесной','Цветочная',8),(8,443890,'Лесной','Коммунистическая',1),(9,603379,'Лесной','Спортивная',46),(10,603721,'Лесной','Гоголя',41),(11,410172,'Лесной','Северная',13),(12,614611,'Лесной','Молодежная',50),(13,454311,'Лесной','Новая',19),(14,660007,'Лесной','Октябрьская',19),(15,603036,'Лесной','Садовая',4),(16,394060,'Лесной','Фрунзе',43),(17,410661,'Лесной','Школьная',50),(18,625590,'Лесной','Коммунистическая',20),(19,625683,'Лесной','8 Марта',1),(20,450983,'Лесной','Комсомольская',26),(21,394782,'Лесной','Чехова',3),(22,603002,'Лесной','Дзержинского',28),(23,450558,'Лесной','Набережная',30),(24,344288,'Лесной','Чехова',1),(25,614164,'Лесной','Степная',30),(26,394242,'Лесной','Коммунистическая',43),(27,660540,'Лесной','Солнечная',25),(28,125837,'Лесной','Шоссейная',40),(29,125703,'Лесной','Партизанская',49),(30,625283,'Лесной','Победы',46),(31,614753,'Лесной','Полевая',35),(32,426030,'Лесной','Маяковского',44),(33,450375,'Лесной','Клубная',44),(34,625560,'Лесной','Некрасова',12),(35,630201,'Лесной','Комсомольская',17),(36,190949,'Лесной','Мичурина',26);
/*!40000 ALTER TABLE `pvz` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-08  8:33:57
