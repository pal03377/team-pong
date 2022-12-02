<script>

    import { _ } from "svelte-i18n";
    import { fly } from 'svelte/transition';
    export let open = false;
    let audioCreditsShown = false;

    const legalLink = "__LEGAL_LINK__";
    console.log({ legalLink });

</script>


{#if open}
    <help-dialog transition:fly={{ y: 50 }}>
        <button class="close" on:click={ () => open = false }>⨯</button>
        <h1>{ $_("client.help.title") }</h1>
        <p>
            { $_("client.help.texts.0") }
            { $_("client.help.texts.1") }
        </p>
        <p>
            { $_("client.help.texts.2") }
            { $_("client.help.texts.3") }
        </p>
        <p>
            { $_("client.help.credits.0") }
            { $_("client.help.credits.1") }
            <a href="https://pschwind.de" target="_blank" rel="noreferrer">pschwind.de</a><br>
            { $_("client.help.credits.2") }
        </p>
        <p>
            {#if audioCreditsShown}
                <ul>
                    <li>https://freesound.org/people/JustInvoke/sounds/446142/</li>
                    <li>https://freesound.org/people/plasterbrain/sounds/397354/</li>
                    <li>https://freesound.org/people/danieldouch/sounds/466556/</li>
                </ul>
            {:else}
                <button on:click={() => audioCreditsShown = true}>
                    { $_("client.help.soundEffectCredits") }
                </button>
            {/if}
        </p>
        <p>
            {#if legalLink}
                <a id="legal" href={ legalLink } target="_blank" rel="noopener noreferrer">
                    { $_("client.help.legal") }
                </a>
            {/if}
        </p>
    </help-dialog>
{/if}


<style>

@font-face {
	font-family: "Montserrat";
	src: url("/static/fonts/Montserrat-VariableFont_wght.ttf") format("truetype");
	font-weight: normal;
	font-style: normal;
}

help-dialog {
    position: fixed;
    width: 100%;
    max-width: 100%;
    max-height: 80%;
    padding: 24px;
    box-sizing: border-box;
    overflow-y: auto;
    bottom: 0;
    left: 0;
    border-radius: 8px 8px 0 0;
    background-color: white;
    color: black;
    font-family: Montserrat, sans-serif;
}

.close {
    position: absolute;
    top: 4px;
    right: 4px;
    font-size: 24px;
    background-color: transparent;
    border: none;
    cursor: pointer;
}

ul {
    max-width: 100%;
    word-break: break-all;
}

a {
    color: #0052d4;
    background: linear-gradient(32deg, #0052d4, #4364f7, #6fb1fc);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    text-fill-color: transparent;
}

button {
    color: #0052d4;
    border: none;
    border-radius: 4px;
    padding: 8px 12px;
    cursor: pointer;
}

</style>