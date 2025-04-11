<?php
include 'db.php';  // Ensure correct path to database connection

header('Content-Type: application/json');

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    echo json_encode(["status" => "error", "message" => "Invalid request method!"]);
    exit();
}

// Debug: Log raw received data
$rawData = file_get_contents("php://input");
error_log("Received Data: " . $rawData); // Log request data for debugging

$data = json_decode($rawData, true);

if (!$data) {
    echo json_encode(["status" => "error", "message" => "Invalid JSON format or empty data!", "received" => $rawData]);
    exit();
}

// Check required fields
if (!isset($data["name"], $data["email"], $data["password"], $data["institution_id"], $data["role"])) {
    echo json_encode(["status" => "error", "message" => "All fields are required!", "received" => $data]);
    exit();
}

$name = $conn->real_escape_string($data["name"]);
$email = $conn->real_escape_string($data["email"]);
$password = password_hash($data["password"], PASSWORD_BCRYPT);
$institution_id = intval($data["institution_id"]);
$role = $conn->real_escape_string($data["role"]);

// Validate role
$allowed_roles = ["student", "admin"];
if (!in_array($role, $allowed_roles)) {
    echo json_encode(["status" => "error", "message" => "Invalid role!"]);
    exit();
}

// Check if email already exists
$sqlCheck = "SELECT id FROM users WHERE email = '$email'";
$resultCheck = $conn->query($sqlCheck);

if ($resultCheck->num_rows > 0) {
    echo json_encode(["status" => "error", "message" => "Email already exists!"]);
    exit();
}

// Insert user into database
$sqlUser = "INSERT INTO users (name, email, password_hash, institution_id, role) 
            VALUES ('$name', '$email', '$password', '$institution_id', '$role')";

if ($conn->query($sqlUser) === TRUE) {
    echo json_encode(["status" => "success", "message" => "User registered successfully!"]);
} else {
    echo json_encode(["status" => "error", "message" => "Failed to register user: " . $conn->error]);
}

$conn->close();
?>



