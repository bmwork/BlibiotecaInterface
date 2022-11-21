const starWrapper = document.querySelector(".VisualizeContainer__Book-Rate");
const stars = document.querySelectorAll(".fa-solid fa-star");

stars.forEach((star, clickedIdx) => {
    star.addEventListener("click", () => {
        starWrapper.classList.add("disabled")
        stars.forEach((otherStar, otherIdx) => {
            if (otherIdx <= clickedIdx) {
                otherStar.classList.add("active");
            }
        });
    });
});