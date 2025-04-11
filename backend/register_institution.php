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
if (!isset($data["institution_name"], $data["email"], $data["password"], $data["location"], $data["name"])) {
    echo json_encode(["status" => "error", "message" => "All fields are required!", "received" => $data]);
    exit();
}

$institution_name = $conn->real_escape_string($data["institution_name"]);
$admin_name = $conn->real_escape_string($data["name"]);
$email = $conn->real_escape_string($data["email"]);
$password = password_hash($data["password"], PASSWORD_BCRYPT);
$location = $conn->real_escape_string($data["location"]);

$sqlInstitution = "INSERT INTO institutions (institution_name, email, password, location) VALUES ('$institution_name', '$email', '$password', '$location')";

if ($conn->query($sqlInstitution) === TRUE) {
    $institution_id = $conn->insert_id;

    $sqlUser = "INSERT INTO users (name, email, password_hash, institution_id, role) 
                VALUES ('$admin_name', '$email', '$password', '$institution_id', 'admin')";

    if ($conn->query($sqlUser) === TRUE) {
        echo json_encode(["status" => "success", "message" => "Institution and admin registered successfully!"]);
    } else {
        echo json_encode(["status" => "error", "message" => "Institution registered, but failed to create admin: " . $conn->error]);
    }
} else {
    echo json_encode(["status" => "error", "message" => "Failed to register institution: " . $conn->error]);
}

$conn->close();

?>
