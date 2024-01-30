<?php
if($_SERVER['REQUEST_METHOD'] === 'POST'){
$result = $_POST;
/*
array(
    "Warwolf" => "BacT",
    "Jacqueline of Hainaut" => "TaToH",
    "Admiral Yi Sun-Shin" => "TheMax",
    "Master of the Templar" => "Liereyy",
    "Harald Hardraade" => "F1Re",
    "Sundjata" => "Villese",
    "Pope Leo I" => "TheViper",
    "Gonzalo Pizarro" => "Hera",
    "King Bela IV" => "Nicov",
    "Ivaylo" => "ACCM",
    "Cobra Car" => "DauT",
    "Edward Longshanks" => "Vivi",
    "Le Loi" => "Yo",
    "John the Fearless" => "MbL",
    "Philip the Good" => "Antagonist",
    "Little John" => "dogao"
);*/

$correct_guesses = array(
    "Warwolf" => 0,
    "Jacqueline of Hainaut" => 0,
    "Admiral Yi Sun-Shin" => 0,
    "Master of the Templar" => 0,
    "Harald Hardraade" => 0,
    "Sundjata" => 0,
    "Pope Leo I" => 0,
    "Gonzalo Pizarro" => 0,
    "King Bela IV" => 0,
    "Ivaylo" => 0,
    "Cobra Car" => 0,
    "Edward Longshanks" => 0,
    "Le Loi" => 0,
    "John the Fearless" => 0,
    "Philip the Good" => 0,
    "Little John" => 0
);

$all_guesses = array(
    "Warwolf" => array(),
    "Jacqueline of Hainaut" => array(),
    "Admiral Yi Sun-Shin" => array(),
    "Master of the Templar" => array(),
    "Harald Hardraade" => array(),
    "Sundjata" => array(),
    "Pope Leo I" => array(),
    "Gonzalo Pizarro" => array(),
    "King Bela IV" => array(),
    "Ivaylo" => array(),
    "Cobra Car" => array(),
    "Edward Longshanks" => array(),
    "Le Loi" => array(),
    "John the Fearless" => array(),
    "Philip the Good" => array(),
    "Little John" => array()
);

$scores = array(
	16 => array(),
	15 => array(),
	14 => array(),
	13 => array(),
	12 => array(),
	11 => array(),
	10 => array(),
	8 => array(),
	7 => array(),
	6 => array(),
	9 => array(),
	5 => array(),
	4 => array(),
	3 => array(),
	2 => array(),
	1 => array(),
	0 => array(),
);

$dir = new DirectoryIterator(dirname(__FILE__).'/data');
$entries = 0;
foreach ($dir as $fileinfo) {
    if (!$fileinfo->isDot()) {
        $data = json_decode(file_get_contents($fileinfo->getPathname()));
        $score = 0;
		foreach($result as $hero => $value){
			$hero_s = $hero;
			$hero = str_replace('_', ' ', $hero);
			if($result[$hero_s] === $data->guess->{$hero}){
				$score++;
				$correct_guesses[$hero]++;
			}
			if(!isset($all_guesses[$hero][$data->guess->{$hero}])){
				$all_guesses[$hero][$data->guess->{$hero}] = 0;
			}
			$all_guesses[$hero][$data->guess->{$hero}]++;
		}
		$scores[$score][] = array("emailAddress"=>$data->emailAddress,"twitchUsername"=>$data->twitchUsername);
		$entries++;
    }
}
}
?>
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>Guessing competition result</title>
<style>
body {
	font-family: sans-serif;
}
.bold {
	font-weight: bold;
}
.number {
	text-align: right;
	font-weight: bold;
}
</style>
</head>
<body>
<h1>HC4 guessing competition result</h1>


<?php if($_SERVER['REQUEST_METHOD'] === 'POST'){ ?>

<div style="background-color: #ccc; padding: 1rem;">
<h2>Your submitted configuration</h2>
<table>
<tbody>
<?php 
foreach($result as $hero => $value){
	$hero = str_replace('_', ' ', $hero);
	echo "<tr><td><b>$hero</b></td><td>is</td><td><b>$value</b></td></tr>";
}
?>
</tbody>
</table>
</div>


<h2>Most frequent guesses</h2>

<table>
<tbody>
<?php 
foreach($all_guesses as $hero => $value){
	arsort($value);
	$first = array_keys($value)[0];
	$percent = number_format($value[$first] / $entries * 100, 1);
	echo "<tr><td class='bold'>$hero</td><td>was guessed to be</td><td class='bold'>$first</td><td>by <b>{$value[$first]}</b> people (<b>$percent %</b>)</td></tr>";
}
?>
</tbody>
</table>


<h2>Number of correct guesses</h2>
<p>Given is the number of people that had X correct guesses</p>

<table>
<tbody>
<?php
foreach($scores as $key => $value){
	$count = count($value);
	echo "<tr><td class='number'>$count</td><td>people guessed</td><td class='number'>$key</td><td>players correctly</td></tr>";
        if($key == 16){
            echo "<tr><td colspan='4'>";
            foreach($value as $user){
                echo htmlspecialchars($user["twitchUsername"]) . " | ";
            }
            echo "</td></tr>";
        }
}
?>
</tbody>
</table>

<?php } else { ?>

<form method="post">
<div id="selects"></div>
<input type="submit" value="query"/>
</form>

<script>
    const heroes = [
        "Warwolf",
        "Jacqueline of Hainaut",
        "Admiral Yi Sun-Shin",
        "Master of the Templar",
        "Harald Hardraade",
        "Sundjata",
        "Pope Leo I",
        "Gonzalo Pizarro",
        "King Bela IV",
        "Ivaylo",
        "Cobra Car",
        "Edward Longshanks",
        "Le Loi",
        "John the Fearless",
        "Philip the Good",
        "Little John",
    ];
    const players = [
        "DauT",
        "dogao",
        "Hera",
        "Liereyy",
        "MbL40C",
        "Mr_Yo",
        "TaToH",
        "TheViper",
        "ACCM",
        "BacT",
        "Barles",
        "JorDan",
        "Nicov",
        "Villese",
        "Vinchester",
        "Vivi",
    ];
    let selects = '<table><thead><tr><th>Hero</th><th>Player</th></thead><tbody>';
    for(let hero of heroes){
		let select = `<tr><td>${hero}</td><td><select name="${hero}">`;
		for(let player of players){
			select += `<option value="${player}">${player}</option>`;
		}
		select += '</select></td></tr>';
		selects += select;
    }
    selects += '</tbody></table>'
	document.getElementById('selects').innerHTML = selects;
</script>

<?php } ?>

</body>
</html>

