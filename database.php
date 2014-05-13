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
			
			set_time_limit(0);
			// create new database
			$path = realpath(dirname(__FILE__));
			$path = $path."/database";

			$file = $path."/extraction_brest_edit.xml";
			$session->execute('CREATE DB extraction '.$file);

			$file = $path."/historique.xml";
			$session->execute('CREATE DB historique '.$file);

			$file = $path."/old_lecteur_brest.xml";
			$session->execute('CREATE DB lecteur '.$file);

			$file = $path."/wordnetfrench.xml";
			$session->execute('CREATE DB wordnetfrench '.$file);

			exec('python python/toploanBuild.py');
			$file = $path."/toploan.xml";
			$session->execute('CREATE DB toploan '.$file);

			exec('python python/bookrefBuild.py');
			$file = $path."/bookref.xml";
			$session->execute('CREATE DB bookref '.$file);

			exec('python python/keywordBuild.py');
			$file = $path."/keywordXML.xml";
			$session->execute('CREATE DB keyword '.$file);

			exec('python python/keywordCount.py');

			exec('python python/relatedBookBuild.py');
			$file = $path."/relatedBook.xml";
			$session->execute('CREATE DB relatedBook '.$file);

			exec('python python/loanfreq.py');
			$file = $path."/loanfreqtable.xml";
			$session->execute('CREATE DB loanfreq '.$file);
			$file = $path."/loankeywordfreqtable.xml";
			$session->execute('CREATE DB loankeyfreq '.$file);

			print $session->info();		
			header('Location: ' . $_SERVER['HTTP_REFERER']);
		}

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
