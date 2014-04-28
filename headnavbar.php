<?php

$menus = array('Home','Classification');
$files = array('index','classification')

?>


<div class="navbar navbar-default navbar-static-top" role="navigation">
			<div class="container">
				<!--div class="navbar-header">
					<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
						<span class="sr-only">Toggle navigation</span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
					</button>
					<a class="navbar-brand" href="#">LiRE</a>
				</div-->

				<!--div class="navbar-collapse collapse"-->
				<div class="">
					<ul class="nav navbar-nav">
						<?php
							for ($i=0 ;$i<count($files);$i=$i+1) {
								if($menus[$i] == $current_page) echo '<li class="active"><a href="'.$files[$i].'.php">'.$menus[$i].'</a></li>';
								else echo '<li><a href="'.$files[$i].'.php">'.$menus[$i].'</a></li>';
							}

						?>

						<!--li class="dropdown">
							<a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown <b class="caret"></b></a>
							<ul class="dropdown-menu">
								<li><a href="#">Action</a></li>
								<li><a href="#">Another action</a></li>
								<li><a href="#">Something else here</a></li>
								<li class="divider"></li>
								<li class="dropdown-header">Nav header</li>
								<li><a href="#">Separated link</a></li>
								<li><a href="#">One more separated link</a></li>
							</ul>
						</li-->
					</ul>

					<?php if($_SESSION['UserID'] == false): ?>
						<div class="navbar-collapse collapse">
						  	<form class="navbar-form navbar-right" role="form" action="login.php" method="post">
							<div class="form-group">
							  <input name="id" type="text" placeholder="UserID/CardNumber" class="form-control" required>
							</div>
							<button type="submit" class="btn btn-success">Recommendation for Me</button>
						  </form>
						</div><!--/.navbar-collapse -->
					<?php else: ?>
						<?php if($_SESSION['UserID']=='admin'):?>
							<ul class="nav navbar-nav">
							<?php
								if($current_page == 'Data Management') echo '<li class="active"><a href="data_manage.php">Data Management</a></li>';
								else echo '<li><a href="data_manage.php">Data Management</a></li>';
							?>
							</ul>
						<?php endif; ?>
						<div class="navbar-collapse collapse">
						  	<form class="navbar-form navbar-right" role="form" action="logout.php" method="post">
							<div class="form-group">
							  <input name="id" type="text" placeholder="<?php echo $_SESSION['UserID'];?>" class="form-control" disabled="disabled">
							</div>
							<button type="submit" class="btn btn-danger">Log Out</button>
						  </form>
						</div>
					<?php endif; ?>

				</div><!--/.nav-collapse -->
			</div>
		</div>
