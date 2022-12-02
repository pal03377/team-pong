<script>

    import { _ } from "svelte-i18n";

    export let team;
    export let neededParticipants;

</script>


{#if team}
    <team-view>
        {#key team.score}
            <span class="score" class:aTeam={ team.team === "A" } class:bTeam={ team.team === "B" }>
                { team.score ?? 0 }
            </span>
        {/key}
        <h1>{ $_("board.team.name", { values: { name: team.team }}) }</h1>
        <p class:moreNeeded={ team.count < neededParticipants }>
            {#if team.count >= neededParticipants}
                { $_("board.team.participantsCurrently", { values: { count: team.count } }) }
            {:else}
            { $_("board.team.notEnoughParticipants", { values: { count: team.count, needed: neededParticipants } }) }
            {/if}
        </p>
    </team-view>
{/if}


<style>

team-view {
    display: flex;
    flex-direction: column;
    min-width: 180px;
    margin: 12px 24px;
}

span, h1, p {
    text-align: center;
}

@keyframes highlight {
    from, to {
        transform: scale(1);
    }
    50% {
        transform: scale(1.5);
    }
}

.score {
    font-size: 72px;
    font-weight: bold;
    animation: highlight 400ms ease-out;
    animation-fill-mode: forwards;
}

h1 {
    margin: 0;
}

.aTeam {
    background: linear-gradient(32deg, #0052d4, #4364f7, #6fb1fc);
    background: -webkit-linear-gradient(32deg, #0052d4, #4364f7, #6fb1fc);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

.bTeam {
    background: linear-gradient(32deg, #ffe259, #ffa751);
    background: -webkit-linear-gradient(32deg, #ffe259, #ffa751);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

.moreNeeded {
    font-weight: bold;
    color: #ff5555;
}

</style>