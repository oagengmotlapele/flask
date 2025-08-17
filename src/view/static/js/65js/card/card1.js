document.addEventListener("DOMContentLoaded", () => {
    // Admin card actions
    document.querySelectorAll(".card1").forEach(cardEl => {
        const cardIndex = cardEl.dataset.cardIndex;

        cardEl.querySelectorAll(".card-btn").forEach(btn => {
            btn.addEventListener("click", () => {
                const action = btn.dataset.action;
                openForm(action, parseInt(cardIndex));
            });
        });

        cardEl.querySelectorAll("li").forEach(pointEl => {
            const pointIndex = pointEl.dataset.pointIndex;

            pointEl.querySelectorAll(".point-btn").forEach(btn => {
                btn.addEventListener("click", () => {
                    const action = btn.dataset.action;
                    openForm(action, parseInt(cardIndex), parseInt(pointIndex));
                });
            });
        });
    });
});
