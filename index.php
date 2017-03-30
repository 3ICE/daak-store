<!DOCTYPE html>
<!-- http://clone-clicker.herokuapp.com/ -->
<html>
	<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<link rel="stylesheet" type="text/css" href="style.css">
	<title>DAAK's Clone Clicker</title>
	<script src="jquery-3.1.1.js"></script>
	<script>
	//3ICE: "onload"
	$(document).ready( function() {
		"use strict";

		//3ICE: These track the state of the game
		var helpers = 0;
		var equipment = [];
		var equipmentPool = ["A rock", "A shield", "A bigger sword", "A gun", "A rocket", "A death laser", "Nuke", "Nuke v2", "Nuke v3"] //3ICE: then Nuke v4, Nuke v5, ad infinitum
		var upgrades = 0;
		var points = 0;
		var gold = 100;
		var enemy_health = 100;//3ICE: Current vs:
		var max_health = 100; //3ICE: Maximum
		var enemy_level = 1;
		var helper_cost = 100;
		var equipment_cost = 100;
		var upgrade_cost = 100;

		$(".hid").css("display","none");

		$("#submit_score").click( function () {
			var msg = {
				"messageType": "SCORE",
				"score": points
			};
			window.parent.postMessage(msg, "*");
		});

		$("#save").click( function () {
			var msg = {
				"messageType": "SAVE",
				"gameState": {
					"helpers": helpers,
					"equipment": equipment,
					"upgrades": upgrades,
					"points": points,
					"gold": gold,
					"enemy_health": enemy_health,
					"max_health": max_health,
					"enemy_level": enemy_level,
					"helper_cost": helper_cost,
					"equipment_cost": equipment_cost,
					"upgrade_cost": upgrade_cost,
				}
			};
			window.parent.postMessage(msg, "*");
		});

		$("#load").click( function () {
			var msg = {
				"messageType": "LOAD_REQUEST",
			};
			window.parent.postMessage(msg, "*");
		});

		window.addEventListener("message", function(evt) {
			if(evt.data.messageType === "LOAD") {
				helpers = evt.data.gameState.helpers;
				equipment = evt.data.gameState.equipment;
				upgrades = evt.data.gameState.upgardes;
				points = evt.data.gameState.points;
				gold = evt.data.gameState.gold;
				enemy_health = evt.data.gameState.enemy_health;
				max_health = evt.data.gameState.max_health;
				enemy_level = evt.data.gameState.enemy_level;
				helper_cost = evt.data.gameState.helper_cost;
				equipment_cost = evt.data.gameState.equipment_cost;
				upgrade_cost = evt.data.gameState.upgrade_cost;
				update();
			} else if (evt.data.messageType === "ERROR") {
				alert(evt.data.info);
			}
		});

		$("#hire_helper").click( function () {
		if(helper_cost <= gold){
			helpers += 1;
			gold -= helper_cost;
			update();
			helper_cost += 100;
			$("#hire_helper").text("Hire Helper (" + helper_cost + " gold)")
		}
		else{
			alert("You need " + (helper_cost - gold) + " more gold!");
		}
	});

		$("#purchase_equipment").click( function () {
		if(equipment_cost <= gold){
			equipment.push(equipmentPool[equipment.length]);
			gold -= equipment_cost;
			update();
			equipment_cost += 100;
			if(equipment_cost<1000){
				$("#purchase_equipment").text("Purchase equipment (" + equipment_cost + " gold)")
			}else{
				$("#purchase_equipment").hide()//3ICE: No more equipment in the shop.
			}
		}
		else{
			alert("You need " + (equipment_cost - gold) + " more gold!");
		}
	});

		$("#upgrade").click( function () {
		if(upgrade_cost <= gold){
			upgrades += 1;
			gold -= upgrade_cost;
			update();
			upgrade_cost += 100;
			$("#upgrade").text("Purchase level " + (upgrades+1) + " Upgrade (" + upgrade_cost + " gold)")
		}
		else{
			alert("You need " + (upgrade_cost - gold) + " more gold!");
		}
	});

		var images = ["img/attack1.png", "img/attack2.png", "img/attack3.png", "img/attack4.png", "img/attack5.png", "img/attack6.png", "img/attack7.png", "img/attack8.png", "img/attack9.png"];
		var imageObject = document.getElementById("imageObject");
		var imageCounter = 1;
		$("#attack").click(function () {
			if(imageCounter > 8){imageCounter = 0;} // 3ICE: [9] resets to [0].
			imageObject.src = images[imageCounter++];
			var damage_done = 1 + upgrades + helpers + equipment.length;
			points += damage_done;
			enemy_health -= damage_done;
			if(enemy_health <= 0){
				max_health = 100 + enemy_level * 10;
				gold += 10 + enemy_level * 10;
				points += enemy_level * 100;
				enemy_health = max_health;
				enemy_level += 1;
				update()
			}else{
				//3ICE: Just a light update():
				$("#points").text(points);
				$("#health").width(enemy_health / max_health * 300);
				$("#health").text(enemy_health + " Hit Points");
			}
		});

		function update() {
			$("#gold").text(gold);
			$("#points").text(points);
			$("#helpers").text(helpers);
			$("#health").width(enemy_health / max_health * 300);
			$("#health").text(enemy_health + " Hit Points");
			$("#equipment").html("");
			for (var i = equipment.length - 1; i >= 0; i--) {
				$("#equipment").append("<li>" + equipment[i] + "</li>");
			}
		}

		var message =	{
			messageType: "SETTING",
			options: {
				"width": 640,
				"height": 480
				}
		};
		window.parent.postMessage(message, "*");

	});
	</script>
</head>
<body>

	<button id="attack">Attack</button><br />
	<button id="hire_helper">Hire Helper (100 gold)</button>
	<button id="purchase_equipment">Purchase equipment (100 gold)</button>
	<button id="upgrade">Purchase level 1 Upgrade (100 gold)</button>

	<h3>Equipment</h3>
	<ul id="equipment"></ul>

	<div><span id="points">0</span> Points</div>
	<div><span id="gold">100</span> Gold</div>
	<div><span id="helpers">0</span> Helpers</div>
	<div><span id="health" style="width: 300px;">100 Hit Points</span></div>

	<button id="submit_score">Submit score</button><br />
	<button id="save">Save</button>
	<button id="load">Load</button><br />
	<img src="img/attack1.png" id="imageObject" />
	<img src="img/attack2.png" class="hid" style="display: inline" />
	<img src="img/attack3.png" class="hid" style="display: inline" />
	<img src="img/attack4.png" class="hid" style="display: inline" />
	<img src="img/attack5.png" class="hid" style="display: inline" />
	<img src="img/attack6.png" class="hid" style="display: inline" />
	<img src="img/attack7.png" class="hid" style="display: inline" />
	<img src="img/attack8.png" class="hid" style="display: inline" />
	<img src="img/attack9.png" class="hid" style="display: inline" />

</body></html>