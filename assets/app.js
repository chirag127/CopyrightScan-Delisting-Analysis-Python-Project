/* app.js — shared site logic for google-transparency-report-analysis.oriz.in */

// Mark active nav link
(function () {
  const path = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll("nav ul a").forEach((a) => {
    const href = a.getAttribute("href").split("/").pop() || "index.html";
    if (href === path || (path === "" && href === "index.html")) {
      a.classList.add("active");
    }
  });
})();

// Load JSON data from docs/data/<id>.json and render charts if Chart.js present
async function loadDatasetJson(id) {
  try {
    const res = await fetch(`data/${id}.json`);
    if (!res.ok) return null;
    return await res.json();
  } catch {
    return null;
  }
}

// Shared Chart.js defaults
function applyChartDefaults(Chart) {
  Chart.defaults.font.family =
    '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif';
  Chart.defaults.color = "#5a6478";
  Chart.defaults.borderColor = "#dde3ec";
  Chart.defaults.plugins.legend.labels.boxWidth = 12;
}

window.GTRA = { loadDatasetJson, applyChartDefaults };
