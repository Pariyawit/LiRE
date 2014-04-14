<?php

function query($input,$database){
	if(!isset($session)){
		$session = new Session("localhost", "1984", "admin", "admin");
	}
	$session->execute('OPEN '.$database);
	$query = $session->query($input);
	$results = array();
	$tmp = array();
	// loop through all results
	while($query->more()){
		$x = $query->next();
		if($x == '$'){
			if($tmp !== end($results))array_push($results,$tmp);
			$tmp = array();
			continue;
		}
		array_push($tmp,$x);
	}
	// close query instance
	$query->close();
	//return 2D array results
	return $results;
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
					return ($record/../marcxml:controlfield[@tag="001"]/text(),
							$record/marcxml:subfield[@code="k"]/text(),
							$record/../marcxml:datafield[@tag="200"]/marcxml:subfield[@code="a"]/text(),"$")';
					//return ($record/marcxml:subfield[@code="k"],$record/marcxml:datafield[@tag="200"]/marcxml:subfield[@code="a"])';
		return query($input,'extraction');

	} catch (Exception $e) {
		// print exception
		print $e->getMessage();
		print "<br>Exception";
	}
}

function query_book($ref){
	try {
		$input = 'declare namespace marcxml = "http://www.loc.gov/MARC21/slim";
				for $record in //marcxml:record/*
				where $record/../marcxml:controlfield[@tag="001"]= "'.$ref.'"
				and $record/marcxml:subfield[@code="e"]="BSTB"
				order by $record/marcxml:subfield[@code="k"]
				return (
				$record/../marcxml:datafield[@tag="200"]/marcxml:subfield[@code="a"]/text(),
				$record/marcxml:subfield[@code="k"]/text(),
				$record/../marcxml:datafield[@tag="210"]/marcxml:subfield[@code="c"]/text(),"$")';
					//return ($record/marcxml:subfield[@code="k"],$record/marcxml:datafield[@tag="200"]/marcxml:subfield[@code="a"])';
		//$session = new Session("localhost", "1984", "admin", "admin");
		$results = query($input,'extraction');
		$result = $results[0];
		return $result;

	} catch (Exception $e) {
		// print exception
		print $e->getMessage();
		print "<br>Exception";
	}
}

function book_loan_time($ref){
	try {
		$input = 'for $row in /Document/*
			where $row/NoticeKoha="'.$ref.'"
			return count($row/NoticeKoha="'.$ref.'")';
					//return ($record/marcxml:subfield[@code="k"],$record/marcxml:datafield[@tag="200"]/marcxml:subfield[@code="a"])';
		//$session = new Session("localhost", "1984", "admin", "admin");
		if(!isset($session)){
			$session = new Session("localhost", "1984", "admin", "admin");
		}
		$session->execute('OPEN historique');
		$query = $session->query($input);
		
		$results = array();
		while($query->more()){
			array_push($results,$query->next());
		}
		// close query instance
		$query->close();
		return count($results);

	} catch (Exception $e) {
		// print exception
		print $e->getMessage();
		print "<br>Exception";
	}
}

?>
