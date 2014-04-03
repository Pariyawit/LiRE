<?php
/*
 * This example shows how new databases can be created.
 *
 * Documentation: http://docs.basex.org/wiki/Clients
 *
 * (C) BaseX Team 2005-12, BSD License
 */
include("BaseXClient.php");
try {
	if(!isset($_SESSION['session'])){
		session_start();
		// create session
		$_SESSION['session'] = new Session("localhost", "1984", "admin", "admin");
		
		// create new database
		$path = realpath(dirname(__FILE__));

		$file = $path."/extraction_brest_edit.xml";
		
		$_SESSION['session']->execute('CREATE DB extraction '.$file);

		print $_SESSION['session']->info();		

	}

/*
	// drop database
	$session->execute("drop db extraction");

	// close session
	$session->close();
	print "DONE";
*/

} 
catch (Exception $e) {
	// print exception
	print $e->getMessage();
}

?>
