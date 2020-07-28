<?php		

	$rootDir = __DIR__;

	$inboxPath = $rootDir . "/../images";
	$destinationPath = $rootDir . "/../labeled/" . $_GET["destination"];

	$imageName= $_GET["image"];
	
	rename($inboxPath . "/" . $imageName, $destinationPath . "/" . $imageName);
		
	header("Location: .");

?>
       
