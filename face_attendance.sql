/*
 Navicat Premium Data Transfer

 Source Server         : Local MySql
 Source Server Type    : MySQL
 Source Server Version : 100422
 Source Host           : localhost:3306
 Source Schema         : face_attendance

 Target Server Type    : MySQL
 Target Server Version : 100422
 File Encoding         : 65001

 Date: 23/05/2022 15:56:54
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for attendance
-- ----------------------------
DROP TABLE IF EXISTS `attendance`;
CREATE TABLE `attendance`  (
  `attendance_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NULL DEFAULT NULL,
  `time_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`attendance_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of attendance
-- ----------------------------
INSERT INTO `attendance` VALUES (1, 1, NULL);
INSERT INTO `attendance` VALUES (2, 1, NULL);
INSERT INTO `attendance` VALUES (3, 1, NULL);
INSERT INTO `attendance` VALUES (4, 1, NULL);

-- ----------------------------
-- Table structure for students
-- ----------------------------
DROP TABLE IF EXISTS `students`;
CREATE TABLE `students`  (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `image_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of students
-- ----------------------------
INSERT INTO `students` VALUES (1, 'Shahed', 'Shahed.jpg');
INSERT INTO `students` VALUES (2, 'Shekhar', 'Shekhar.jpg');
INSERT INTO `students` VALUES (3, 'Shekhar Abdullah', NULL);
INSERT INTO `students` VALUES (4, 'Shekhar Abdullah', 'krish.JPG');
INSERT INTO `students` VALUES (5, 'Shekhar Abdullah', 'krish.JPG');

SET FOREIGN_KEY_CHECKS = 1;
