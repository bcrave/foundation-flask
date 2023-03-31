const params = new URLSearchParams(window.location.search);
const entries = params.entries();
const { term: searchTerm } = Object.fromEntries(entries);

if (searchTerm !== "") {
  const resultCards = document.querySelectorAll(".result-card");
  resultCards.forEach((card) => {
    const text = card.innerHTML;
    const regex = new RegExp(searchTerm, "gi");
    const newText = text.replace(regex, (match) => {
      return matchCase(searchTerm, match);
    });
    card.innerHTML = newText;
  });
}

function matchCase(text, pattern) {
  let result = "";
  for (let i = 0; i < text.length; i++) {
    const char = text.charAt(i);
    const patternCode = pattern.charCodeAt(i);

    if (patternCode >= 65 && patternCode < 65 + 26) {
      result += char.toUpperCase();
    } else {
      result += char.toLowerCase();
    }
  }
  return `<mark style="padding: 0; margin: 0;">${result}</mark>`;
}
