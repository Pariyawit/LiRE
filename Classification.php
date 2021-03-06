<?php 
	session_start();
	include 'header.php';
	include 'class.php';
	include 'query/query_func.php';
	$current_page = 'Classification';

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
								<th class="col-sm-2" style="text-align:center">Time(s)</th>
								<th class="col-sm-10" style="text-align:center">Top 5 Most Borrowed Books</th>
							</tr>
						</thead>
						<tbody>
						<?php
							$top_loans = top_loan($_GET['seach_class']);
							foreach ($top_loans as $top_loan) {
								echo "<tr>";
								echo '<td style="text-align:center">'.$top_loan[1].'</td>';
								echo '<td><a href="bookdetail.php?ref='.$top_loan[0].'" style="text-align:center"><div>';
								echo $top_loan[2]."</div></a></td>";
								echo "</tr>";
						}
						?>
						</tbody>
					</table>
				<?php endif ?>

				<?php if((!isset($_GET['seach_class'])) and $_SESSION['UserID']):?>
					<table class="table table-bordered table-condensed table-hover">
						<thead>
							<tr>
								<th class="col-sm-2" style="text-align:center">Code</th>
								<th class="col-sm-10" style="text-align:center">Recommendation for you</th>
							</tr>
						</thead>
						<tbody>
						<?php
							$results = shell_exec('python python/getRecommendation.py '.$_SESSION['UserID']);
							$recom_books = explode(",",$results);
							foreach ($recom_books as $book_ref) {
								$CodeName = getBookCodeName($book_ref);
								echo '<tr>';
								echo '<td style="padding-left:5%;">'.$CodeName[0].'</td>';
								echo '<td style="padding-left:5%;"><a href="bookdetail.php?ref='.$book_ref.'"><div>'.$CodeName[1].'</div></a></td></tr>';
								$i = $i+1;
								if($i>=10)break;
							}
						?>
						</tbody>
					</table>
				<?php endif ?>

				<?php if(isset($_GET['seach_class']) and $_SESSION['UserID']):?>
					<table class="table table-bordered table-condensed table-hover">
						<thead>
							<tr>
								<th class="col-sm-2" style="text-align:center">Code</th>
								<th class="col-sm-10" style="text-align:center">Recommendation for you in this Category</th>
							</tr>
						</thead>
						<tbody>
						<?php
							$results = shell_exec('python python/getRecommendation.py '.$_SESSION['UserID'].' '.$_GET['seach_class']);
							$recom_books = explode(",",$results);
							foreach ($recom_books as $book_ref) {
								$CodeName = getBookCodeName($book_ref);
								echo '<tr>';
								echo '<td style="padding-left:5%;">'.$CodeName[0].'</td>';
								echo '<td style="padding-left:5%;"><a href="bookdetail.php?ref='.$book_ref.'"><div>'.$CodeName[1].'</div></a></td></tr>';
								$i = $i+1;
								if($i>=10)break;
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
							<th class="col-sm-10" style="text-align:center">Book Title</th>
						</tr>
					</thead>
					<tbody>
					<?php
						$results = search_by_class($_GET['seach_class']);
						foreach ($results as $result) {
							echo "<tr>";
							echo '<td style="padding-left:5%;">'.$result[1].'</td>';
							echo '<td style="padding-left:5%;">';
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
	</body>

<?php include 'footer.php';?>