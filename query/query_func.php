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
			where $record/../marcxml:controlfield[@tag="001"] ="'.$ref.'"
			and $record/marcxml:subfield[@code="e"]="BSTB"
			order by $record/marcxml:subfield[@code="k"]
			return (
				if(exists($record/../marcxml:datafield[@tag="200"]/marcxml:subfield[@code="e"]/text()))
					then "yes" else "no",
				if(exists($record/../marcxml:datafield[@tag="205"]/marcxml:subfield[@code="a"]/text()))
					then "yes" else "no",
				$record/../marcxml:datafield[@tag="200"]/marcxml:subfield[@code="a"]/text(),
				$record/../marcxml:datafield[@tag="200"]/marcxml:subfield[@code="e"]/text(),
				$record/../marcxml:datafield[@tag="200"]/marcxml:subfield[@code="f"]/text(),
				$record/../marcxml:datafield[@tag="995"]/marcxml:subfield[@code="k"]/text(),
				$record/../marcxml:datafield[@tag="995"]/marcxml:subfield[@code="f"]/text(),
				$record/../marcxml:datafield[@tag="205"]/marcxml:subfield[@code="a"]/text(),
				$record/../marcxml:datafield[@tag="210"]/marcxml:subfield[@code="c"]/text(),
				$record/../marcxml:datafield[@tag="210"]/marcxml:subfield[@code="a"]/text(),
				$record/../marcxml:datafield[@tag="210"]/marcxml:subfield[@code="d"]/text(),
				"$")';
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
			return $row/LecteurCode/text()';
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
		return count(array_unique($results));

	} catch (Exception $e) {
		// print exception
		print $e->getMessage();
		print "<br>Exception";
	}
}

function top_loan($classification){
	if($classification[0] == '0'){
		$classification = substr($classification,1);
	}
	if(strpos($classification,'.')==FALSE){
		$classification .= '.';
	}
	try {
		$input = 'for $row in /Document/class[@mainclass="'.$classification.'"]/*
					return ($row/@NoticeKoha/string(),$row/@loanNum/string(),$row/text())';
					//return ($record/marcxml:subfield[@code="k"],$record/marcxml:datafield[@tag="200"]/marcxml:subfield[@code="a"])';
		//$session = new Session("localhost", "1984", "admin", "admin");
		if(!isset($session)){
			$session = new Session("localhost", "1984", "admin", "admin");
		}
		$session->execute('OPEN toploan');
		$query = $session->query($input);
		
		$results = array();
		while($query->more()){
			$result = array();
			array_push($result,$query->next()); #get Notice koha
			array_push($result,$query->next()); #get loan num
			array_push($result,$query->next()); #get Name
			array_push($results,$result);
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

#get reader from book reference
function get_borrower($NoticeKoha){
	try {
		$input = 'for $row in /Document/*
					where $row/NoticeKoha="'.$NoticeKoha.'"
					return $row/LecteurCode/text()';
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
		return array_unique($results);

	} catch (Exception $e) {
		// print exception
		print $e->getMessage();
		print "<br>Exception";
	}
}


#get book from LecteurCode
function get_books($NoticeKoha){
	try {
		$input = 'for $row in /Document/*
					where $row/LecteurCode="'.$NoticeKoha.'"
					return ($row/NoticeKoha/text(),$row/Titre/text())';
		if(!isset($session)){
			$session = new Session("localhost", "1984", "admin", "admin");
		}
		$session->execute('OPEN historique');
		$query = $session->query($input);
		$results = array();
		while($query->more()){
			$result = array();
			array_push($result,$query->next());
			array_push($result,$query->next());
			array_push($results,$result);
		}
		// close query instance
		$query->close();
		#remove redundancy in the result
		return array_map("unserialize", array_unique(array_map("serialize", $results)));

	} catch (Exception $e) {
		// print exception
		print $e->getMessage();
		print "<br>Exception";
	}
}
?>
