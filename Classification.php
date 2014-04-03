<?php 
	include 'header.php';
	include 'class.php';
	include 'query/search_by_class.php';
	$current_page = 'Classification';
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
								<?php foreach($class as $item): ?>
									<?php if (strpos($item[0],'.') == FALSE):?>
										<option value=<?php echo '"'.$item[0].'"'; ?> > <?php echo $item[0]." -- ".$item[1]; ?></option>
									<?php else: ?>
										<option value=<?php echo '"'.$item[0].'"'; ?> > <?php echo "&nbsp;&nbsp;&nbsp;".$item[0]." -- ".$item[1]; ?></option>
									<?php endif; ?>
								<?php endforeach;?>
							</select>
						</div>
						<div class="col-sm-2">
							<button type="submit" class="btn btn-default">Search</button>
						</div>
					</div>
				</form>
			</div>
			<div class="container">
				<?php if(isset($_GET['seach_class'])) :?>
					<table class="table table-bordered table-condensed table-hover">
					<thead>
						<tr>
							<th class="col-sm-4">Code</th>
							<th class="col-sm-8">Name</th>
						</tr>
					</thead>
					<tbody>
					<?php
						$results = search_by_class($_GET['seach_class']);
						foreach ($results as $result) {
							echo "<tr>";
							echo "<td>".$result[0]."</td>";
							echo "<td>".$result[1]."</td>";
							echo "</tr>";
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