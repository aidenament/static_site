// Mobile browsers will not render a PDF inside an iframe -- they show a blank
// box or hand the file off to a download prompt -- so on narrow viewports we
// build a viewer instead, using pdf.js's viewer components. That gives the
// same scrollable, selectable document the desktop viewer does, in a box
// sized for a phone, with a small toolbar for page count and zoom.
//
// If anything here fails (CDN blocked, parse error, no module support) the
// markup is left exactly as it shipped, so the "Open the PDF" link stays
// visible and the page is still usable.

const PDFJS_VERSION = "5.7.284";
const PDFJS_BASE = `https://cdn.jsdelivr.net/npm/pdfjs-dist@${PDFJS_VERSION}`;
const NARROW = window.matchMedia("(max-width: 700px)");

const ZOOM_STEP = 0.25;
const MIN_SCALE = 0.25;
const MAX_SCALE = 5;

let libs = null;

async function loadPdfjs() {
  if (!libs) {
    // The component stylesheet has to be in the document before the viewer
    // lays pages out, or the first paint has no page sizing at all.
    if (!document.querySelector("link[data-pdfjs]")) {
      const css = document.createElement("link");
      css.rel = "stylesheet";
      css.href = `${PDFJS_BASE}/web/pdf_viewer.css`;
      css.dataset.pdfjs = "true";
      document.head.appendChild(css);
    }
    // Strictly sequential: pdf_viewer.mjs destructures globalThis.pdfjsLib at
    // import time, so the core has to be loaded and published first.
    const core = await import(`${PDFJS_BASE}/build/pdf.min.mjs`);
    core.GlobalWorkerOptions.workerSrc = `${PDFJS_BASE}/build/pdf.worker.min.mjs`;
    globalThis.pdfjsLib = core;
    const viewer = await import(`${PDFJS_BASE}/web/pdf_viewer.mjs`);
    libs = { core, viewer };
  }
  return libs;
}

function buildShell(container, href) {
  const shell = document.createElement("div");
  shell.className = "pdf-viewer-shell";
  shell.innerHTML = `
    <div class="pdf-toolbar">
      <span class="pdf-pages-label" aria-live="polite">&nbsp;</span>
      <span class="pdf-toolbar-actions">
        <button type="button" class="pdf-btn" data-zoom="out" aria-label="Zoom out">&minus;</button>
        <button type="button" class="pdf-btn" data-zoom="in" aria-label="Zoom in">+</button>
        <a class="pdf-btn pdf-open" href="${href}" target="_blank" rel="noopener">Open</a>
      </span>
    </div>
    <div class="pdf-viewer-frame">
      <div class="pdf-viewer-scroll"><div class="pdfViewer"></div></div>
    </div>`;
  container.insertBefore(shell, container.firstChild);
  return shell;
}

async function renderInline(container) {
  if (container.dataset.pdfInlineState) return;
  container.dataset.pdfInlineState = "rendering";

  const iframe = container.querySelector("iframe");
  const src = iframe && iframe.getAttribute("src");
  if (!src) return;
  // Drop the #view=... fragment; those are directives for the native viewer.
  const url = src.split("#")[0];

  try {
    const { core, viewer: v } = await loadPdfjs();
    const shell = buildShell(container, url);
    const scroll = shell.querySelector(".pdf-viewer-scroll");
    const label = shell.querySelector(".pdf-pages-label");

    const eventBus = new v.EventBus();
    const linkService = new v.PDFLinkService({ eventBus });
    const pdfViewer = new v.PDFViewer({
      container: scroll,
      viewer: shell.querySelector(".pdfViewer"),
      eventBus,
      linkService,
      textLayerMode: 1,
    });
    linkService.setViewer(pdfViewer);

    eventBus.on("pagesinit", () => {
      // Fit the page to the phone's width rather than opening at 100%.
      pdfViewer.currentScaleValue = "page-width";
    });
    const setLabel = (page, total) => { label.textContent = `${page} / ${total}`; };
    eventBus.on("pagechanging", (e) => setLabel(e.pageNumber, pdfViewer.pagesCount));

    const doc = await core.getDocument(url).promise;
    pdfViewer.setDocument(doc);
    linkService.setDocument(doc, null);
    setLabel(1, doc.numPages);

    shell.querySelectorAll("[data-zoom]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const next = pdfViewer.currentScale + (btn.dataset.zoom === "in" ? ZOOM_STEP : -ZOOM_STEP);
        pdfViewer.currentScale = Math.min(MAX_SCALE, Math.max(MIN_SCALE, next));
      });
    });

    // Only now swap out the link -- until the viewer is on screen it is the
    // only way to read the paper.
    container.classList.add("pdf-inline");
    container.dataset.pdfInlineState = "done";
  } catch (err) {
    container.dataset.pdfInlineState = "failed";
    console.error("Inline PDF viewer failed, leaving the download link:", err);
  }
}

function sync() {
  if (!NARROW.matches) return;
  document.querySelectorAll(".pdf-container").forEach(renderInline);
}

sync();
// Covers a desktop window dragged narrow, and orientation changes that cross
// the breakpoint after load.
NARROW.addEventListener("change", sync);
