<?php
	include '../class.php';
	include 'query_func.php';
	if(!class_exists('Session')) {
		include '../BaseXClient.php';
	}

try{
	$session = new Session("localhost", "1984", "admin", "admin");
	$statistic = array();
	//$session->execute('OPEN extraction');

//	$class = array(
//		array("00","GENERALITES"),
//		array("00.1"," Généralités sur les sciences"),
//		array("00.2","Enseignement - Recherche"));

	foreach ($class as $category) {
		set_time_limit(30);
		$session->execute('OPEN extraction');
		$num = $category[0];
		if($num[0] == '0'){
			$num = substr($num,1);
		}
		if(strpos($num,'.') == FALSE){
			$main_cat = $num;
			echo '--------'.$num.'<br>';
			$num .= '.';
//			continue;
		}

		$statistic[$num] = array();

		$input = 'declare namespace marcxml = "http://www.loc.gov/MARC21/slim";
				for $record in //marcxml:record/*
				where starts-with($record/marcxml:subfield[@code="k"], "'.$num.'")
					and $record/marcxml:subfield[@code="e"]="BSTB"
				return $record/../marcxml:controlfield[@tag="001"]/text()';
		$query = $session->query($input);
		$numKoha = array();
		while($query->more()){
			array_push($numKoha,$query->next());
		}
		//---------------------------------------------------------------------
		$code = array();
		foreach ($numKoha as $ref) {
			$loan = book_loan_time($ref);
			//echo $ref."  ".$loan."<br>";
			$code[$ref] = $loan;
		}
		echo '-------------------------------------------<br>';
			arsort($code);
			$i=0;
			$top5 = array();
			foreach ($code as $key => $value) {
				if($value==0) break;
				echo $key.'---'.$value.'<br>';
				$top5[$key] = $value;
				$i=$i+1;
				if($i>=5) break;
			}
		echo '-------------------------------------------<br>';
		$statistic[$num] = $top5;
		$query->close();
	}
	echo var_dump($statistic);
}
catch (Exception $e) {
		// print exception
		print $e->getMessage();
}

?>