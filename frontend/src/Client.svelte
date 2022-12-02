<script>

	import { onMount } from "svelte";
	import { _ } from "svelte-i18n";
	import io from "socket.io-client";
	import confetti from "canvas-confetti";
    import HelpDialog from "./HelpDialog.svelte";
    import { boardConfig, listenForConfigChange } from "./boardConfig";

	export let myTeam;
	let BACKEND_URL = "";
	
	const socket = io.connect(BACKEND_URL, {
		reconnect: true, 
        upgrade: false,  
		query: {}
	});
	listenForConfigChange(socket);

	let inactive = false;

	function join() {
		if (inactive) return;
		socket.emit("join", myTeam);
	}
	onMount(join);
	socket.on("rejoin_request", join);

	function reactivate() {
		inactive = false;
		join();
	}
	let inactivityTimer;
	function resetInactivityTimer() {
		if (inactive) {
			reactivate();
		}
		clearTimeout(inactivityTimer);
		inactivityTimer = setTimeout(() => inactive = true, 60000);
	}
	resetInactivityTimer();

	let disabled = false;
	function up() {
		if (disabled) return;
		resetInactivityTimer();
		disabled = true;
		socket.emit("up", myTeam);
		setTimeout(() => disabled = false, $boardConfig["tap_cooldown"]);
	}
	function down() {
		if (disabled) return;
		resetInactivityTimer();
		disabled = true;
		socket.emit("down", myTeam);
		setTimeout(() => disabled = false, $boardConfig["tap_cooldown"]);
	}

	const teamAcolors = ["#0052d4", "#4364f7", "#6fb1fc"];
	const teamBcolors = ["#ffe259", "#ffa751"];
	function onWin(team) {
		if (team === myTeam) {
			confetti({
				angle: 270,
				particleCount: 100,
				spread: 180,
				origin: { x: 0.5, y: -0.2 },
				colors: team === "A" ? teamAcolors : teamBcolors,
				scalar: 2,
			});
			navigator.vibrate(200);
		} else {
			navigator.vibrate([100, 100]);
		}
	}
	socket.on("win", onWin);

	let helpOpen = false;

</script>

<main>

	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<h1 on:click={resetInactivityTimer} class:aTeam={myTeam === "A"} class:bTeam={myTeam === "B"}>
		{ $_("board.team.name", { values: { name: myTeam } }) }
		{#if inactive}
			(inaktiv)
		{/if}
	</h1>
	<button class="help" on:click={ () => helpOpen = !helpOpen }>?</button>

	<button class="up" on:click={up} disabled={disabled}>
		<img class="arrow" src="img/arrow-up.svg" alt="Up" />
	</button>
	<button class="down" on:click={down} disabled={disabled}>
		<img class="arrow" src="img/arrow-down.svg" alt="Down" />
	</button>

	<disabled-countdown class:disabled style="--timeout: {$boardConfig["tap_cooldown"]}ms">
	</disabled-countdown>

	<HelpDialog bind:open={helpOpen} />

</main>


<style>

main {
	width: 100%;
	height: 100%;
}

h1 {
	display: block;
	width: 100%;
	text-align: center;
	color: white;
	margin: 0;
	padding: 12px 0;
	user-select: none;
}

.aTeam {
	background: linear-gradient(32deg, #0052d4, #4364f7, #6fb1fc);
}

.bTeam {
	background: linear-gradient(32deg, #ffe259, #ffa751);
}

button {
	width: 100%;
	height: calc(50% - 12px);
	font-size: 100px;
	background-color: black;
	transition: background-color 300ms;
}

button:disabled {
	background: #777;
}

.arrow {
	height: 60%;
	box-sizing: border-box;
	pointer-events: none;
}

disabled-countdown {
	position: fixed;
	width: 100%;
	height: 24px;
	left: 0;
	bottom: 0;
  	background: linear-gradient(to right, #00c9ff, #92fe9d);
	box-shadow: 0 0 10px #00c9ff;
	transform: scaleX(100%);
	transition-duration: 0ms;
	transition-timing-function: linear;
}

disabled-countdown.disabled {
	transform: scaleX(0);
	transition-duration: var(--timeout);
}

.help {
	position: fixed;
	top: 4px;
	right: 0;
	width: 50px;
	height: 50px;
	font-size: 30px;
	border-radius: 50%;
	border: none;
	background-color: black;
	color: white;
}

</style>
