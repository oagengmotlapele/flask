function showPopup(popupId) {
    document.getElementById('overlay').style.display = 'flex';

    // Hide all popups first
    document.querySelectorAll('.popup').forEach(p => p.style.display = 'none');

    // Show the requested popup
    const popup = document.getElementById(popupId);
    if (popup) {
        popup.style.display = 'block';
    }
}

function hideAllPopups() {
    document.getElementById('overlay').style.display = 'none';

    // Hide all popups
    document.querySelectorAll('.popup').forEach(p => p.style.display = 'none');
}

document.addEventListener('DOMContentLoaded', function () {
    const overlay = document.getElementById('overlay');

    // Click outside the popup to close
    overlay.addEventListener('click', function (e) {
        if (e.target.id === 'overlay') {
            hideAllPopups();
        }
    });

    // Bind open buttons
    document.querySelectorAll('.open-popup-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const popupId = btn.getAttribute('data-popup-id');
            showPopup(popupId);
        });
    });

    // Bind close buttons inside each popup
    document.querySelectorAll('.close-popup-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            hideAllPopups();
        });
    });
});
