const logsContainer = document.getElementById("logs-container");

if (logsContainer) {
    const speed = parseInt(logsContainer.dataset.speed || "500", 10);
    const fadeDuration = Number.isNaN(speed) ? 500 : speed;

    const source = new EventSource("/stream");
    source.onmessage = function(event) {
        const currentLogs = document.querySelectorAll(".log-entry");

        const newLog = document.createElement("div");
        newLog.className = "log-entry";
        newLog.style.transitionDuration = fadeDuration / 1000 + "s";
        newLog.innerHTML = event.data;

        logsContainer.appendChild(newLog);

        // Ensure the element is painted before we animate opacity.
        requestAnimationFrame(() => {
            newLog.style.opacity = 1;

            currentLogs.forEach((oldLog) => {
                oldLog.style.opacity = 0;

                setTimeout(() => {
                    if (logsContainer.contains(oldLog)) {
                        logsContainer.removeChild(oldLog);
                    }
                }, fadeDuration);
            });
        });
    };
}
