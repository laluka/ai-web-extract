<?php

class Main {
    public function __construct() {
        echo "Hello, World!";
    }
}

if (isset($_GET['action']) && $_GET['action'] === 'echo') {
    if (isset($_GET['message'])) {
        $message = $_GET['message'];
        echo $message;
    } else {
        echo "No message provided";
    }
}

# path router
$path = $_SERVER['REQUEST_URI'];

if ($path === '/') {
    $main = new Main();
    $main->index();
}

if ($path === '/phpinfo') {
    phpinfo();
}

