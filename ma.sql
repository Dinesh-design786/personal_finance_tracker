SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `tbluser` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `FullName` varchar(150) DEFAULT NULL,
  `Email` varchar(200) DEFAULT NULL,
  `MobileNumber` bigint(10) DEFAULT NULL,
  `Password` varchar(200) DEFAULT NULL,
  `RegDate` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `tblexpense` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `UserId` int(10) NOT NULL,
  `ExpenseDate` date DEFAULT NULL,
  `ExpenseItem` varchar(200) DEFAULT NULL,
  `ExpenseCost` DECIMAL(10,2) NOT NULL,
  `NoteDate` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`ID`),
  FOREIGN KEY (`UserId`) REFERENCES `tbluser`(`ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `tbluser` (`ID`, `FullName`, `Email`, `MobileNumber`, `Password`, `RegDate`) VALUES
(1, 'Rajeshwari', 'raj@gmail.com', 5655555655, '202cb962ac59075b964b07152d234b70', '2019-05-15 08:52:27'),
(2, 'Meenakhi', 'meena@gmail.com', 8989898897, '81dc9bdb52d04dc20036dbd8313ed055', '2019-05-15 08:52:27'),
(3, 'Khusbu', 'khusi@gmail.com', 5645798897, '202cb962ac59075b964b07152d234b70', '2019-05-15 08:52:27');

INSERT INTO `tblexpense` (`ID`, `UserId`, `ExpenseDate`, `ExpenseItem`, `ExpenseCost`, `NoteDate`) VALUES
(1, 2, '2019-05-15', 'Milk', 63.00, NULL),
(2, 2, '2019-05-15', 'Vegetables', 520.00, '2019-05-15 10:06:19');

COMMIT;
