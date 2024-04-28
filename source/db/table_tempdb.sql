CREATE TABLE `tempdb`(
    `no` int(11) NOT NULL,
    `user_id` varchar(255) NOT NULL,
    `user_name` varchar(255) NOT NULL,
    `image_path` varchar(255) NOT NULL,
    `code_farm` varchar(255) NOT NULL,
    `latitude` varchar(255) NOT NULL,
    `longitude` varchar(255) NOT NULL,
    `disease_percent` varchar(10) NOT NULL,
    `symptom` varchar(255) NOT NULL,
    `status` varchar(255) NOT NULL DEFAULT 'Not Submitted'

)

ALTER TABLE `tempdb`
  ADD PRIMARY KEY (`no`);

ALTER TABLE `tempdb`
  MODIFY `no` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;