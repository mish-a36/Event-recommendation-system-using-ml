<?php
include 'db.php';

header('Content-Type: application/json');

// Check if event_id is passed
if (!isset($_GET['event_id'])) {
    echo json_encode(["status" => "error", "message" => "Event ID is required"]);
    exit();
}

$event_id = intval($_GET['event_id']);  // Convert to integer for safety
error_log("Received event_id: " . $event_id);  // Log event_id for debugging

// Fetch event details from the database
$sql = "SELECT title, date, description_extra FROM events WHERE id = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $event_id);
$stmt->execute();
$result = $stmt->get_result();

if ($row = $result->fetch_assoc()) {
    echo json_encode(["status" => "success", "title" => $row['title'], "date" => $row['date'], "description_extra" => $row['description_extra']]);
} else {
    error_log("No event found with ID: " . $event_id);  // Log issue
    echo json_encode(["status" => "error", "message" => "Event not found"]);
}

$stmt->close();
$conn->close();
?>
