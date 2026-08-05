// Mobile browsers will not render a PDF inside an iframe -- they show a blank
// box or hand the file off to a download prompt -- so on narrow viewports we
// draw the pages ourselves with pdf.js instead of embedding the native viewer.
//
// If anything here fails (CDN blocked, parse error, unsupported browser) the
// markup is left exactly as it shipped, which means the "Open the PDF" link
// stays visible and the page is still usable.

const PDFJS_VERSION = "5.7.284";
const PDFJS_BASE = `https://cdn.jsdelivr.net/npm/pdfjs-dist@${PDFJS_VERSION}`;
const NARROW = window.matchMedia("(max-width: 700px)");

// Cap the backing-store resolution. Phones report device pixel ratios of 3+,
// and rendering every page of a multi-page paper at 3x is slow and memory
// hungry for no visible gain.
const MAX_PIXEL_RATIO = 2;

let pdfjs = null;

async function loadPdfjs() {
  if (!pdfjs) {
    pdfjs = await import(`${PDFJS_BASE}/build/pdf.min.mjs`);
    pdfjs.GlobalWorkerOptions.workerSrc = `${PDFJS_BASE}/build/pdf.worker.min.mjs`;
  }
  return pdfjs;
}

async function renderInline(container) {
  if (container.dataset.pdfInlineState) return;
  container.dataset.pdfInlineState = "rendering";

  const iframe = container.querySelector("iframe");
  const src = iframe && iframe.getAttribute("src");
  if (!src) return;
  // Drop the #view=... fragment; those are viewer directives, not part of the file.
  const url = src.split("#")[0];

  try {
    const lib = await loadPdfjs();
    const doc = await lib.getDocument(url).promise;

    const pages = document.createElement("div");
    pages.className = "pdf-pages";
    container.insertBefore(pages, container.firstChild);

    const width = pages.clientWidth || container.clientWidth;
    const ratio = Math.min(window.devicePixelRatio || 1, MAX_PIXEL_RATIO);

    for (let n = 1; n <= doc.numPages; n++) {
      const page = await doc.getPage(n);
      const unscaled = page.getViewport({ scale: 1 });
      const viewport = page.getViewport({ scale: (width / unscaled.width) * ratio });

      const canvas = document.createElement("canvas");
      canvas.width = viewport.width;
      canvas.height = viewport.height;
      canvas.setAttribute("role", "img");
      canvas.setAttribute("aria-label", `Page ${n} of ${doc.numPages}`);
      pages.appendChild(canvas);

      await page.render({ canvasContext: canvas.getContext("2d"), viewport }).promise;
    }

    // Only now swap out the link -- until the pages are actually on screen it
    // is the only way to read the paper.
    container.classList.add("pdf-inline");
    container.dataset.pdfInlineState = "done";
  } catch (err) {
    container.dataset.pdfInlineState = "failed";
    console.error("Inline PDF rendering failed, leaving the download link:", err);
  }
}

function sync() {
  if (!NARROW.matches) return;
  document.querySelectorAll(".pdf-container").forEach(renderInline);
}

sync();
// Covers a desktop window being dragged narrow, and orientation changes that
// cross the breakpoint after load.
NARROW.addEventListener("change", sync);
