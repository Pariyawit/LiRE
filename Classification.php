<?php 
	include 'header.php';
	include 'class.php';
	include 'query/query_func.php';
	$current_page = 'Classification';

	session_start();
	$_SESSION['classification']=array();
?>
	<body>
		<?php include 'headnavbar.php'; ?>

		<div class="container">

			<div class="jumbotron">
				<form class="form-horizontal" role="form" method="get" action="Classification.php">
					<div class="form-group">
						<label class="col-sm-2 control-label">Select Catagory</label>
						<div class="col-sm-8">
							<select class="form-control" name="seach_class">
								<option>--SELECT CATEGORY--</option>
								<?php foreach($class as $item){
									if (strpos($item[0],'.') == FALSE){
										echo '<option value="'.$item[0].'"';
										if (isset($_GET['seach_class']) && $_GET['seach_class']==$item[0]) echo ' selected ';
										echo '>';
										echo $item[0].' -- '.$item[1].'</option>'; 
									}
									else{
										echo '<option value="'.$item[0].'"';
										if (isset($_GET['seach_class']) && $_GET['seach_class']==$item[0]) echo ' selected ';
										echo '>';
										echo '&nbsp;&nbsp;&nbsp;&nbsp;'.$item[0].' -- '.$item[1].'</option>'; 
									}

								}
								?>
							</select>
						</div>
						<div class="col-sm-2">
							<button type="submit" class="btn btn-default">Search</button>
						</div>
					</div>
				</form>

				<?php if(isset($_GET['seach_class'])):?>
					<table class="table table-bordered table-condensed table-hover">
						<thead>
							<tr>
								<th class="col-sm-10" style="text-align:center">Name</th>
								<th class="col-sm-2" style="text-align:center">#</th>
							</tr>
						</thead>
						<tbody>
						<?php
							$top_loans = top_loan($_GET['seach_class']);
							foreach ($top_loans as $top_loan) {
								echo "<tr>";
								echo "<td>";
								echo '<a href="bookdetail.php?ref='.$top_loan[0].'" style="text-align:center"><div>';
								echo $top_loan[2]."</div></a></td>";
								echo '<td style="padding-left:40px" style="text-align:center">'.$top_loan[1].'</td>';
								echo "</tr>";
						}
						?>
						</tbody>
					</table>
				<?php endif ?>

			</div>

			<div class="container">
				<?php if(isset($_GET['seach_class'])) :?>
					<table class="table table-bordered table-condensed table-hover">
					<thead>
						<tr>
							<th class="col-sm-2" style="text-align:center">Code</th>
							<th class="col-sm-10" style="text-align:center">Name</th>
						</tr>
					</thead>
					<tbody>
					<?php
						$results = search_by_class($_GET['seach_class']);
						foreach ($results as $result) {
							echo "<tr>";
							echo '<td style="padding-left:40px">'.$result[1].'</td>';
							echo "<td>";
							echo '<a href="bookdetail.php?ref='.$result[0].'"><div>';
							echo $result[2]."</div></a></td>";
							echo "</tr>";
							array_push($_SESSION['classification'],$result[0]);
						}
					?>
					</tbody>
					</table>
				<?php endif;?>

			</div>



		</div> <!-- /container -->


		<!-- Bootstrap core JavaScript
		================================================== -->
		<!-- Placed at the end of the document so the pages load faster -->
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
		<script src="../../dist/js/bootstrap.min.js"></script>
	</body>

<?php include 'footer.php';?>