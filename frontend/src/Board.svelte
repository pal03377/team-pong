<script>

	import { onMount } from "svelte";
	import { _ } from "svelte-i18n";
	import io from "socket.io-client";
	import confetti from "canvas-confetti";

	import TeamView from "./TeamView.svelte";
	import Platform from "./Platform.svelte";
	import Ball from "./Ball.svelte";
    import Countdown from "./Countdown.svelte";

	import { yScale } from "./scale.js";
	import { boardConfig, listenForConfigChange } from "./boardConfig.js";

	let BACKEND_URL = "";
	
	const socket = io.connect(BACKEND_URL, {
		reconnect: true, 
        upgrade: false, 
		query: {}
	});
	listenForConfigChange(socket);

	onMount(async () => {
		socket.emit("join_board");
	});

	$: console.log($_("board.developmentCredits"));
	$: console.log($boardConfig)

	let teams = [];
	socket.on("teams", data => teams = data);
	let balls = [];
	socket.on("balls", data => balls = data);
	let countdown = -1;
	socket.on("countdown", data => countdown = data);

	const teamAcolors = ["#0052d4", "#4364f7", "#6fb1fc"];
	const teamBcolors = ["#ffe259", "#ffa751"];
	const tada = new Audio("/static/audio/tada.wav");
	function onWin(team) {
		confetti({
			angle: 270,
			particleCount: 100,
			spread: 180,
			origin: { x: 0.5, y: -0.2 },
			colors: team === "A" ? teamAcolors : teamBcolors,
			scalar: 2,
		});
		tada.play();
	}
	socket.on("win", onWin);

	let topText = "";
	let topTextUnchanged = true;
	$: if (topTextUnchanged) {
		topText = $_("board.participate", { values: { host: location.host } });
	}
	let bottomText = "";
	let bottomTextUnchanged = true;
	$: if (bottomTextUnchanged) {
		bottomText = $_("board.developmentCredits");
	}

	const blop0 = new Audio("/static/audio/blop1.wav");
	const blop1 = new Audio("/static/audio/blop2.wav");
	let lastBlop = 0;
	let lastBlopTime = Date.now();
    function playBlop() {
        if (Date.now() - lastBlopTime < 100) return;
		lastBlopTime = Date.now();
		if (lastBlop === 0) {
			blop1.play();
			lastBlop = 1;
		} else {
			blop0.play();
			lastBlop = 0;
		}
		// sometimes just flip randomly
		if (Math.random() < 0.2) lastBlop = 1 - lastBlop;
        lastBlopTime = Date.now();
    }
	socket.on("blop", () => setTimeout(playBlop, 200));

	let main;
	function goIntoFullscreen() {
		if (main.requestFullscreen) {
			main.requestFullscreen({ navigationUI: "hide" });
		} else if (main.mozRequestFullScreen) { /* Firefox */
			main.mozRequestFullScreen({ navigationUI: "hide" });
		} else if (main.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
			main.webkitRequestFullscreen({ navigationUI: "hide" });
		}
	}

</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<main bind:this={ main } on:click={ goIntoFullscreen }>

	<input class="infoText top" bind:value={topText} on:input={() => topTextUnchanged = false} />
	<input class="infoText bottom" bind:value={bottomText} on:input={() => bottomTextUnchanged = false} />

	<div class="yBorder" style="transform: translateY({yScale * 21.5}vh)"></div>
	<div class="yBorder" style="transform: translateY({-yScale * 21.5}vh)"></div>

	<div id="bottomLeft">
		<TeamView team={teams[0]} neededParticipants={ $boardConfig["min_player_number_per_team"] } />
	</div>
	<div id="bottomRight">
		<TeamView team={teams[1]} neededParticipants={ $boardConfig["min_player_number_per_team"] } />
	</div>

	{#each balls as ball}
		<Ball {ball} />
	{/each}

	{#each teams as team}
		<Platform {team} platformHeight={ $boardConfig["platform_height"] ?? 1 } />
	{/each}

	<Countdown {countdown} />

</main>


<style>

@font-face {
	font-family: "Montserrat";
	src: url("/static/fonts/Montserrat-VariableFont_wght.ttf") format("truetype");
	font-weight: normal;
	font-style: normal;
}

@font-face {
	font-family: "Montserrat";
	src: url("/static/fonts/Montserrat-VariableFont_wght.ttf") format("truetype");
	font-weight: 700;
	font-style: normal;
}

main {
	width: 100%;
	height: 100%;
	display: flex;
	background-color: black;
	color: white;
	font-family: Montserrat, sans-serif;
}

:global(main input) {
	font-family: Montserrat, sans-serif;
}

.infoText {
	position: absolute;
	width: 100%;
	font-size: 2.5vh;
	text-align: center;
	border: none;
	background-color: transparent;
	color: white;
	outline: none;
}

.infoText.top {
	top: 2vh;
	font-weight: semibold;
}

.infoText.bottom {
	bottom: 2vh;
}

.yBorder {
	position: absolute;
	top: 50vh;
	left: 0;
	right: 0;
	margin: 0 auto;
	width: 70%;
	height: 1px;
	background: radial-gradient(ellipse at center, rgba(255,255,255,0) 0%,rgba(255,255,255,1) 50%,rgba(255,255,255,0) 100%);
}

#bottomLeft {
	position: absolute;
	bottom: 0;
	left: 0;
}

#bottomRight {
	position: absolute;
	bottom: 0;
	right: 0;
}

</style>
