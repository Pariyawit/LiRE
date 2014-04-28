<?php 
	session_start();
	include 'header.php';
	include 'class.php';
	include 'query/query_func.php';
	$current_page = 'History';

	$histories = get_books_from_codebarre($_SESSION['UserID']);
?>
	<body>
		<?php include 'headnavbar.php'; ?>

			<div class="container">
					<table class="table table-bordered table-hover">
					<thead>
						<tr>
							<th class="col-sm-2" style="text-align:center">Date</th>
							<th class="col-sm-8" style="text-align:center">Name</th>
							<th class="col-sm-2" style="text-align:center">Type</th>
						</tr>
					</thead>
					<tbody>
					<?php
						foreach ($histories as $result) {
							echo "<tr>";
							echo '<td style="text-align:center;">'.$result[2].'</td>';
							echo "<td>";
							echo '<a href="bookdetail.php?ref='.$result[0].'"><div>';
							echo $result[1]."</div></a></td>";
							echo '<td style="text-align:center;">'.$result[3].'</td>';
							echo "</tr>";

						}
					?>
					</tbody>
					</table>
			</div>



		</div> <!-- /container -->
	</body>

<?php include 'footer.php';?>