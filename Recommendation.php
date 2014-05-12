<?php 
	include 'header.php';
	include 'query/query_func.php';
	$current_page = 'Recommendation';
	#set_time_limit(0);
	$results = shell_exec('python python/getRecommendationMatrix.py '.$_SESSION['UserID']);
	#var_dump($results);
	if($results=="UserID not found"){
		
	}
	$recom_books = explode(",",$results);
	#var_dump($recom_books)
?>
	<body>
		<?php include 'headnavbar.php'; ?>

		<div class="container">

			<div class="jumbotron">
				<h1>Recommendation</h1>
				<h2>for <?php echo $_SESSION['UserID'] ?></h2>
				<br>
			</div>
			<div class="modal"><!-- Place at bottom of page --></div>

			<div class="row">
				<table class="table table-condensed">
						<thead><tr><th>Code</th><th>Book Title</th></tr></thead>
						<tbody>
						<?php
							$i=0;
							foreach ($recom_books as $book_ref) {
								$CodeName = getBookCodeName($book_ref);
								echo '<tr><td>'.$CodeName[0].'</td><td><a href="bookdetail.php?ref='.$book_ref.'"><div>'.$CodeName[1].'</div></a></td></tr>';
								$i = $i+1;
								if($i>=10)break;
							}
						?>
						</tbody>
					</table>
			</div>


		</div> <!-- /container -->


		<!-- Bootstrap core JavaScript
		================================================== -->
		<!-- Placed at the end of the document so the pages load faster -->
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
		<script src="../../dist/js/bootstrap.min.js"></script>
	</body>

<?php include 'footer.php';?>

<script type="text/JavaScript"> 

$body = $("body");

$(document).on({
    ajaxStart: function() { $body.addClass("loading");    },
    ajaxStop: function() { $body.removeClass("loading"); }    
});


$(document).ready(function(){
    $('.button').click(function(){
        var clickBtnValue = $(this).val();
        var ajaxurl = 'ajax.php',
        data =  {'action': clickBtnValue,
    			'UserID': <?php echo json_encode($_SESSION['UserID']); ?>};
        $.post(ajaxurl, data, function (response) {
            // Response div goes here.
            //alert("Finish Searching");
            alert(<?php echo json_encode($results); ?>);
        });
    });
});
</script>