<?php
header("Content-Type: application/json");
require_once "db.php"; // Include database connection

if ($_SERVER["REQUEST_METHOD"] === "GET") {
    if (!isset($_GET["user_id"]) || !isset($_GET["event_id"])) {
        echo json_encode(["error" => "User ID and Event ID are required"]);
        exit;
    }

    $user_id = intval($_GET["user_id"]);
    $event_id = intval($_GET["event_id"]);

    // Fetch rating for the specific user and event
    $sql = "SELECT rating FROM user_interest WHERE user_id = ? AND event_id = ?";  // Fixed column name
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ii", $user_id, $event_id);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($row = $result->fetch_assoc()) {
        echo json_encode(["rating" => intval($row["rating"])]); // Return rating as an integer
    } else {
        echo json_encode(["error" => "No rating found"]); // Return an error if no row exists
    }
} else {
    echo json_encode(["error" => "Invalid request method"]);
}
?>
