function claim() {

    alert("Claim request sent!");

}

function sendClaim() {

    alert("Claim submitted to finder.");

}

function searchItems() {

    let input = document.getElementById("searchInput").value.toLowerCase();

    let items = document.querySelectorAll(".item");

    items.forEach(function (item) {

        let text = item.innerText.toLowerCase();

        if (text.includes(input)) {

            item.style.display = "block";

        } else {

            item.style.display = "none";

        }

    });

}

function toggleMenu() {

    var menu = document.getElementById("profileDropdown");

    if (menu.style.display === "block") {
        menu.style.display = "none";
    } else {
        menu.style.display = "block";
    }

}





// for REWARD PAGE

document.addEventListener("DOMContentLoaded", () => {
    const items = document.querySelectorAll(".leader-item");

    items.forEach((item, index) => {
        item.style.opacity = 0;
        setTimeout(() => {
            item.style.opacity = 1;
            item.style.transition = "0.5s";
        }, index * 200);
    });
});