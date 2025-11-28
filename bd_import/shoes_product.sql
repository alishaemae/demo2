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
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `article` varchar(255) NOT NULL,
  `id_type` int unsigned NOT NULL,
  `unit` varchar(50) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `id_supplier` int unsigned NOT NULL,
  `id_producer` int unsigned NOT NULL,
  `id_category` int unsigned NOT NULL,
  `discount` int NOT NULL,
  `amount` int NOT NULL,
  `description` varchar(255) NOT NULL,
  `photo` blob NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_type` (`id_type`),
  KEY `id_supplier` (`id_supplier`),
  KEY `id_producer` (`id_producer`),
  KEY `id_category` (`id_category`),
  CONSTRAINT `product_ibfk_1` FOREIGN KEY (`id_type`) REFERENCES `product_type` (`id`),
  CONSTRAINT `product_ibfk_2` FOREIGN KEY (`id_supplier`) REFERENCES `supplier` (`id`),
  CONSTRAINT `product_ibfk_3` FOREIGN KEY (`id_producer`) REFERENCES `producer` (`id`),
  CONSTRAINT `product_ibfk_4` FOREIGN KEY (`id_category`) REFERENCES `category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,'А112Т4',1,'шт.',4990.00,1,1,1,3,6,'Женские Ботинки демисезонные kari',_binary '1.jpg'),(2,'F635R4',1,'шт.',3244.00,2,2,1,2,13,'Ботинки Marco Tozzi женские демисезонные, размер 39, цвет бежевый',_binary '2.jpg'),(3,'H782T5',2,'шт.',4499.00,1,1,2,4,5,'Туфли kari мужские классика MYZ21AW-450A, размер 43, цвет: черный',_binary '3.jpg'),(4,'G783F5',1,'шт.',5900.00,1,3,2,2,8,'Мужские ботинки Рос-Обувь кожаные с натуральным мехом',_binary '4.jpg'),(5,'J384T6',1,'шт.',3800.00,2,4,2,2,16,'B3430/14 Полуботинки мужские Rieker',_binary '5.jpg'),(6,'D572U8',4,'шт.',4100.00,2,3,2,3,6,'129615-4 Кроссовки мужские',_binary '6.jpg'),(7,'F572H7',2,'шт.',2700.00,1,2,1,2,14,'Туфли Marco Tozzi женские летние, размер 39, цвет черный',_binary '7.jpg'),(8,'D329H3',3,'шт.',1890.00,2,5,1,4,4,'Полуботинки Alessio Nesca женские 3-30797-47, размер 37, цвет: бордовый',_binary '8.jpg'),(9,'B320R5',2,'шт.',4300.00,1,4,1,2,6,'Туфли Rieker женские демисезонные, размер 41, цвет коричневый',_binary '9.jpg'),(10,'G432E4',2,'шт.',2800.00,1,1,1,3,15,'Туфли kari женские TR-YR-413017, размер 37, цвет: черный',_binary '10.jpg'),(11,'S213E3',3,'шт.',2156.00,2,6,2,3,6,'407700/01-01 Полуботинки мужские CROSBY',''),(12,'E482R4',3,'шт.',1800.00,1,1,1,2,14,'Полуботинки kari женские MYZ20S-149, размер 41, цвет: черный',''),(13,'S634B5',5,'шт.',5500.00,2,6,2,3,0,'Кеды Caprice мужские демисезонные, размер 42, цвет черный',''),(14,'K345R4',3,'шт.',2100.00,2,6,2,2,3,'407700/01-02 Полуботинки мужские CROSBY',''),(15,'O754F4',2,'шт.',5400.00,2,4,1,4,18,'Туфли женские демисезонные Rieker артикул 55073-68/37',''),(16,'G531F4',1,'шт.',6600.00,1,1,1,12,9,'Ботинки женские зимние ROMER арт. 893167-01 Черный',''),(17,'J542F5',6,'шт.',500.00,1,1,2,13,0,'Тапочки мужские Арт.70701-55-67син р.41',''),(18,'B431R5',1,'шт.',2700.00,2,4,2,2,5,'Мужские кожаные ботинки/мужские ботинки',''),(19,'P764G4',2,'шт.',6800.00,1,6,1,15,15,'Туфли женские, ARGO, размер 38',''),(20,'C436G5',1,'шт.',10200.00,1,5,1,15,9,'Ботинки женские, ARGO, размер 40',''),(21,'F427R5',1,'шт.',11800.00,2,4,1,15,11,'Ботинки на молнии с декоративной пряжкой FRAU',''),(22,'N457T5',3,'шт.',4600.00,1,6,1,3,13,'Полуботинки Ботинки черные зимние, мех',''),(23,'D364R4',2,'шт.',12400.00,1,1,1,16,5,'Туфли Luiza Belly женские Kate-lazo черные из натуральной замши',''),(24,'S326R5',6,'шт.',9900.00,2,6,2,17,15,'Мужские кожаные тапочки \"Профиль С.Дали\"',''),(25,'L754R4',3,'шт.',1700.00,1,1,1,2,7,'Полуботинки kari женские WB2020SS-26, размер 38, цвет: черный',''),(26,'M542T5',4,'шт.',2800.00,2,4,2,18,3,'Кроссовки мужские TOFA',''),(27,'D268G5',2,'шт.',4399.00,2,4,1,3,12,'Туфли Rieker женские демисезонные, размер 36, цвет коричневый',''),(28,'T324F5',7,'шт.',4699.00,1,6,1,2,5,'Сапоги замша Цвет: синий',''),(29,'K358H6',6,'шт.',599.00,1,4,2,20,2,'Тапочки мужские син р.41',''),(30,'H535R5',1,'шт.',2300.00,2,4,1,2,7,'Женские Ботинки демисезонные','');
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
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
