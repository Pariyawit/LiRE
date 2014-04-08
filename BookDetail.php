<?php 
	include 'header.php';
	include 'query/query_func.php';
	$current_page = 'Book Detail';
	if(isset($_GET['ref'])){
		$details = query_book($_GET['ref']);
		$loan_num = book_loan_time($_GET['ref']);
	}
?>
	<body>

		<?php include 'headnavbar.php'; ?>

		<div class="container">

			<!-- Main component for a primary marketing message or call to action -->
			<div class="jumbotron">
				<h1>Book Detail</h1>
				<p>
				<?php
					echo $_GET['ref'].'<br>';
					if(isset($_GET['ref'])){
						foreach ($details as $value) {
							echo $value."<br>";
						}
					}
					echo 'This book has been loan '.$loan_num.' time(s)';
				?>
				</p>
			</div>

		</div> <!-- /container -->


		<!-- Bootstrap core JavaScript
		================================================== -->
		<!-- Placed at the end of the document so the pages load faster -->
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
		<script src="../../dist/js/bootstrap.min.js"></script>
	</body>

<?php include 'footer.php';?>