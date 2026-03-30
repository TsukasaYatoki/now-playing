const logsContainer = document.getElementById("logs-container");
const vantaElement = document.getElementById("vanta-bg");
const LOG_FADE_DURATION_MS = 1000;

if (window.VANTA && window.VANTA.WAVES && vantaElement) {
    window.VANTA.WAVES({
        el: vantaElement,
        mouseControls: false,
        touchControls: false,
        gyroControls: false,
        color: 0x0f5b37,
        shininess: 28,
        waveHeight: 16,
        waveSpeed: 0.6,
        zoom: 0.95
    });
}

if (logsContainer) {
    const fadeDuration = LOG_FADE_DURATION_MS;

    const source = new EventSource("/stream");
    source.onmessage = function (event) {
        const currentLogs = document.querySelectorAll(".log-entry");
        const hasCurrentLogs = currentLogs.length > 0;

        const newLog = document.createElement("div");
        newLog.className = "log-entry";
        newLog.style.transitionDuration = fadeDuration / 1000 + "s";
        newLog.innerHTML = event.data;

        logsContainer.appendChild(newLog);

        // Ensure the element is painted before we animate opacity.
        requestAnimationFrame(() => {
            currentLogs.forEach((oldLog) => {
                oldLog.style.opacity = 0;

                setTimeout(() => {
                    if (logsContainer.contains(oldLog)) {
                        logsContainer.removeChild(oldLog);
                    }
                }, fadeDuration);
            });

            const fadeInDelay = hasCurrentLogs ? fadeDuration : 0;
            setTimeout(() => {
                newLog.style.opacity = 1;
            }, fadeInDelay);
        });
    };
}
