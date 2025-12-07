/* Synthetic dashboard interactions */

const apiBase = "http://localhost:8000";
const analysisOutput = document.getElementById("analysisOutput");
const riskGauge = document.getElementById("riskGauge");
const clusterChartCanvas = document.getElementById("clusterChart");
const recommendationsList = document.getElementById("recommendations");

const gaugeChart = new Chart(riskGauge, {
  type: "doughnut",
  data: {
    labels: ["Risk", "Remaining"],
    datasets: [
      {
        data: [0, 100],
        backgroundColor: ["#e76f51", "#e0e0e0"],
      },
    ],
  },
  options: { responsive: true, cutout: "70%" },
});

const clusterChart = new Chart(clusterChartCanvas, {
  type: "bar",
  data: { labels: [], datasets: [{ label: "Cluster Size", data: [], backgroundColor: "#2a9d8f" }] },
});

async function analyzeText() {
  const text = document.getElementById("textInput").value;
  const response = await fetch(`${apiBase}/analyze_text`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  const data = await response.json();
  analysisOutput.textContent = JSON.stringify(data, null, 2);

  await refreshRisk([text]);
}

async function refreshRisk(items) {
  const response = await fetch(`${apiBase}/risk_score`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text_items: items, domain_credibility: 70 }),
  });
  const data = await response.json();
  const riskScore = data.risk.score || 0;
  gaugeChart.data.datasets[0].data = [riskScore, 100 - riskScore];
  gaugeChart.update();

  const clusters = data.influence.narrative_clusters || {};
  const labels = Object.keys(clusters);
  const values = labels.map((key) => clusters[key].length);
  clusterChart.data.labels = labels;
  clusterChart.data.datasets[0].data = values;
  clusterChart.update();

  recommendationsList.innerHTML = "";
  const recs = [
    "Cross-verify claims with trusted references.",
    "De-escalate language and avoid amplifying fear or anger cues.",
    "Educate teams on synthetic manipulation tactics detected here.",
  ];
  recs.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    recommendationsList.appendChild(li);
  });
}

document.getElementById("analyzeBtn").addEventListener("click", analyzeText);
