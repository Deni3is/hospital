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

function setupColumnToggles(table) {
    const tools = document.querySelector(`[data-table-tools="${table.id}"]`);
    const container = tools?.querySelector("[data-column-toggles]");
    if (!container) {
        return;
    }

    Array.from(table.querySelectorAll("thead th")).forEach((header, index) => {
        const columnName = header.dataset.column;
        if (!columnName) {
            return;
        }

        const labelText =
            header.querySelector(".sort-button")?.textContent.trim() ||
            header.querySelector(".column-label")?.textContent.trim() ||
            header.textContent.trim();

        const label = document.createElement("label");
        label.className = "column-toggle";

        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.checked = true;
        checkbox.disabled = columnName === "actions";

        checkbox.addEventListener("change", () => {
            setColumnVisibility(table, index, checkbox.checked);
        });

        const text = document.createElement("span");
        text.textContent = labelText;

        label.appendChild(checkbox);
        label.appendChild(text);
        container.appendChild(label);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-interactive-table]").forEach((table) => {
        setupSorting(table);
        setupColumnToggles(table);
    });
});
