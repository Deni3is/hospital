function getCellValue(row, index) {
    const cell = row.children[index];
    if (!cell) {
        return "";
    }

    return (cell.dataset.value || cell.textContent || "").trim();
}

function compareValues(left, right, sortType) {
    if (sortType === "number") {
        return Number(left) - Number(right);
    }

    if (sortType === "date") {
        return new Date(left) - new Date(right);
    }

    return left.localeCompare(right, "ru", { numeric: true, sensitivity: "base" });
}

function updateSortIndicators(table, activeButton, direction) {
    table.querySelectorAll(".sort-button").forEach((button) => {
        button.dataset.sortDirection = "";
        button.classList.remove("is-sorted");
    });

    activeButton.dataset.sortDirection = direction;
    activeButton.classList.add("is-sorted");
}

function setupSorting(table) {
    const tbody = table.querySelector("tbody");
    if (!tbody) {
        return;
    }

    table.querySelectorAll("thead th[data-sort-type]").forEach((header, index) => {
        const button = header.querySelector(".sort-button");
        const sortType = header.dataset.sortType;
        if (!button) {
            return;
        }

        button.addEventListener("click", () => {
            const rows = Array.from(tbody.querySelectorAll("tr")).filter(
                (row) => !row.querySelector(".empty-state")
            );
            const nextDirection = button.dataset.sortDirection === "asc" ? "desc" : "asc";

            rows.sort((rowA, rowB) => {
                const result = compareValues(
                    getCellValue(rowA, index),
                    getCellValue(rowB, index),
                    sortType
                );
                return nextDirection === "asc" ? result : -result;
            });

            rows.forEach((row) => tbody.appendChild(row));
            updateSortIndicators(table, button, nextDirection);
        });
    });
}

function setColumnVisibility(table, columnIndex, visible) {
    table.querySelectorAll("tr").forEach((row) => {
        const cell = row.children[columnIndex];
        if (!cell) {
            return;
        }

        cell.classList.toggle("is-hidden-column", !visible);
    });
}

function closeColumnMenu(menu, trigger) {
    menu.classList.remove("is-open");
    menu.hidden = true;
    trigger.setAttribute("aria-expanded", "false");
}

function openColumnMenu(menu, trigger) {
    menu.hidden = false;
    menu.classList.add("is-open");
    trigger.setAttribute("aria-expanded", "true");
}

function toggleColumnMenu(menu, trigger) {
    if (menu.classList.contains("is-open")) {
        closeColumnMenu(menu, trigger);
        return;
    }

    openColumnMenu(menu, trigger);
}

function createCheckboxItem(table, index, labelText, isLocked) {
    const label = document.createElement("label");
    label.className = "column-option";

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = true;
    checkbox.disabled = isLocked;

    checkbox.addEventListener("change", () => {
        setColumnVisibility(table, index, checkbox.checked);
    });

    const text = document.createElement("span");
    text.className = "column-option-label";
    text.textContent = labelText;

    label.appendChild(checkbox);
    label.appendChild(text);
    return label;
}

function setupColumnToggles(table) {
    const tools = document.querySelector(`[data-table-tools="${table.id}"]`);
    const controls = tools?.querySelector("[data-column-controls]");
    const container = tools?.querySelector("[data-column-toggles]");
    if (!tools || !controls || !container) {
        return;
    }

    const trigger = document.createElement("button");
    trigger.type = "button";
    trigger.className = "column-menu-trigger";
    trigger.textContent = "\u0421\u0442\u043e\u043b\u0431\u0446\u044b";
    trigger.setAttribute("aria-expanded", "false");
    trigger.setAttribute("aria-haspopup", "dialog");

    container.classList.add("column-menu");
    container.hidden = true;
    controls.appendChild(container);

    const title = document.createElement("div");
    title.className = "column-menu-title";
    title.textContent = "\u0412\u044b\u0431\u043e\u0440 \u0441\u0442\u043e\u043b\u0431\u0446\u043e\u0432";
    container.appendChild(title);

    const hint = document.createElement("div");
    hint.className = "column-menu-hint";
    hint.textContent =
        "\u041e\u0442\u043c\u0435\u0442\u044c\u0442\u0435 \u0433\u0430\u043b\u043e\u0447\u043a\u0430\u043c\u0438 \u043f\u043e\u043b\u044f, \u043a\u043e\u0442\u043e\u0440\u044b\u0435 \u0434\u043e\u043b\u0436\u043d\u044b \u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0430\u0442\u044c\u0441\u044f \u0432 \u0442\u0430\u0431\u043b\u0438\u0446\u0435.";
    container.appendChild(hint);

    const options = document.createElement("div");
    options.className = "column-options";
    container.appendChild(options);

    trigger.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        toggleColumnMenu(container, trigger);
    });

    container.addEventListener("click", (event) => {
        event.stopPropagation();
    });

    document.addEventListener("click", (event) => {
        if (!tools.contains(event.target)) {
            closeColumnMenu(container, trigger);
        }
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeColumnMenu(container, trigger);
        }
    });

    controls.appendChild(trigger);

    Array.from(table.querySelectorAll("thead th")).forEach((header, index) => {
        const columnName = header.dataset.column;
        if (!columnName) {
            return;
        }

        const labelText =
            header.querySelector(".sort-button")?.textContent.trim() ||
            header.querySelector(".column-label")?.textContent.trim() ||
            header.textContent.trim();

        const isLocked = columnName === "actions";
        options.appendChild(createCheckboxItem(table, index, labelText, isLocked));
    });
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-interactive-table]").forEach((table) => {
        setupSorting(table);
        setupColumnToggles(table);
    });
});
