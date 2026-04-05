const LOG_FADE_DURATION_MS = 1000;

const setupLogStream = () => {
    const logsContainer = document.getElementById("logs-container");
    if (!logsContainer) return;

    const fadeDuration = LOG_FADE_DURATION_MS;

    const source = new EventSource("/stream");
    source.onmessage = (event) => {
        const currentLogs = document.querySelectorAll(".log-entry");
        const hasCurrentLogs = currentLogs.length > 0;

        const newLog = document.createElement("div");
        newLog.className = "log-entry";
        newLog.style.transitionDuration = `${fadeDuration}ms`;
        newLog.textContent = event.data;

        logsContainer.appendChild(newLog);

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
};

document.addEventListener("DOMContentLoaded", () => {
    setupLogStream();
});
