<?php
if (isset($_POST['action'])) {
    switch ($_POST['action']) {
        case 'create':
            create();
            break;
        case 'select':
            select();
            break;
    }
}

function select() {
    echo "The select function is called.";
    exit;
}

function create() {
    echo "The create function is called.";
    include 'database.php';
    connect_db();
    exit;
}
?>