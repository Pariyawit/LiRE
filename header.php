<!DOCTYPE html>
<?php

$path = realpath(dirname(__FILE__));

if (session_status() === PHP_SESSION_NONE){
        session_start();
}
if(!class_exists('Session')) {
    include 'BaseXClient.php';
}
#if user not login
if(!isset($_SESSION['UserID'])){
    $_SESSION['UserID'] = false;
    $_SESSION['timeout'] = time();
}else if($_SESSION['UserID']==false){
    $_SESSION['timeout'] = time();
}
#user login, check session timeout
else if ($_SESSION['timeout'] + 10 * 60 < time()) {
    $_SESSION['UserID'] = false;
    header("Location: index.php");
    die();
}
?>


<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="shortcut icon" href="media/telecom-bretagne.gif">

    <title>LiRE</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="navbar-static-top.css" rel="stylesheet">
    <link href="css/custom.css" rel="stylesheet">

    <!-- Just for debugging purposes. Don't actually copy this line! -->
    <!--[if lt IE 9]><script src="../../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
