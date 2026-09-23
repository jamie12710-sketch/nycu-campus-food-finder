const state = {
  data: [],
  filtered: [],
  visible: 6,
};

const elements = {
  form: document.querySelector("#finder-form"),
  keyword: document.querySelector("#keyword"),
  area: document.querySelector("#area"),
  shop: document.querySelector("#shop"),
  budget: document.querySelector("#budget"),
  sort: document.querySelector("#sort"),
  clear: document.querySelector("#clear"),
  results: document.querySelector("#results"),
  count: document.querySelector("#result-count"),
  empty: document.querySelector("#empty"),
  error: document.querySelector("#load-error"),
  dataState: document.querySelector("#data-state"),
  showMore: document.querySelector("#show-more"),
};

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = "";
  let quoted = false;

  for (let i = 0; i < text.length; i += 1) {
    const char = text[i];
    const next = text[i + 1];
    if (char === '"' && quoted && next === '"') {
      cell += '"';
      i += 1;
    } else if (char === '"') {
      quoted = !quoted;
    } else if (char === "," && !quoted) {
      row.push(cell);
      cell = "";
    } else if ((char === "\n" || char === "\r") && !quoted) {
      if (char === "\r" && next === "\n") i += 1;
      row.push(cell);
      if (row.some((value) => value.trim() !== "")) rows.push(row);
      row = [];
      cell = "";
    } else {
      cell += char;
    }
  }
  if (cell || row.length) {
    row.push(cell);
    rows.push(row);
  }

  const headers = rows.shift().map((value) => value.replace(/^\uFEFF/, "").trim());
  return rows.map((values) => Object.fromEntries(headers.map((header, index) => [header, (values[index] || "").replace(/\u00A0/g, " ").trim()])));
}

function normalizeRows(rows) {
  return rows
    .map((row) => ({
      area: row["餐廳區域"],
      shop: row["店家"],
      item: row["餐點"],
      price: Number(String(row["價格"]).replaceAll("$", "").replaceAll(",", "").trim()),
      hours: row["營業時間"],
    }))
    .filter((row) => row.area && row.shop && row.item && Number.isFinite(row.price));
}

function unique(values) {
  return [...new Set(values)].sort((a, b) => a.localeCompare(b, "zh-Hant"));
}

function setOptions(select, values, placeholder) {
  const current = select.value;
  select.replaceChildren(new Option(placeholder, ""));
  values.forEach((value) => select.add(new Option(value, value)));
  select.value = values.includes(current) ? current : "";
}

function updateShopOptions() {
  const list = state.data.filter((row) => !elements.area.value || row.area === elements.area.value);
  setOptions(elements.shop, unique(list.map((row) => row.shop)), "全部店家");
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function applyFilters() {
  const query = elements.keyword.value.trim().toLocaleLowerCase("zh-Hant");
  const budget = elements.budget.value === "" ? Infinity : Number(elements.budget.value);

  state.filtered = state.data.filter((row) => {
    const haystack = `${row.area} ${row.shop} ${row.item}`.toLocaleLowerCase("zh-Hant");
    return (
      (!elements.area.value || row.area === elements.area.value) &&
      (!elements.shop.value || row.shop === elements.shop.value) &&
      (!query || haystack.includes(query)) &&
      row.price <= budget
    );
  });

  if (elements.sort.value === "price-asc") {
    state.filtered.sort((a, b) => a.price - b.price || a.item.localeCompare(b.item, "zh-Hant"));
  } else if (elements.sort.value === "price-desc") {
    state.filtered.sort((a, b) => b.price - a.price || a.item.localeCompare(b.item, "zh-Hant"));
  }

  renderResults();
}

function renderResults() {
  const visibleRows = state.filtered.slice(0, state.visible);
  elements.results.innerHTML = visibleRows.map((row) => `
    <article class="food-card">
      <div>
        <h3 title="${escapeHtml(row.item)}">${escapeHtml(row.item)}</h3>
        <p>${escapeHtml(row.shop)} · ${escapeHtml(row.area.replaceAll("_", " "))}</p>
      </div>
      <strong>NT$${row.price.toLocaleString("zh-TW")}</strong>
      <small>${escapeHtml(row.hours || "營業時間未提供")}</small>
    </article>
  `).join("");

  const total = state.filtered.length;
  const shown = Math.min(state.visible, total);
  elements.count.textContent = total === state.data.length
    ? `全部資料：${total} 筆，顯示 ${shown} 筆`
    : `符合條件：${total} 筆，顯示 ${shown} 筆`;
  elements.empty.hidden = total !== 0;
  elements.showMore.hidden = shown >= total;
  elements.showMore.textContent = `顯示更多餐點（尚有 ${total - shown} 筆）`;
}

function resetVisibleAndFilter() {
  state.visible = 6;
  applyFilters();
}

async function loadData() {
  try {
    const response = await fetch("restaurant_data.csv", { cache: "no-store" });
    if (!response.ok) throw new Error(`CSV request failed: ${response.status}`);
    state.data = normalizeRows(parseCsv(await response.text()));
    if (!state.data.length) throw new Error("CSV contains no valid rows");

    setOptions(elements.area, unique(state.data.map((row) => row.area)), "全部區域");
    setOptions(elements.shop, unique(state.data.map((row) => row.shop)), "全部店家");

    const prices = state.data.map((row) => row.price);
    document.querySelector("#stat-areas").textContent = unique(state.data.map((row) => row.area)).length;
    document.querySelector("#stat-shops").textContent = unique(state.data.map((row) => row.shop)).length;
    document.querySelector("#stat-items").textContent = state.data.length;
    document.querySelector("#stat-range").textContent = `$${Math.min(...prices)}–${Math.max(...prices)}`;

    elements.dataState.classList.add("ready");
    elements.dataState.innerHTML = "<i></i> 資料已就緒";
    elements.results.setAttribute("aria-busy", "false");
    applyFilters();
  } catch (error) {
    console.error(error);
    elements.results.setAttribute("aria-busy", "false");
    elements.error.hidden = false;
    elements.form.hidden = true;
    elements.dataState.classList.add("error");
    elements.dataState.innerHTML = "<i></i> 載入失敗";
  }
}

elements.keyword.addEventListener("input", resetVisibleAndFilter);
elements.budget.addEventListener("input", resetVisibleAndFilter);
elements.shop.addEventListener("change", resetVisibleAndFilter);
elements.sort.addEventListener("change", resetVisibleAndFilter);
elements.area.addEventListener("change", () => {
  updateShopOptions();
  resetVisibleAndFilter();
});
elements.clear.addEventListener("click", () => {
  elements.form.reset();
  updateShopOptions();
  resetVisibleAndFilter();
  elements.keyword.focus();
});
elements.showMore.addEventListener("click", () => {
  state.visible += 6;
  renderResults();
});
elements.form.addEventListener("submit", (event) => event.preventDefault());
document.querySelectorAll("[data-print]").forEach((button) => button.addEventListener("click", () => window.print()));
document.querySelector("#year").textContent = new Date().getFullYear();

loadData();
