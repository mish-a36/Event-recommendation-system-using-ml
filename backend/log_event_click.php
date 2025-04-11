<?php
include 'db.php';  // Database connection

header('Content-Type: application/json');

// Check if request is POST
if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    echo json_encode(["status" => "error", "message" => "Invalid request method!"]);
    exit();
}

// Get request data
$rawData = file_get_contents("php://input");
$data = json_decode($rawData, true);

if (!$data || !isset($data["event_id"], $data["user_id"])) {
    echo json_encode(["status" => "error", "message" => "Missing required fields!"]);
    exit();
}

$event_id = intval($data["event_id"]);
$user_id = intval($data["user_id"]);

// Insert click into event_clicks table (Assuming table structure: id, event_id, user_id, clicked_at)
$sql = "INSERT INTO event_clicks (event_id, user_id, clicked_at) VALUES (?, ?, NOW())";
$stmt = $conn->prepare($sql);
$stmt->bind_param("ii", $event_id, $user_id);

if ($stmt->execute()) {
    echo json_encode(["status" => "success", "message" => "Click logged!"]);
} else {
    echo json_encode(["status" => "error", "message" => "Failed to log click: " . $conn->error]);
}

$stmt->close();
$conn->close();
?>
