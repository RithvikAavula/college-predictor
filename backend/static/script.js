async function predict() {
  const rank = document.getElementById("rank").value;
  const categoryBase = document.getElementById("category").value;  // e.g., "OC"
  const gender = document.getElementById("gender").value;         // "MALE" or "FEMALE"
  const branch = document.getElementById("branch").value;

  if (!rank || rank < 1) {
    alert("Please enter a valid rank.");
    return;
  }

  const genderSuffix = gender === "MALE" ? "_BOYS" : "_GIRLS";
  const category = categoryBase + genderSuffix;

  let url = `/search?rank=${rank}&category=${category}`;
  if (branch) url += `&branch=${branch.toUpperCase()}`;

  try {
    const response = await fetch(url);
    if (!response.ok) {
      const errorData = await response.json();
      alert(errorData.error || "Error fetching data");
      return;
    }
    const data = await response.json();
    displayResults(data, category);
  } catch (err) {
    alert("Server error: " + err.message);
  }
}

function displayResults(data, category) {
  const resultDiv = document.getElementById("results");
  resultDiv.innerHTML = "<h2>Predicted Colleges & Branches</h2>";

  if (!data.length) {
    resultDiv.innerHTML += "<p>No colleges found matching your criteria.</p>";
    return;
  }

  data.forEach(item => {
    resultDiv.innerHTML += `
      <div class="college-card">
        <h3>${item.INSTITUTE_NAME}</h3>
        <p><strong>Branch:</strong> ${item.BRANCH_NAME} (${item.BRANCH})</p>
        <p><strong>Cutoff Rank (${category}):</strong> ${item[category]}</p>
        <p><strong>Location:</strong> ${item.PLACE}, ${item.DIST}</p>
        <p><strong>Tuition Fee:</strong> ₹${item.TUITION_FEE}</p>
        <p><strong>Affiliated To:</strong> ${item.AFFILIATED}</p>
      </div>
    `;
  });
}

function downloadPDF() {
  const element = document.getElementById("results");
  if (!element.innerHTML.trim()) {
    alert("No results to save.");
    return;
  }
  html2pdf().from(element).save('college_predictions.pdf');
}
