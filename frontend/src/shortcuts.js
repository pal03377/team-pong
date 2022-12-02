export default function setupShortcuts() {
    document.addEventListener('keyup', function(event) {
        console.log(event)
        if (event.key === "b") {
            // open board
            location.search = "board=1";
        }
        if (event.key === "c") {
            // open config
            location.search = "config=1";
        }
    });
}