<script>

    import { _ } from "svelte-i18n";
	import io from "socket.io-client";
    import { boardConfig, listenForConfigChange, updateConfig } from "./boardConfig";
    import { LANGUAGE_NAMES } from "./translations/translationInit.js";

	let BACKEND_URL = "";
	const socket = io.connect(BACKEND_URL, {
		reconnect: true, 
        upgrade: false,  
		query: {}
	});
    listenForConfigChange(socket);

    async function reset() {
        await fetch("/reset", {
            method: "POST"
        });
        alert("Zurückgesetzt.");
    }

</script>

<main>

	<h1>{ $_("config.title") }</h1>

    <section>
        <label for="language">{ $_("config.language.title") }</label>
        <select bind:value={ $boardConfig.language } id="language" on:change={ () => updateConfig() }>
            {#each Object.keys(LANGUAGE_NAMES) as languageCode}
                <option value={ languageCode }>{ LANGUAGE_NAMES[languageCode] }</option>
            {/each}
        </select>
    </section>

    <section>
        <label for="resetButton">{ $_("config.reset.title") }</label>
        <p>{ $_("config.reset.description") }</p>
        <button id="resetButton" on:click={() => reset()}>
            { $_("config.reset.action") }
        </button>
    </section>

    <section class="note">
        <p>{ $_("config.note") }</p>
    </section>

    <section>
        <label for="minPlayerNumberPerTeam">
            { $_("config.minPlayerNumberPerTeam.title") }
        </label>
        <p>{ $_("config.minPlayerNumberPerTeam.description") }</p>
        <input
            type="number" id="minPlayerNumberPerTeam"
            bind:value={ $boardConfig.min_player_number_per_team }
            min=0
            on:input={ () => updateConfig() }
        />
    </section>

    <section>
        <label for="platformHeight">
            { $_("config.platformHeight.title") }
        </label>
        <p>{ $_("config.platformHeight.description") }</p>
        <input
            type="range" id="platformHeight"
            bind:value={ $boardConfig.platform_height }
            min=1 max=50
            on:input={ () => updateConfig() }
        />
    </section>

    <section>
        <label for="platformMovementSpeed">
            { $_("config.platformMovementSpeed.title") }
        </label>
        <p>
            { $_("config.platformMovementSpeed.description", { values: { current: $boardConfig.platform_movement_speed, default: 1.2 } }) }
        </p>
        <input
            type="range" id="platformMovementSpeed"
            bind:value={ $boardConfig.platform_movement_speed }
            min={0.1} max={10.0} step={0.1}
            on:input={ () => updateConfig() }
        />
    </section>

    <section>
        <label for="tapCoolDown">
            { $_("config.tapCoolDown.title") }
        </label>
        <p>
            { $_("config.tapCoolDown.description", { values: { default: 1500 } }) }
        </p>
        <input
            type="number" id="tapCoolDown"
            bind:value={ $boardConfig.tap_cooldown }
            min=0 max=20000 step=1
            on:input={ () => updateConfig() }
        />
    </section>

    <section>
        <label for="numberOfBalls">
            { $_("config.numberOfBalls.title") }
        </label>
        <p>{ $_("config.numberOfBalls.description") }</p>
        <input
            type="number" id="numberOfBalls"
            bind:value={ $boardConfig.number_of_balls }
            min=1 max=100 step=1
            on:input={ () => updateConfig() }
        />
    </section>

    <section>
        <label for="ballSpeedFactor">
            { $_("config.ballSpeedFactor.title") }
        </label>
        <p>
            { $_("config.ballSpeedFactor.description", { values: { current: $boardConfig.ball_speed_factor, default: 1.2 } }) }
        </p>
        <input
            type="range" id="ballSpeedFactor"
            bind:value={ $boardConfig.ball_speed_factor }
            min={0.1} max={5.5} step={0.1}
            on:input={ () => updateConfig() }
        />
    </section>

    <section>
        <label for="maxBallSpeedFactor">
            { $_("config.maxBallSpeedFactor.title") }
        </label>
        <p>
            { $_("config.maxBallSpeedFactor.description", { values: { current: $boardConfig.max_ball_speed_factor, default: 2.8 } }) }
        </p>
        <input
            type="range" id="maxBallSpeedFactor"
            bind:value={ $boardConfig.max_ball_speed_factor }
            min={0.1} max={5.5} step={0.1}
            on:input={ () => updateConfig() }
        />
    </section>

    <section>
        <label for="countdown">
            { $_("config.countdown.title") }
        </label>
        <p>
            { $_("config.countdown.description") }
        </p>
        <input
            type="number" id="countdown"
            bind:value={ $boardConfig.countdown }
            min=1 step=1
            on:input={ () => updateConfig() }
        />
    </section>

    <section>
        <label for="blopSoundEnabled">
            { $_("config.blopSoundEnabled.title") }
        </label>
        <p>
            { $_("config.blopSoundEnabled.description") }
        </p>
        <input
            type="checkbox" id="blopSoundEnabled"
            checked={ $boardConfig.blop_sound_enabled }
            on:input={ evt => {
                $boardConfig = {
                    ...$boardConfig,
                    blop_sound_enabled: evt.target.checked
                };
                updateConfig();
            }}
        />
    </section>

</main>


<style>

main {
	width: 100%;
	height: 100%;
    background-color: black;
    color: white;
    max-height: 100vh;
    overflow-y: auto;
    padding: 48px 0;
    box-sizing: border-box;
}

h1 {
	display: block;
	width: 100%;
	text-align: center;
	margin: 0;
	padding: 12px 0;
	user-select: none;
}

section {
    display: block;
    max-width: 600px;
    padding: 24px;
    margin: 12px auto;
    box-sizing: border-box;
    border-radius: 12px;
    background-color: #333;
}

section.note {
    background-color: transparent;
    padding: 0;
    padding-top: 16px;
}

label {
    display: block;
    font-size: 1.2em;
    margin-bottom: 12px;
}

select {
    display: block;
    width: 100%;
    padding: 12px;
    margin: 12px 0;
    box-sizing: border-box;
    border-radius: 12px;
    border: 1px solid black;
    background-color: #333;
    color: white;
    font-size: 1.2em;
}

#resetButton {
    display: block;
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 12px;
    background-color: #f00;
    color: white;
    font-size: 1.2em;
    cursor: pointer;
}

input {
    display: block;
    width: 100%;
    padding: 12px;
    box-sizing: border-box;
    border-radius: 12px;
    border: 1px solid #AAA;
    background-color: #333;
    color: white;
}

</style>
