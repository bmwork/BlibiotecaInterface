const btn = document.querySelector("#msg-button");

btn.addEventListener("click", () => {
    btn.parentElement.parentElement.classList.add("msg-disabled");
});

