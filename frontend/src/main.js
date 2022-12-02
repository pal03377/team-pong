import TeamDecisionWrapper from './TeamDecisionWrapper.svelte';
import Board from './Board.svelte';
import Config from './Config.svelte';
import { initTranslations } from './translations/translationInit.js';
import setupShortcuts from './shortcuts.js';

initTranslations();
setupShortcuts();

function getEntry() {
	if (location.search.indexOf("board") >= 0) {
		return Board;
	} else if (location.search.indexOf("config") >= 0){
		return Config;
	}
	return TeamDecisionWrapper;
}

const app = new (getEntry())({
	target: document.body,
	props: {}
});

export default app;
