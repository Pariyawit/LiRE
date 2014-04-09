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
					if($details[0]=="no") $dOffset = 1; // check if the book description field is available?
					else $dOffset = 0; 
					if($details[1]=="no") $eOffset = 1; // check if the book edition field is available?
					else $eOffset = 0; 
					$book_titre = $details[2];
					$book_description = $details[3];
					$book_author = $details[4 - $dOffset];
					$book_class = $details[5 - $dOffset];
					$book_barcode = $details[6 - $dOffset];
					$book_edition = $details[7 - $dOffset];
					$book_pubname = $details[8 - $dOffset - $eOffset];
					$book_pubplace = $details[9 - $dOffset - $eOffset];
					$book_pubdate = $details[10 - $dOffset - $eOffset];
					echo $book_titre."<br>";
					if($details[0]=="yes") echo $book_description."<br>";
					echo $book_author."<br>";	
					echo $book_class." / ".$book_barcode."<br>";
					if($details[1]=="yes") echo "Edition : ".$book_edition. "<br>";
					echo "Publication : ".$book_pubname.", ".$book_pubplace.", ".$book_pubdate."<br>";	
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