<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Origin, Content-Type, X-Auth-Token');
// Remove the // from the next two lines to close the voting.
//echo '{"success":true, "message":"Sadly, voting has closed already. Have fun during the reveal!"}';
//die();
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	$filename = 'data/' . bin2hex(random_bytes(16)) . '-' . time() . '.json';
	if(FALSE === file_put_contents($filename, file_get_contents('php://input'))){
		echo '{"success":false, "message":"An error occured. Please try again after a few seconds."}';
	} else {
		echo '{"success":true, "message":"Your guess has been saved successfully! You can close this window now."}';
	}
}
