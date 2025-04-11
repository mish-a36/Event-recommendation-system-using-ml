<?php
header("Content-Type: application/json");

$host = "localhost";
$db = "event_recommendation_system";
$user = "root";
$pass = "";

// Create connection
$conn = new mysqli($host, $user, $pass, $db);

// Check connection
if ($conn->connect_error) {
    echo json_encode(["error" => "Connection failed: " . $conn->connect_error]);
    exit();
}

// Get event_id from query params
if (!isset($_GET["event_id"])) {
    echo json_encode(["error" => "Missing event_id"]);
    exit();
}

$event_id = intval($_GET["event_id"]);

$sql = "SELECT `date` FROM `events` WHERE `id` = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $event_id);
$stmt->execute();
$result = $stmt->get_result();

if ($row = $result->fetch_assoc()) {
    echo json_encode(["event_id" => $event_id, "date" => $row["date"]]);
} else {
    echo json_encode(["error" => "Event not found"]);
}

$stmt->close();
$conn->close();
?>
