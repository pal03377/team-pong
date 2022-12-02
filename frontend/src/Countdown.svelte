<script>

    export let countdown = -1;

    const audio = new Audio("/static/audio/countdown.wav");
    $: if (countdown > 0 && countdown <= 3) {
        audio.currentTime = 0;
        audio.play();
    }

</script>


{#if countdown > 0}
    {#key countdown}
        <div class="countdown">
            {#if countdown >= 60}
                {Math.floor(countdown / 60)}:{countdown % 60 < 10 ? "0" : ""}{countdown % 60}
            {:else}
                {countdown}
            {/if}
        </div>
    {/key}
{/if}


<style>

    @keyframes appear {
        from {
            transform: translate(-50%, -50%) scale(0.6);
            opacity: 1;
        }
        80% {
            opacity: .1;
        }
        to {
            transform: translate(-50%, -50%) scale(1.5);
            opacity: 0;
        }
    }

    .countdown {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        transform-origin: center;
        font-size: 10vw;
        font-weight: bold;
        animation: appear 800ms ease-out;
        animation-fill-mode: forwards;
    }

</style>