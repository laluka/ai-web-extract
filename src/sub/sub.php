<?php
# path router
$path = $_SERVER['REQUEST_URI'];

if ($path === '/sub') {
    echo "Sub DIR & Sub FILE";
}

if ($path === '/download') {
    echo "Download File";
    if (isset($_GET['file'])) {
        $file = $_GET['file'];
        $file_path = __DIR__ . '/' . $file;
        if (file_exists($file_path)) {
            header('Content-Type: application/octet-stream');
            header('Content-Disposition: attachment; filename="' . basename($file_path) . '"');
            readfile($file_path);
        } else {
            echo "File not found";
        }
    } else {
        echo "No file provided";
    }
}

