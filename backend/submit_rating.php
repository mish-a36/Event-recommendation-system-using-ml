<?php
header("Content-Type: application/json");
require_once "db.php"; // Ensure database connection is included

$response = ["status" => "error", "message" => "Invalid request"];

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $data = json_decode(file_get_contents("php://input"), true);

    // Validate required fields
    if (!isset($data["user_id"], $data["user_name"], $data["event_id"], 
               $data["event_title"], $data["event_description"], $data["event_date"], $data["rating"])) {
        $response["message"] = "Missing required fields!";
        echo json_encode($response);
        exit();
    }

    // Extract and sanitize input
    $user_id = intval($data["user_id"]);
    $user_name = trim($data["user_name"]);
    $event_id = intval($data["event_id"]);
    $event_title = trim($data["event_title"]);
    $event_description = trim($data["event_description"]);
    $event_date = trim($data["event_date"]);
    $rating = intval($data["rating"]);

    // Ensure rating is between 1 and 5
    if ($rating < 1 || $rating > 5) {
        $response["message"] = "Invalid rating value! Must be between 1 and 5.";
        echo json_encode($response);
        exit();
    }

    try {
        $conn = new mysqli($host, $username, $password, $dbname);

        if ($conn->connect_error) {
            throw new Exception("Database connection failed: " . $conn->connect_error);
        }

        // Insert or update the rating in the `user_interest` table
        $sql = "INSERT INTO user_interest (user_id, user_name, event_id, event_title, event_description, event_date, rating) 
                VALUES (?, ?, ?, ?, ?, ?, ?) 
                ON DUPLICATE KEY UPDATE rating = VALUES(rating), event_date = VALUES(event_date)";
        
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("isssssi", $user_id, $user_name, $event_id, $event_title, $event_description, $event_date, $rating);

        if ($stmt->execute()) {
            $response = ["status" => "success", "message" => "Rating submitted successfully!"];
        } else {
            throw new Exception("Failed to submit rating: " . $stmt->error);
        }

        $stmt->close();
        $conn->close();
    } catch (Exception $e) {
        $response["message"] = $e->getMessage();
    }
}

echo json_encode($response);
?>
