<?php
if (isset($_POST['action'])) {
    switch ($_POST['action']) {
        case 'create':
            create();
            break;
        case 'recommend':
            recommend(($_POST['UserID']);
            break;
    }
}

function recommend($UserID) {
    echo "The recommend function is called.";
    $results = exec('python python/getRecomdationMatrix.py '.$UserID);
    #return $results;
    exit;
}

function create() {
    echo "The create function is called.";
    include 'database.php';
    connect_db();
    exit;
}
?>