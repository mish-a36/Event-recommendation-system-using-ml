<?php
include 'db.php';

header('Content-Type: application/json');

if (!isset($_GET['user_id']) || !is_numeric($_GET['user_id']) || intval($_GET['user_id']) <= 0) {
    echo json_encode(["status" => "error", "message" => "Valid User ID is required"]);
    exit();
}

$user_id = intval($_GET['user_id']);
$api_url = "http://127.0.0.1:5000/recommend?user_id=" . $user_id;

// Debugging logs
error_log("🟢 Calling Flask API: " . $api_url);

$response = @file_get_contents($api_url); // Suppress warnings for cleaner error handling

if ($response === FALSE) {
    error_log("🔴 Failed to connect to Flask API at: " . $api_url);
    echo json_encode(["status" => "error", "message" => "Failed to connect to recommendation API"]);
    exit();
}

// Decode JSON response
$recommendations = json_decode($response, true);

if (json_last_error() !== JSON_ERROR_NONE) {
    error_log("🔴 Invalid JSON response from Flask API: " . $response);
    echo json_encode(["status" => "error", "message" => "Invalid JSON response from recommendation API"]);
    exit();
}

// Handle empty recommendations
if (empty($recommendations)) {
    echo json_encode(["status" => "success", "message" => "No recommendations found", "recommendations" => []]);
    exit();
}

// Return recommendations
echo json_encode(["status" => "success", "recommendations" => $recommendations]);
?>
