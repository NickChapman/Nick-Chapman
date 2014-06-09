<?php

require "keyGen.php";

function validateEntry($username, $validChars){
	$nameArray = str_split($username);
	$valid = true;
	foreach($nameArray as $nameChar){
		$nameChar = (string)$nameChar;
		if(!in_array($nameChar, $validChars, true)){
			$valid = false;
		}
	}
	return $valid;
}


function db_connect(){
	//Returns the database connection or false if something went wrong
	$db = new MySQLi('localhost', 'YOUR USERNAME', 'YOUR PASSWORD', 'YOUR DATABASE');
	if($db->connect_errno > 0){
		/* Enable the next line if you would like email notifications of connection failures
		mail("YOUR EMAIL", "Server Status", $db->sqlstate);
		*/
		$err = json_encode(array("status" => "server"));
		echo $err;
		return false;
	}
	else{
		return $db;
	}
}

//Grab things out of POST
$email1 = strtolower(trim($_POST['email1']));
$email2 = strtolower(trim($_POST['email2']));
$pass1 = $_POST['pass1'];
$pass2 = $_POST['pass2'];
$process = $_POST["process"];

//REGISTER A NEW USER
//To initiate the registration process the approriate trigger variables must be set
if(isset($email1) && isset($email2) && isset($pass1) && isset($pass2) && $process == "register"){	
	//establish a database connection
	$db = db_connect();
	if(!$db){
		return;	
	}
	//Escape all input for security
	$email1 = $db->real_escape_string($email1);
	$email2 = $db->real_escape_string($email2);
	$pass1 = $db->real_escape_string($pass1);
	$pass2 = $db->real_escape_string($pass2);
	
	if($email1 != $email2){
		$err = json_encode(array("status" => "email"));
		echo $err;
		return;
	}
	if($pass1 != $pass2){
		$err = json_encode(array("status" => "password"));
		echo $err;
		return;
	}
	
	//Password is suspiciously long
	if(strlen($pass1) > 100 || strlen($pass1) < 7){
		$err = json_encode(array("status" => "password"));
		echo $err;
		return;
	}
	
	//Generating validation data
	$validChars = array_merge(range(A, Z), range(a, z));
	$moreChars = array(1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "_", "-", " ", ".", "+", "@");
	$validChars = array_merge($validChars, $moreChars);
	//The loop casts each character in the valid chars list to a string
	foreach($validChars as $key => $ch){
		$validChars[$key] = (string)$ch;
	}
	//Check their email
	if(!validateEntry($email1, $validChars)){
		$err = json_encode(array("status" => "email"));
		echo $err;
		return;
	}
	$emailExt = explode("@", $email1);
	if($emailExt[1] != "###SELECTIVE EMAIL###"){
		$err = $json_encode(array("status" => "email"));
		echo $err;
		return;
	}
	$qry = $db->query("SELECT * FROM users WHERE user='".$emailExt[0]."'");
	if($qry->num_rows > 0){
		$err = json_encode(array("status" => "taken"));
		echo $err;
		return;
	}
	//Prepare the password for storage
	$passhash = password_hash($pass1, PASSWORD_DEFAULT);
	
	if(!$passhash){
		$err = json_encode(array("status" => "password"));
		echo $err;
		return;
	}

	$confirmKeyHash = gen_confirm_key_hash();
	
	//Register a user
	if($stmt = $db->prepare("INSERT INTO users (user, pass, confirmKey, confirmed, login_attempts) VALUES (?, ?, ?, ?, ?)")){
		$confirmed = 0;
		$login_attempts = 0;
		$stmt->bind_param("sssii", $emailExt[0], $passhash, $confirmKeyHash, $confirmed, $login_attempts);
		$stmt->execute();
		//After executing, now check to see that it exists
		$qry = $db->query("SELECT * FROM users WHERE user='".$emailExt[0]."'");
		if($qry->num_rows == 0){
			$err = json_encode(array("status" => "server"));
			echo $err;
			return;
		}
		else{
			$headers = "From: accounts@###YOURWEBSITE.COM###";
			mail(stripslashes($email1), "###YOUR SERVICE### Account Confirmation", "To confirm your ###YOUR SERVICE### account please go to the following link: http://###YOURSITE.COM###/confirm.php?user=".$emailExt[0]."&confirmKey=".$confirmKeyHash."&process=signupConfirm", $headers);
			$err = json_encode(array("status" => "registered"));
			echo $err;
			return;
		}
	}
}

//LOGIN AN EXISTING USER
if(isset($email1) && isset($pass1) && $process == "login"){
	//establish database connection
	$db = db_connect();
	if(!$db){
		return;
	}
	//split email to get the username
	$username = explode("@", $email1);
	$username = $username[0];
	//real_escape_string the username and password
	$username = $db->real_escape_string($username);
	$password = $db->real_escape_string($pass1);
	//check for username
	$qry = $db->query("SELECT * FROM users WHERE user='".$username."'");
	if($qry->num_rows!=1){
		$err = json_encode(array("status" => "username"));	
		echo $err;
		return;
	}
	$qry = $qry->fetch_assoc();
	//check to make sure the account is confirmed
	if($qry["confirmed"] != 1){
		$err = json_encode(array("status" => "confirm account"));
		echo $err;
		return;	
	}
	//check to make sure that the number of login attempts is fewer than 10
	if($qry["login_attempts"] > 10){
		//if they have logged in too many times send them a reset email
		$err = json_encode(array("status" => "login overflow"));
		echo $err;
		$headers = "From: accounts@###YOURSITE.COM###";
		mail($username."@###LIMITED EXTENSIONS###", "###YOUR SERVICE### Account Reset", "Someone has attempted to login to your account ten times in a row with the wrong password. We encourage you to change your password. Go here to reactivate your account: http://###YOURSITE.COM###/confirm.php?user=".$username."&confirmKey=".$qry["confirmKey"]."&process=reactivate", $headers);
		return;
	}
	//password_verify the password
	if(password_verify($pass1, $qry["pass"])){
		//if the password is right sign them in
		session_start();
		$_SESSION["user"] = $username;
		$_SESSION["startTime"] = time();
		//set login attempts back to 0
		$db->query("UPDATE users SET login_attempts='0' WHERE user='".$username."'");
		$err = json_encode(array("status" => "signed in"));
		echo $err;
		return;
	}
	else{
		//Increase the login attempts counter by 1
		$login_attempts = $qry["login_attempts"] + 1;
		$db->query("UPDATE users SET login_attempts='".$login_attempts."' WHERE user='".$username."'");
		$err = json_encode(array("status" => "password"));
		echo $err;
		return;
	}
}

//Logging people out
	//TODO
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	$_SESSION = array();
	session_destroy();
	$err = json_encode(array("status" => "logged out"));
	echo $err;
	return;
}


