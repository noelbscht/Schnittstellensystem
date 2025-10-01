CREATE TABLE `authentication` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(8) NOT NULL,
  `auth_key` varchar(36) NOT NULL DEFAULT (UUID()),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;