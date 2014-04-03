<?php

$menus = ['Index','Classification'];

?>


<div class="navbar navbar-default navbar-static-top" role="navigation">
			<div class="container">
				<div class="navbar-header">
					<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
						<span class="sr-only">Toggle navigation</span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
					</button>
					<a class="navbar-brand" href="#">LiRE</a>
				</div>

				<div class="navbar-collapse collapse">
					<ul class="nav navbar-nav">
						<?php
							foreach ($menus as $menu) {
								if($menu == $current_page) echo '<li class="active"><a href="'.$menu.'.php">'.$menu.'</a></li>';
								else echo '<li><a href="'.$menu.'.php">'.$menu.'</a></li>';
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
					<ul class="nav navbar-nav navbar-right">
						<!--li><a href="database.php">Connect to Database</a></li>
						<li class="active"><a>Static top</a></li-->
					</ul>
				</div><!--/.nav-collapse -->
			</div>
		</div>
