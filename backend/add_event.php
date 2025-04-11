<?php
include 'db.php';

header('Content-Type: application/json');

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    echo json_encode(["status" => "error", "message" => "Invalid request method!"]);
    exit();
}

// Debug: Log raw received data
$rawData = file_get_contents("php://input");
error_log("Received Data: " . $rawData); // Log to PHP error log

$data = json_decode($rawData, true);

if (!$data) {
    echo json_encode(["status" => "error", "message" => "Invalid JSON format or empty data!", "received" => $rawData]);
    exit();
}

// Check required fields
if (!isset($data["title"], $data["date"], $data["institution_id"], $data["admin_id"], $data["category"])) {
    echo json_encode(["status" => "error", "message" => "Missing required fields!", "received" => $data]);
    exit();
}

$title = $conn->real_escape_string($data["title"]);
$description = isset($data["description"]) ? $conn->real_escape_string($data["description"]) : null;
$description_extra = isset($data["description_extra"]) ? $conn->real_escape_string($data["description_extra"]) : null;
$date = $conn->real_escape_string($data["date"]);
$institution_id = intval($data["institution_id"]);
$admin_id = intval($data["admin_id"]);
$category = $conn->real_escape_string($data["category"]); // Sanitize category input

$sql = "INSERT INTO events (title, description, description_extra, date, institution_id, admin_id, category) 
        VALUES (?, ?, ?, ?, ?, ?, ?)";

$stmt = $conn->prepare($sql);
$stmt->bind_param("ssssiss", $title, $description, $description_extra, $date, $institution_id, $admin_id, $category);

if ($stmt->execute()) {
    echo json_encode(["status" => "success", "message" => "Event added successfully!"]);
} else {
    echo json_encode(["status" => "error", "message" => "Failed to add event: " . $conn->error]);
}

$stmt->close();
$conn->close();
?>
