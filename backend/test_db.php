<?php
include 'db.php';

header("Content-Type: application/json");

if ($conn->ping()) {
    echo json_encode(["success" => "Database connection is successful"]);
} else {
    echo json_encode(["error" => "Database connection failed"]);
}
?>
