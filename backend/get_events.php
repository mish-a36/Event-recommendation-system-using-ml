<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");

error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once "db.php";

$response = ["status" => "error", "message" => "Invalid request"];

if (!empty($_GET['institution_id']) && is_numeric($_GET['institution_id'])) {
    $institution_id = intval($_GET['institution_id']);

    $sql = "SELECT 
        events.id, 
        events.title,  
        events.description, 
        events.date,
        events.institution_id,  -- ✅ Added institution_id
        events.admin_id,        -- ✅ Added admin_id
        events.created_at, 
        users.name AS admin_name
    FROM events 
    INNER JOIN users 
        ON events.admin_id = users.id  -- ✅ Corrected admin association
    WHERE events.institution_id = ?
    ORDER BY events.date ASC;
    ";

    if ($stmt = $conn->prepare($sql)) {
        $stmt->bind_param("i", $institution_id);
        $stmt->execute();
        $result = $stmt->get_result();

        $events = [];
        while ($row = $result->fetch_assoc()) {
            $events[] = $row;
        }

        $response = ["status" => "success", "events" => $events];
        $stmt->close();
    } else {
        $response["message"] = "SQL query failed: " . $conn->error;
    }
} else {
    $response["message"] = "Invalid or missing institution ID.";
}

echo json_encode($response, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
$conn->close();
?>
