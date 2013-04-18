// http://api.jquery.com/category/ajax/
// http://stackoverflow.com/questions/1616724/jquery-using-ranges-in-switch-cases
var URL = "http://raspberrypi.cocoa/command";
function log(msg)
{
	var numlines = 20;
	var div = $("div#debug");
	var nl = "\n";
	var lines = div.text().split(nl);
	if (lines.length == 1 && lines[0] == "") {
		div.text(msg);
		return(msg);
	}
	lines.push(msg);
	var newmsg = lines.join(nl);
	lines = newmsg.split(nl);
	while (lines.length > numlines) {
		lines.shift();
	}
	newmsg = lines.join(nl);
	div.text(newmsg);
	return(newmsg);
}

function issue_command(code)
{
	var cmds = ["L", "F", "R", "B"];
	var cmd = cmds[code-37];
	log(cmd);
	jQuery.get(URL, cmd);
}

function keydown_handler(event)
{
	if (event.which>=37 && event.which <=40) {
		event.preventDefault();
		issue_command(event.which);
	}
}

function setup()
{
	$(document).keydown(keydown_handler);
}

$(document).ready(setup);
