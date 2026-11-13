// script.js - handles the form, calls Flask with fetch, updates the page.
const $ = (id) => document.getElementById(id);

const els = {
  type: $("message-type"),
  message: $("message"),
  generate: $("generate-btn"),
  copy: $("copy-btn"),
  download: $("download-btn"),
  regenerate: $("regenerate-btn"),
  clear: $("clear-btn"),
  inputError: $("input-error"),
  outputError: $("output-error"),
  placeholder: $("placeholder"),
  loading: $("loading"),
  result: $("result"),
  subject: $("subject"),
  body: $("result-body"),
};

let lastRequest = null;     // used by Regenerate
let generatedText = "";     // used by Copy / Download

function selectedTone() {
  return document.querySelector('input[name="tone"]:checked').value;
}

function setLoading(on) {
  els.loading.hidden = !on;
  els.generate.disabled = on;
  els.regenerate.disabled = on || !generatedText;
  els.generate.textContent = on ? "Generating..." : "Generate with AI";
  if (on) {
    els.placeholder.hidden = true;
    els.result.hidden = true;
    els.outputError.hidden = true;
  }
}

function showError(text, inInput) {
  const box = inInput ? els.inputError : els.outputError;
  box.textContent = text;
  box.hidden = false;
  if (!inInput) {
    // keep the previous result visible if there is one
    if (generatedText) els.result.hidden = false;
    else els.placeholder.hidden = false;
  }
}

function showResult(text) {
  generatedText = text;
  // Split a leading "Subject:" line from the body
  const match = text.match(/^\s*Subject:\s*(.+?)\r?\n+([\s\S]*)$/i);
  if (match) {
    els.subject.textContent = "Subject: " + match[1].trim();
    els.subject.hidden = false;
    els.body.textContent = match[2].trim();
  } else {
    els.subject.hidden = true;
    els.body.textContent = text.trim();
  }
  els.placeholder.hidden = true;
  els.result.hidden = false;
  els.copy.disabled = els.download.disabled = els.regenerate.disabled = false;
}

async function requestMessage(payload) {
  setLoading(true);
  try {
    const response = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (data.success) {
      showResult(data.generated_message);
    } else {
      showError(data.error || "Something went wrong. Please try again.", false);
    }
  } catch (err) {
    showError("Unable to connect to the AI service. Please try again.", false);
  } finally {
    setLoading(false);
  }
}

function onGenerate() {
  els.inputError.hidden = true;
  const message = els.message.value.trim();
  if (!message) {
    showError("Please enter your message.", true);
    els.message.focus();
    return;                               // no API call for empty input
  }
  lastRequest = { message, message_type: els.type.value, tone: selectedTone() };
  requestMessage(lastRequest);
}

function onRegenerate() {
  if (lastRequest) requestMessage(lastRequest);   // fresh API call every time
}

async function onCopy() {
  try {
    await navigator.clipboard.writeText(generatedText);
  } catch {
    const area = document.createElement("textarea");
    area.value = generatedText;
    document.body.appendChild(area);
    area.select();
    document.execCommand("copy");
    area.remove();
  }
  flash(els.copy, "Copied!");
}

function onDownload() {
  const blob = new Blob([generatedText], { type: "text/plain;charset=utf-8" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "message.txt";
  link.click();
  URL.revokeObjectURL(link.href);
}

function onClear() {
  els.message.value = "";
  generatedText = "";
  lastRequest = null;
  els.inputError.hidden = els.outputError.hidden = els.result.hidden = true;
  els.placeholder.hidden = false;
  els.copy.disabled = els.download.disabled = els.regenerate.disabled = true;
}

function flash(button, text) {
  const original = button.textContent;
  button.textContent = text;
  setTimeout(() => (button.textContent = original), 1500);
}

els.generate.addEventListener("click", onGenerate);
els.regenerate.addEventListener("click", onRegenerate);
els.copy.addEventListener("click", onCopy);
els.download.addEventListener("click", onDownload);
els.clear.addEventListener("click", onClear);
