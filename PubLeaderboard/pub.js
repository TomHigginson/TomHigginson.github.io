// Categories to show in main table
const mainCategories = [
  "Selection",
  "Toilets",
  "Atmos",
  "Price",
  "Staff",
  "Interior",
  "Exterior",
  "Extras",
  "Foodage"
];

// Helper: parse CSV into objects
function parseCSV(text) {
  const lines = text.trim().split("\n");
  const headers = lines.shift().split(",");

  return lines.map(line => {
    const values = line.match(/(".*?"|[^",]+)(?=\s*,|\s*$)/g)
                    .map(v => v.replace(/^"|"$/g, ""));
    const obj = {};
    headers.forEach((h, i) => obj[h] = values[i]);
    return obj;
  });
}

fetch("BristolPubs_subtotals_SeperateFood.csv")
  .then(r => r.text())
  .then(csvText => {

    const pubs = parseCSV(csvText);

    // Get pub name from URL (e.g., ?name=Apple)
    const params = new URLSearchParams(window.location.search);
    const pubName = params.get("name");

    const pub = pubs.find(x => x.Name === pubName);

    // Insert name and location
    document.getElementById("pub-name").textContent = pub.Name;
    document.getElementById("pub-location").textContent = pub.Location;

    const tbody = document.getElementById("score-body");

    // Build main scoring table (no PreFood / PreGuinness)
    mainCategories.forEach(cat => {
      const ben = pub[`${cat}_Ben`];
      const tom = pub[`${cat}_Tom`];
      const total = pub[`${cat}_Total`];

      const cleanBen = (ben === "0" ? "NA" : ben);
      const cleanTom = (tom === "0" ? "NA" : tom);
      const cleanTotal = (total === "0" ? "NA" : total);

      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${cat}</td>
        <td>${cleanBen}</td>
        <td>${cleanTom}</td>
        <td>${cleanTotal}</td>
      `;
      tbody.appendChild(row);
    });

    // ---- SUMMARY BLOCK ---- //
    const summary = document.getElementById("score-summary");

    const PreFoodTotal = pub.PreFood_Total;
    const PreGuinnessTotal = pub.PreGuinness_Total;
    const FinalTotal = pub.PostGuinnessTotal;

    let GuinnessText = "";
    if (pub["DoesGuinness?"] === "n") {
      GuinnessText = `<strong>Guinness Total:</strong> <span style="color:darkred;font-weight:bold;">Not Applicable</span>`;
    } else {
      const gTot = pub.Guinness_Total;
      GuinnessText = `<strong>Guinness Total:</strong> ${gTot === "0" ? "To be revisited" : gTot}`;
    }

    summary.innerHTML = `
      <p><strong>Pre-Food Total:</strong> ${PreFoodTotal}</p>
      <p><strong>Pre-Guinness Total:</strong> ${PreGuinnessTotal}</p>
      <p>${GuinnessText}</p>
      <p><strong>Final Post-Guinness Total:</strong> ${FinalTotal}</p>
    `;

    // ----- COMMENTS SECTION ----- //
    const commentsBox = document.getElementById("pub-comments");

    let comments = pub.Comments;

    // If empty or "0", give a message
    if (!comments || comments.trim() === "" || comments.trim() === "0") {
    commentsBox.innerHTML = `<p style="color:#777;font-style:italic;">No comments yet for this pub.</p>`;
    } else {
    // Replace | with line breaks if you want multiple comments
    comments = comments.replace(/\|/g, "<br><br>");

    commentsBox.innerHTML = `
        <div style="
        background:#fff;
        border:1px solid #ccc;
        padding:12px;
        border-radius:8px;
        max-width:700px;
        line-height:1.5;
        ">
        ${comments}
        </div>
    `;
    }

    // ----- IMAGE SECTION ----- //
    const imgBox = document.getElementById("pub-image");
    const imgFile = pub.Image;

    if (imgFile && imgFile.trim() !== "") {
    imgBox.innerHTML = `
        <img src="images/${imgFile}" 
            alt="Image of ${pub.Name}"
            style="max-width:400px;border-radius:10px;border:1px solid #ccc;">
    `;
    } else {
    imgBox.innerHTML = `<p style="color:#777;font-style:italic;">No image available.</p>`;
    }

  });

