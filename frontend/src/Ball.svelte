<script>

    import { xScale, yScale } from "./scale.js";
    export let ball;

</script>


<play-ball style="--x-scale: {xScale}vw; --y-scale: {yScale}vh; --x: {ball.x}; --y: {- ball.y};"></play-ball>


<style>

play-ball {
    position: absolute;
    border-radius: 50%;
    background: #fff;
    border: 1px solid black;
    width: calc(var(--x-scale) * 3);
    height: calc(var(--x-scale) * 3);
    top: calc(50vh - var(--x-scale) * 3 / 2);
    left: calc(50vw - var(--x-scale) * 3 / 2);
    transform: translate(calc(var(--x-scale) * var(--x)), calc(var(--y-scale) * var(--y)));
    transition: transform 100ms linear;
}

</style>