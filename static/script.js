/* ======================================================
   CRYPTAGE — client-side logic (fixed)
   ====================================================== */

document.addEventListener("DOMContentLoaded", () => {

  /* ── refs ── */
  const btnCesar    = document.getElementById("btn-cesar");
  const btnVernam   = document.getElementById("btn-vernam");
  const btnVigenere = document.getElementById("btn-vigenere");
  const btnEncrypt  = document.getElementById("btn-encrypt");
  const btnDecrypt  = document.getElementById("btn-decrypt");
  const inputText   = document.getElementById("input-text");
  const inputKey    = document.getElementById("input-key");
  const keyHint     = document.getElementById("key-hint");
  const btnRun      = document.getElementById("btn-run");
  const errorMsg    = document.getElementById("error-msg");
  const resultBox   = document.getElementById("result-box");
  const resultVal   = document.getElementById("result-value");
  const btnCopy     = document.getElementById("btn-copy");
  const placeholder = document.getElementById("output-placeholder");

  let algorithm = "cesar";
  let action    = "chiffrement";

  /* ── activate toggle (works with class .tbtn) ── */
  function activate(groupId, btn) {
    document.querySelectorAll(`#${groupId} .tbtn`).forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
  }

  /* ── key hint ── */
  function updateKeyHint() {
    if (algorithm === "cesar") {
      keyHint.textContent = "nombre entier";
      inputKey.placeholder = "Ex: 3";
    } else if (algorithm === "vernam") {
      keyHint.textContent = "même longueur que le texte";
      inputKey.placeholder = "Ex: CLEF";
    } else {
      keyHint.textContent = "répétée si nécessaire";
      inputKey.placeholder = "Ex: CLEF";
    }
  }

  /* ── error helpers ── */
  function showError(msg) {
    errorMsg.textContent = msg;
    errorMsg.classList.add("visible");
  }
  function hideError() {
    errorMsg.classList.remove("visible");
  }

  /* ── algo buttons ── */
  btnCesar.addEventListener("click", () => {
    algorithm = "cesar";
    activate("algo-group", btnCesar);
    updateKeyHint();
  });
  btnVernam.addEventListener("click", () => {
    algorithm = "vernam";
    activate("algo-group", btnVernam);
    updateKeyHint();
  });
  btnVigenere.addEventListener("click", () => {
    algorithm = "vigenere";
    activate("algo-group", btnVigenere);
    updateKeyHint();
  });

  /* ── action buttons ── */
  btnEncrypt.addEventListener("click", () => {
    action = "chiffrement";
    activate("action-group", btnEncrypt);
  });
  btnDecrypt.addEventListener("click", () => {
    action = "dechiffrement";
    activate("action-group", btnDecrypt);
  });

  /* ── run ── */
  btnRun.addEventListener("click", async () => {
    hideError();
    resultBox.classList.add("hidden");
    placeholder.classList.remove("hidden");

    const texte = inputText.value.trim();
    const cle   = inputKey.value.trim();

    if (!texte) { showError("Veuillez entrer un texte."); return; }
    if (!cle)   { showError("Veuillez entrer une clé."); return; }

    btnRun.disabled = true;
    btnRun.querySelector(".btn-label").textContent = "Traitement...";

    try {
      const res = await fetch("/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ algorithm, action, texte, cle }),
      });

      const data = await res.json();

      if (!res.ok) {
        showError(data.error || "Une erreur est survenue.");
        return;
      }

      resultVal.textContent = data.resultat;
      resultBox.classList.remove("hidden");
      placeholder.classList.add("hidden");

    } catch (err) {
      showError("Erreur réseau — impossible de joindre le serveur.");
    } finally {
      btnRun.disabled = false;
      btnRun.querySelector(".btn-label").textContent = "Exécuter";
    }
  });

  /* ── copy ── */
  btnCopy.addEventListener("click", () => {
    navigator.clipboard.writeText(resultVal.textContent).then(() => {
      btnCopy.title = "Copié !";
      setTimeout(() => { btnCopy.title = "Copier"; }, 1500);
    });
  });

  /* ── Ctrl/Cmd + Enter ── */
  document.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) btnRun.click();
  });

  /* init */
  updateKeyHint();
});