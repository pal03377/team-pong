<script>

    import { xScale, yScale } from "./scale.js";
    export let team;
    export let platformHeight;

</script>

{#if team}
    <play-platform 
        style="--x-scale: {xScale}vw; --y-scale: {yScale}vh; --platform-height: {platformHeight}; --y: {- team.y * yScale}vh;"
        class:aTeam={team.team === "A"}
        class:bTeam={team.team === "B"}
    ></play-platform>
{/if}


<style>

play-platform {
    position: absolute;
    width: calc(var(--x-scale) * 2.5);
    height: calc(var(--y-scale) * var(--platform-height));
    top: calc(50vh - var(--y-scale) * var(--platform-height) / 2);
    border-radius: calc(var(--x-scale) * 2.5);
    transition: transform 100ms ease-in-out;
}

.aTeam {
    left: calc(var(--x-scale) * 6.5);
    transform: translate(-100%, var(--y));
    background: linear-gradient(32deg, #0052d4, #4364f7, #6fb1fc);
}

.bTeam {
    right: calc(var(--x-scale) * 6.5);
    transform: translate(100%, var(--y));
    background: linear-gradient(32deg, #ffe259, #ffa751);
}

</style>