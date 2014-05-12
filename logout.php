<?php
include 'header.php';
include 'query/query_func.php';

$_SESSION['UserID'] = false;

?>
	<body>
		<div class="container log">
			<div class="jumbotron">
				<h1><span class="glyphicon glyphicon-log-out" style="color:orange"></span>&nbsp;Logging Out...</h1>
				<p>You will be redirected soon</p>
			</div>
		</div> <!-- /container -->

	</body>

<?php 
include 'footer.php';
$path = realpath(dirname(__FILE__));
?>

<script type="text/javascript">
	setTimeout("window.location.href = 'index.php'", 2000);
</script>