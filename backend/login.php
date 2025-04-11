<?php
header("Content-Type: application/json");
require_once "db.php";  // Include database connection

$data = json_decode(file_get_contents("php://input"), true);

if (!isset($data["email"]) || !isset($data["password"])) {
    echo json_encode(["status" => "error", "message" => "Email and password are required"]);
    exit();
}

$email = $data["email"];
$password = $data["password"];

// Fetch user details based on email
$stmt = $conn->prepare("SELECT id, name, role, institution_id, password_hash FROM users WHERE email = ?");
$stmt->bind_param("s", $email);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows > 0) {
    $user = $result->fetch_assoc();
    
    // ✅ Verify hashed password
    if (password_verify($password, $user["password_hash"])) {
        echo json_encode([
            "status" => "success",
            "user" => [
                "id" => $user["id"],
                "name" => $user["name"],
                "role" => $user["role"],
                "institution_id" => $user["institution_id"]
            ]
        ]);
    } else {
        echo json_encode(["status" => "error", "message" => "Invalid password"]);
    }
} else {
    echo json_encode(["status" => "error", "message" => "User not found"]);
}

$stmt->close();
$conn->close();
?>


