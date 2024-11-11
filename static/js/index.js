
function updateWaitTimes() {
    fetch('/api/wait-times')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const waitTimesContainer = document.querySelector('.waiting-time-container');
                if (!waitTimesContainer) return;

                // Clear existing content
                waitTimesContainer.innerHTML = '';

                // Add each dining hall's wait time
                Object.entries(data.predictions).forEach(([location, prediction]) => {
                    const status = prediction.status;
                    let waitTimeHtml = '';
                    
                    if (status === 'success') {
                        waitTimeHtml = `
                            <div class="border p-2 flex-fill text-center wait-time-card">
                                <span class="d-block fw-bold">${location}</span>
                                <small>Estimated waiting time: ${prediction.wait_time} minutes</small>
                                <small class="d-block text-muted">Current crowd: ~${prediction.crowd} people</small>
                            </div>`;
                    } else if (status === 'closed') {
                        waitTimeHtml = `
                            <div class="border p-2 flex-fill text-center wait-time-card">
                                <span class="d-block fw-bold">${location}</span>
                                <small class="text-danger">Currently Closed</small>
                            </div>`;
                    } else {
                        waitTimeHtml = `
                            <div class="border p-2 flex-fill text-center wait-time-card">
                                <span class="d-block fw-bold">${location}</span>
                                <small class="text-warning">Temporarily unavailable</small>
                            </div>`;
                    }
                    
                    waitTimesContainer.innerHTML += waitTimeHtml;
                });

                // Update last refreshed time
                const lastUpdated = document.querySelector('.wait-times-updated');
                if (lastUpdated) {
                    const timestamp = new Date(data.timestamp);
                    lastUpdated.textContent = `Last updated: ${timestamp.toLocaleTimeString()}`;
                }
            }
        })
        .catch(error => {
            console.error('Error fetching wait times:', error);
            const waitTimesContainer = document.querySelector('.waiting-time-container');
            if (waitTimesContainer) {
                waitTimesContainer.innerHTML = `
                    <div class="alert alert-warning text-center w-100" role="alert">
                        Unable to load wait times. Please try again later.
                    </div>`;
            }
        });
}

// Update wait times initially and every 5 minutes
document.addEventListener('DOMContentLoaded', () => {
    updateWaitTimes();
    setInterval(updateWaitTimes, 300000); // 5 minutes
});