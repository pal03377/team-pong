<script>
    import { _ } from "svelte-i18n";
    import Client from "./Client.svelte";

    // https://stackoverflow.com/a/901144/4306257
	const params = new Proxy(new URLSearchParams(window.location.search), {
		get: (searchParams, prop) => searchParams.get(prop),
	});
    let myTeam = params.team || localStorage.getItem("team");
    if (myTeam) {
        localStorage.setItem("team", myTeam);
    }

    async function fetchMyTeam() {
        // get preferred random team
        const response = await fetch('/weakest_teams');
        const teams = await response.json(); 
        myTeam = teams[Math.floor(Math.random() * teams.length)];
        localStorage.setItem("team", myTeam);
    }

    if (!myTeam) {
        // there should be a 80% chance that the user will be from the currently weaker team
        // this is to prevent the user from always being on the same team
        if (Math.random() < 0.8) {
            fetchMyTeam();
        } else {
            myTeam = ["A", "B"][Math.floor(Math.random() * 2)];
            localStorage.setItem("team", myTeam);
        }
    }
</script>


{#if myTeam}
    <Client {myTeam} />
{:else}
    { $_("client.decidingOnTeam") }
{/if}