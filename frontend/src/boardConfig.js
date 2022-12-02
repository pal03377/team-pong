import { get, writable } from 'svelte/store';
import { locale } from 'svelte-i18n';

export const boardConfig = writable({});

boardConfig.subscribe((config) => {
    if (config.language) {
        locale.set(config.language);
    }
});

async function loadBoardConfig() {
    const response = await fetch('/config');
    const config = await response.json();
    boardConfig.set(config);
}
loadBoardConfig();

export function listenForConfigChange(socket) {
    socket.on('config', (config) => {
        boardConfig.set(config);
    });
}

export async function updateConfig() {
    const config = get(boardConfig);
    await fetch('/config', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(config)
    });
}