<?php
header('Content-Type: application/json');
include '../db.php';

$result = $conn->query("SELECT * FROM events");
$events = [];

while ($row = $result->fetch_assoc()) {
    $events[] = $row;
}

echo json_encode(empty($events) ? ["error" => "No events found"] : $events);
?>
