<?php


if(!class_exists('Session')) {
	include 'BaseXClient.php';
}

$session = new Session("localhost", "1984", "admin", "admin");

function connect_db(){
	try {
			echo "Connecting to Database...";
			// create session
			if(!isset($session)){
				$session = new Session("localhost", "1984", "admin", "admin");
			}
			
			// create new database
			$path = realpath(dirname(__FILE__));

			$file = $path."/extraction_brest_edit.xml";
			$session->execute('CREATE DB extraction '.$file);

			$file = $path."/historique_escap.xml";
			$session->execute('CREATE DB historique '.$file);

			print $session->info();		
			header('Location: ' . $_SERVER['HTTP_REFERER']);
		}

	/*
		// drop database
		$session->execute("drop db extraction");

		// close session
		$session->close();
		print "DONE";
	*/
	catch (Exception $e) {
		// print exception
		print $e->getMessage();
	}
}

function isConnect_db(){
	if(!isset($session)){
		$session = new Session("localhost", "1984", "admin", "admin");
	}
	$session->execute('CHECK extraction');
	if(strpos($session->info(),'create')){
		connect_db();
	}
}

?>
