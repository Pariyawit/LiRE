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
				<h1>Create Database</h1>
				<h3>Create and Open Database from folder database/<br>
				 	Run python from python/ to make .xml file<br>
					This takes long time before finish</h3><br>
				<p>/extraction_brest.xml</p>
				<p>/historique.xml</p>
				<p>/old_lecteur_brest.xml</p>
				<p>/wordnetfrench.xml</p>
				<p><i>run toploanBuild.py</i><br>/toploan.xml</p>
				<p><i>run bookrefBuild.py</i><br>/bookref.xml</p>
				<p><i>run keywordBuild.py</i><br>/keywordXML.xml</p>
				<p><i>run keywordCount.py</i><br></p>
				<p><i>run relatedBookBuild.py</i><br>/relatedBook.xml<br>/relatedMatrix.txt</p>
				<p><i>run loanfreq.py</i><br>
					/loanfreqtable.xml<br>
					/loankeywordfreqtable.xml</p>
				<p><i>run season.py</i><p>
				<input type="submit" class="button btn btn-primary" name="create" value="create" />
				<br>
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