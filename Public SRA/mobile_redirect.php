<?php
    // Get the user agent
$user_agent = $_SERVER['HTTP_USER_AGENT'];

// Create an array of known mobile user agents
// Most mobile devices send a pretty standard string that can be covered by
// one of these.  I believe I have found all the agents (as of the date above)
// that do not and have included them below.  If you use this function, you 
// should periodically check your list against the WURFL file, available at:
// http://wurfl.sourceforge.net/


$mobile_agents = Array(
    "240x320", "acer", "acoon", "acs-", "abacho", "ahong", "airness", "alcatel", "amoi",     "android", "anywhereyougo.com", "applewebkit/525", "applewebkit/532", "asus", "audio", "au-mic", "avantogo", "becker", "benq", "bilbo", "bird", "blackberry", "blazer", "bleu", "cdm-", "compal", "coolpad", "danger", "dbtel", "dopod", "elaine", "eric", "etouch", "fly " , "fly_", "fly-", "go.web", "goodaccess", "gradiente", "grundig", "haier", "hedy", "hitachi", "htc", "huawei", "hutchison", "inno", "ipad", "ipaq", "iPhone", "ipod", "jbrowser", "kddi", "kgt", "kwc", "lenovo", "lg ", "lg2", "lg3", "lg4", "lg5", "lg7", "lg8", "lg9", "lg-", "lge-", "lge9", "longcos", "maemo", "mercator", "meridian", "micromax", "midp", "mini", "mitsu", "mmm", "mmp", "mobi", "mot-", "moto", "nec-", "netfront", "newgen", "nexian", "nf-browser", "nintendo", "nitro", "nokia", "nook", "novarra", "obigo", "palm", "panasonic", "pantech", "philips", "phone", "pg-", "playstation", "pocket", "pt-", "qc-", "qtek", "rover", "sagem", "sama", "samu", "sanyo", "samsung", "sch-", "scooter", "sec-", "sendo", "sgh-", "sharp", "siemens", "sie-", "softbank", "sony", "spice", "sprint", "spv", "symbian", "tablet", "talkabout", "tcl-", "teleca", "telit", "tianyu", "tim-", "toshiba", "tsm", "up.browser", "utec", "utstar", "verykool", "virgin", "vk-", "voda", "voxtel", "vx", "wap", "wellco", "wig browser", "wii", "windows ce", "wireless", "xda", "xde", "zte"
);

// Pre-set $is_mobile to false.

$is_mobile = false;

// Cycle through the list in $mobile_agents to see if any of them
// appear in $user_agent.

foreach ($mobile_agents as $device) {

    // Check each element in $mobile_agents to see if it appears in
    // $user_agent.  If it does, set $is_mobile to true.

    if (stristr($user_agent, $device)) {

        $is_mobile = true;

        // break out of the foreach, we don't need to test
        // any more once we get a true value.

        break;
    }
}
//check whether mobile is true, and if so, redirect to mobile page
if(!$is_mobile){
    header("Location: https://www.facebook.com/drbrandtskincare/app_183671798471240");
	//https://www.facebook.com/srayerassociates?v=app_183671798471240&app_data=gaReferrerOverride%3Dhttp%253A%252F%252Fwww.shortstackapp.com%252Fmember%252Fworking_tabs%252F2505491 <-- Faecbook link to S Rayer location
	//replace domain
    exit;
}
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Dr Brandt Mobile Sweepstakes App</title>

<style type="text/css">
body{
	background-color:black;	
	max-width:360px;
	overflow-x:hidden;
}
html {	
	
}
#frame {
	margin-left:auto;
	margin-right:auto;	
}
</style>


<meta name="viewport" content="">
</head>
<body>

<iframe id = 'frame' src="http://a.pgtb.me/0fdkLC?embed=1" width="318" height="355" scrolling="no" frameborder="0"></iframe>

<script type="text/javascript">
function direct(){
		var res = screen.width;
		var zoom = res/350;
		//if (res < 500){
			document.getElementsByName('viewport').item(0).setAttribute('content', "width=device-width, minimum-scale =" +zoom+ ", initial-scale =" + zoom);
		//}
		/*if(499 < res < 1000){
			document.getElementsByName('viewport').item(0).setAttribute('content', 'width=device-width, initial-scale = 1.7');	
		}
		if(999 < res){
			document.getElementsByName('viewport').item(0).setAttribute('content', 'width=device-width, initial-scale = 2');	
		}*/
}
direct();
document.ontouchmove = function(event) {
	event.preventDefault();
	window.scrollTo(0,0);	
}

</script>
</body>
</html>
