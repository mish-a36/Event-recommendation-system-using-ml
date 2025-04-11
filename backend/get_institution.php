<?php
session_start();
include 'db.php';

header('Content-Type: application/json');

$query = $conn->query("SELECT COUNT(*) AS total FROM institutions");
$row = $query->fetch_assoc();

if ($row && $row['total'] > 0) {
    echo json_encode(["exists" => true]);
} else {
    echo json_encode(["exists" => false]);
}

$conn->close();
?>
