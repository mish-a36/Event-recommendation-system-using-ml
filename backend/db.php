<?php
$host = "localhost";
$dbname = "event_recommendation_system";
$username = "root";  // Change if needed
$password = "";      // Change if needed

$conn = new mysqli($host, $username, $password, $dbname);
if ($conn->connect_error) {
    die(json_encode(["error" => "Database connection failed: " . $conn->connect_error]));
}
?>
