<?php
include 'header.php';
include 'query/query_func.php';

$id = trim($_POST['id']);

if($id == 'admin'){
	$result = 'true';
	$_SESSION['UserID'] = 'admin';
}else{
	$result = userCheck($id);
	if($result == 'true'){
		$_SESSION['UserID'] = $id;
	}
}

?>
	<body>
		<div class="container log">
			<div class="jumbotron">
				<?php if($result=='true') :?>
					<h1><span class="glyphicon glyphicon-ok-circle" style="color:green;"></span>&nbsp;Log in Successful</h1>
				<?php else :?>
					<h1><span class="glyphicon glyphicon-remove-circle" style="color:red;"></span>&nbsp;User not Found</h1>
				<?php endif; ?>
				<p>You will be redirected soon</p>
			</div>
		</div> <!-- /container -->
	</body>

<?php 
include 'footer.php';
?>
<script type="text/javascript">
	setTimeout("window.location = '<?php echo $_SERVER['HTTP_REFERER'] ?>'", 2000);
</script>