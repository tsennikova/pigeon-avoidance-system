<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="/docs/4.0/assets/img/favicons/favicon.ico">

    <title>Pigeon Tinder</title>

    <!-- Bootstrap core CSS -->
    <link href="assets/css/bootstrap.min.css" rel="stylesheet">

  </head>

	<?php
		$relativePath = "/../images/";
		$inboxPath = __DIR__ . $relativePath;

		$allFiles = array_diff(scandir($inboxPath ), [".", ".."]); // Use array_diff to remove both period values eg: ("." , "..")

		if(sizeof($allFiles)==0){
			echo "<h1>No pigeon to tinder!</h1>";
			exit(0);
		}
		$imageName= $allFiles[2];
		$imagePath = $relativePath . $imageName;
		$matches = array();
		preg_match('/_(.*)\.jpg/',$imageName,$matches);

       
    ?> 

  <body class="bg-light">

    <div class="container" >
      <div class="text-center" >
	<!-- Image -->
        <img src="<?php echo $imagePath; ?>" class = "img-fluid" style="height: 260px;" alt="" title=""/>
     
		</br>
		</br>
	<h4>Really <?php echo ucfirst(array_pop($matches)); ?>?</h4>

    <div class="container" >
<div class="row">
		<button onclick="window.location.href='move.php?destination=pigeons&image=<?php echo $imageName; ?>';" class="btn btn-secondary btn-lg btn-block">
			Pigeon
		</button>
	
		<button onclick="window.location.href='move.php?destination=humans&image=<?php echo $imageName; ?>';" class="btn btn-secondary btn-lg btn-block">
			Human
		</button>
	
		<button onclick="window.location.href='move.php?destination=nothing&image=<?php echo $imageName; ?>';" class="btn btn-secondary btn-lg btn-block">
			Nothing
		</button>
		
		<button onclick="window.location.href='move.php?destination=trash&image=<?php echo $imageName; ?>';" class="btn btn-secondary btn-lg btn-block">
			Delete
		</button>
</div>
	  </div>
	  </div>
	</div>
    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="assets/js/bootstrap.min.js"></script>

  </body>
</html>
