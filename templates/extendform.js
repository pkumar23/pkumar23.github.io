const source = document.querySelector("#Location");
const target1 = document.querySelector("#Dorms");
const target2 = document.querySelector("#Houses");
const target3 = document.querySelector("#Libraries");
const target4 = document.querySelector("#Cafes");

const displayWhenSelected = (source, value, target) => {
    const selectedIndex = source.selectedIndex;
    const isSelected = source[selectedIndex].value === value;
    target.classList[isSelected
        ? "add"
        : "remove"
    ]("show");
};
source.addEventListener("change", (evt) =>
    displayWhenSelected(source, "First-Year Dorm", target1)
);
source.addEventListener("change", (evt) =>
    displayWhenSelected(source, "Upperclass House", target2)
);
source.addEventListener("change", (evt) =>
    displayWhenSelected(source, "Library", target3)
);
source.addEventListener("change", (evt) =>
    displayWhenSelected(source, "Cafe", target4)
);
