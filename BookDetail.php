<?php 
	session_start();
	include 'header.php';
	include 'query/query_func.php';
	$current_page = 'Book Detail';
	if(isset($_GET['ref'])){
		$details = query_book($_GET['ref']);
		$loan_num = book_loan_time($_GET['ref']);
	}
	$borrowers = get_borrower($_GET['ref']);
	$related_books = array();
	foreach ($borrowers as $borrower) {
		$books = get_books($borrower);
		foreach ($books as $book) {
			if (in_array($book[0], $_SESSION['classification'])){
				array_push($related_books,$book);
			}
		}
	}
	#remove redundancy
	$related_books = array_map("unserialize", array_unique(array_map("serialize", $related_books)));
	/*
	foreach ($related_books as $book) {
		echo $book[0]."    ".$book[1]."<br>";
	}
	*/
?>
	<body>

		<?php include 'headnavbar.php'; ?>

		<div class="container">

			<!-- Main component for a primary marketing message or call to action -->
			<div class="row">
				<div class="jumbotron col-md-8">
					<?php
						//echo $_GET['ref'].'<br>';
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
					?>
					<h2>
					<?php 
						echo $book_titre."<br>";
					?>
					</h2>
					<p>
					<?php

						if($details[0]=="yes") echo $book_description."<br>";
						echo $book_class." / ".$book_barcode."<br>";
						echo "Author : ".$book_author."<br>";	
							if($details[1]=="yes") echo "Edition : ".$book_edition. "<br>";
							echo "Publication : ".$book_pubname.", ".$book_pubplace.", ".$book_pubdate."<br>";	
							echo 'This book has been borrowed by '.$loan_num.' user(s)';

					?>
					</p>
				</div>
				<div class="col-md-4">
					<table class="table table-condensed">
						<thead><tr><th>People who borrow this also borrow</th></tr></thead>
						<tbody>
						<?php
							foreach ($related_books as $book) {
								if($book[0] != ($_GET['ref']))
								echo '<tr><td><a href="bookdetail.php?ref='.$book[0].'"><div>'.$book[1].'</div></a></td></tr>';
							}
						?>
						</tbody>
					</table>
				</div>
			</div>

		</div> <!-- /container -->


		<!-- Bootstrap core JavaScript
		================================================== -->
		<!-- Placed at the end of the document so the pages load faster -->
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
		<script src="../../dist/js/bootstrap.min.js"></script>
	</body>

<?php include 'footer.php';?>