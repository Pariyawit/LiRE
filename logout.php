<?php
include 'header.php';
include 'query/query_func.php';

$_SESSION['UserID'] = false;

?>
	<body>
		<div class="container log">
			<div class="jumbotron">
				<h1><span class="glyphicon glyphicon-log-out" style="color:orange"></span>&nbsp;Loging Out</h1>
				<p>You will be redirected soon</p>
			</div>
		</div> <!-- /container -->

	</body>

<?php 
include 'footer.php';
?>

<script src="js/custom.js"></script>

<script type="text/javascript">
	setTimeout("window.location = '<?php echo $_SERVER['HTTP_REFERER'] ?>'", 2000);
</script>