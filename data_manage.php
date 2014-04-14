<?php 
	include 'header.php';
	include 'class.php';
	include 'database.php';
	$current_page = 'Data Management';

?>
	<body>
		<?php include 'headnavbar.php'; ?>

		<div class="container">

			<div class="jumbotron">
				<h1>Create Database</h1><br>
				<p>/extraction_brest.xml</p>
				<p>/historique.xml</p>
				<p>/toploan.xml</p>
				<input type="submit" class="button btn btn-primary" name="create" value="create" />
			</div>
			<div class="modal"><!-- Place at bottom of page --></div>



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
        data =  {'action': clickBtnValue};
        $.post(ajaxurl, data, function (response) {
            // Response div goes here.
            alert("Database created successfully");
        });
    });
});
</script>