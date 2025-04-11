<?php
include 'db.php';

header('Content-Type: application/json');

$query = $conn->query("SELECT id, institution_name FROM institutions");
$institutions = [];

while ($row = $query->fetch_assoc()) {
    $institutions[] = $row;
}

echo json_encode(["institutions" => $institutions]);

$conn->close();
?>
