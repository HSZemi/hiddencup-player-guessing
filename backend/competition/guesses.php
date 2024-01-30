<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Origin, Content-Type, X-Auth-Token');
if (isset($_GET['id']) && preg_match("/[0-9a-f]{64}/", $_GET['id']) === 1) {
	$filepath = './guesses/'.$_GET['id'].'.json';
	if(file_exists($filepath)){
		echo file_get_contents($filepath);
	} else {
		http_response_code(404);
		echo '404';
	}
} else {
		http_response_code(403);
		echo '403';
}
