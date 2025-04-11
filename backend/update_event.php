<?php
error_reporting(E_ALL & ~E_WARNING);  // Suppress warnings
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Allow-Headers: Content-Type");

require_once "db.php";  // Ensure this file is correct

$response = ["status" => "error", "message" => "Invalid request"];

try {
    // Ensure POST method is used
    if ($_SERVER["REQUEST_METHOD"] !== "POST") {
        throw new Exception("Invalid request method");
    }

    // Read JSON input
    $rawData = file_get_contents("php://input");

    // Decode JSON
    $data = json_decode($rawData, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception("Invalid JSON format: " . json_last_error_msg());
    }

    // Validate required fields
    if (!isset($data["event_id"], $data["title"], $data["date"], $data["institution_id"], $data["admin_id"])) {
        http_response_code(400);
        throw new Exception("Missing required fields");
    }

    // Sanitize inputs
    $event_id = intval($data["event_id"]);
    $title = trim($data["title"]);
    $description = isset($data["description"]) ? trim($data["description"]) : "";
    $date = trim($data["date"]);
    $institution_id = intval($data["institution_id"]);
    $admin_id = intval($data["admin_id"]);

    // Check if the event exists and is owned by the correct admin
    $checkQuery = "SELECT id FROM events WHERE id = ? AND institution_id = ? AND admin_id = ?";
    $checkStmt = $conn->prepare($checkQuery);
    $checkStmt->bind_param("iii", $event_id, $institution_id, $admin_id);
    $checkStmt->execute();
    $result = $checkStmt->get_result();

    if ($result->num_rows === 0) {
        http_response_code(404);
        throw new Exception("Event not found or unauthorized.");
    }
    $checkStmt->close();

    // Update the event
    $query = "UPDATE events SET title = ?, description = ?, date = ? WHERE id = ? AND institution_id = ? AND admin_id = ?";
    $stmt = $conn->prepare($query);
    $stmt->bind_param("sssiii", $title, $description, $date, $event_id, $institution_id, $admin_id);

    if ($stmt->execute()) {
        http_response_code(200);
        $response = ["status" => "success", "message" => "Event updated successfully"];
    } else {
        http_response_code(500);
        throw new Exception("Failed to update event: " . $stmt->error);
    }

    // Close statements and connection
    $stmt->close();
    $conn->close();

} catch (Exception $e) {
    http_response_code(500);
    $response["message"] = $e->getMessage();
}

// Return JSON response
echo json_encode($response, JSON_PRETTY_PRINT);
?>
