const statusSelect = document.querySelector("#status");
const tableBody = document.querySelector("#applications");
const summaryBox = document.querySelector("#summary");
const message = document.querySelector("#message");

const label = value => value.replaceAll("_", " ").replace(/\b\w/g, c => c.toUpperCase());

async function loadSummary() {
  const response = await fetch("/api/summary");
  if (!response.ok) throw new Error("Could not load summary");
  const data = await response.json();
  summaryBox.innerHTML = `<article><strong>${data.total}</strong><span>Total</span></article>` +
    Object.entries(data.by_status).map(([status, count]) =>
      `<article><strong>${count}</strong><span>${label(status)}</span></article>`).join("");
  statusSelect.innerHTML = '<option value="">All</option>' +
    Object.keys(data.by_status).map(status => `<option value="${status}">${label(status)}</option>`).join("");
}

async function loadApplications() {
  const query = statusSelect.value ? `?status=${encodeURIComponent(statusSelect.value)}` : "";
  const response = await fetch(`/api/applications${query}`);
  if (!response.ok) throw new Error("Could not load applications");
  const rows = await response.json();
  tableBody.innerHTML = rows.map(row => `<tr>
    <td>${row.company}</td>
    <td><a href="${row.job_url}" rel="noreferrer">${row.title}</a><small>${row.location}</small></td>
    <td>${row.track}</td>
    <td><span class="pill">${label(row.status)}</span></td>
    <td>${row.match_score ?? "—"}</td>
    <td>${label(row.sponsorship_status)} <small>${label(row.sponsorship_confidence)} confidence</small></td>
  </tr>`).join("");
  message.textContent = rows.length ? "" : "No applications match this filter.";
}

statusSelect.addEventListener("change", () => loadApplications().catch(showError));
function showError(error) { message.textContent = error.message; }
Promise.all([loadSummary(), loadApplications()]).catch(showError);
