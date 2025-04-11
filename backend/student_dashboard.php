<?php
session_start();
if (!isset($_SESSION['username'])) {
    header("Location: ../frontend/index.php");
    exit();
}

echo json_encode(["message" => "Welcome " . $_SESSION['username']]);
?>

