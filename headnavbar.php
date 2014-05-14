<?php

if($_SESSION['UserID'] == false){
	$menus = array('Home','Classification');
}
else{
	$menus = array('Home','Classification','History');
}
$files = array('index','classification','history')

?>


<div class="navbar navbar-default navbar-static-top" role="navigation">
	<div class="container">
		<div class="navbar-header">
			<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse" style="width=90px">
				<span class="sr-only">Toggle navigation</span>
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
			</button>
			<a class="navbar-brand" href="index.php"><b>LiRE</b></a>
			<a class="visible-xs navbar-brand" href="#"><?php echo $current_page; ?></a>
		</div>

		<div class="navbar-collapse collapse">
		<!--div class=""-->
			<ul class="nav navbar-nav">
				<?php
					for ($i=0 ;$i<count($menus);$i=$i+1) {
						if($menus[$i] == $current_page) echo '<li class="active"><a href="'.$files[$i].'.php">'.$menus[$i].'</a></li>';
						else echo '<li><a href="'.$files[$i].'.php">'.$menus[$i].'</a></li>';
					}

				?>

			</ul>

			<?php if($_SESSION['UserID'] == false): ?>
				<!--div class="navbar"-->
				  	<form class="navbar-form navbar-right" role="form" action="login.php" method="post">
					<div class="form-group">
					  <input name="id" type="text" placeholder="UserID/CardNumber" class="form-control" required>
					</div>
					<button type="submit" class="btn btn-success">Recommendation for Me</button>
				  </form>
				<!--/div--><!--/.navbar-collapse -->
			<?php else: ?>
				<?php if($_SESSION['UserID']=='admin'):?>
					<ul class="nav navbar-nav">
					<?php
						if($current_page == 'Data Management') echo '<li class="active"><a href="data_manage.php">Data Management</a></li>';
						else echo '<li><a href="data_manage.php">Data Management</a></li>';
					?>
					</ul>
				<?php endif; ?>
				  	<form class="navbar-form navbar-right" role="form" action="logout.php" method="post">
					<div class="form-group">
					  <input name="id" type="text" placeholder="<?php echo $_SESSION['UserID'];?>" class="form-control" disabled="disabled">
					</div>
					<button type="submit" class="btn btn-danger">Log Out</button>
				  </form>
			<?php endif; ?>

		</div><!--/.nav-collapse -->
	</div><!--container-->
</div>
