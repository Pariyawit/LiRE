<?php
/*
 * This example shows how new databases can be created.
 *
 * Documentation: http://docs.basex.org/wiki/Clients
 *
 * (C) BaseX Team 2005-12, BSD License
 */
include("BaseXClient.php");

if(!isset($_SESSION['session'])){
	session_start();
}

function search_by_class($num){
	if($num[0] == '0'){
		$num = substr($num,1);
	}
	if(strpos($num,'.')==FALSE){
		$num .= '.';
	}
	try {
			$input = 'declare namespace marcxml = "http://www.loc.gov/MARC21/slim";
						for $record in //marcxml:record/*
						where starts-with($record/marcxml:subfield[@code="k"], "'.$num.'")
							and $record/marcxml:subfield[@code="e"]="BSTB"
						order by $record/marcxml:subfield[@code="k"]
						return ($record/marcxml:subfield[@code="k"],$record/../marcxml:datafield[@tag="200"]/marcxml:subfield[@code="a"],"$")';
						//return ($record/marcxml:subfield[@code="k"],$record/marcxml:datafield[@tag="200"]/marcxml:subfield[@code="a"])';
			$session = new Session("localhost", "1984", "admin", "admin");
			$session->execute('OPEN extraction');
			$query = $session->query($input);
			$results = array();
			$tmp = array();
			// loop through all results
			while($query->more()){
				$x = $query->next();
				if($x == '$'){
					array_push($results,$tmp);
					$tmp = array();
					continue;
				}
				array_push($tmp,$x);
			}
			// close query instance
			$query->close();
			return $results;

	} catch (Exception $e) {
		// print exception
		print $e->getMessage();
		print "<br>Exception";
	}
}
?>
