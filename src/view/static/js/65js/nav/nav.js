function toggleMenu() {
    const nav = document.getElementById("nav1");
    nav.classList.toggle("show");

    const btn = document.getElementById("hamburger-toggle");
    btn.textContent = nav.classList.contains("show") ? "✖ Close" : "☰ Open";
}

function toggleDropdown(event) {
    event.preventDefault();

    const li = event.target.closest("li");

    // Close sibling dropdowns
    Array.from(li.parentElement.children).forEach(sibling => {
        if (sibling !== li) sibling.classList.remove("show");
    });

    // Toggle this dropdown
    li.classList.toggle("show");

    event.stopPropagation();
}

document.addEventListener("DOMContentLoaded", function () {
    // Hamburger toggle
    const hamburger = document.getElementById("hamburger-toggle");
    if (hamburger) {
        hamburger.addEventListener("click", toggleMenu);
    }

    // Dropdown toggle
    document.querySelectorAll("#nav1 .has-submenu").forEach(link => {
        link.addEventListener("click", function (event) {
            toggleDropdown(event);
        });
    });

    // Close dropdowns if clicked outside nav
    document.addEventListener("click", function (e) {
        const nav = document.getElementById("nav1");
        if (!nav.contains(e.target)) {
            document.querySelectorAll("#nav1 li.show").forEach(li => li.classList.remove("show"));
        }
    });
});
