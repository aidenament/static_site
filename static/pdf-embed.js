// One PDF viewer, every viewport.
//
// There is no native way to embed a PDF that looks the same twice. <iframe>,
// <embed> and <object> all hand the file to whatever viewer the browser ships,
// and those are three different programs: PDFium in Chrome and Edge, a separate
// pdf.js build in Firefox, PDFKit in Safari. They implement different subsets
// of Adobe's #view= open parameters, none of them can be styled to match a
// page, and mobile browsers decline to render an embedded PDF at all. So the
// document is rendered here instead, which is the only way to get one
// appearance on every device.
//
// If anything fails (CDN blocked, no module support, a parse error) the markup
// is left exactly as it shipped and the "Open the PDF" link stays visible, so
// the paper is always reachable.

const PDFJS_VERSION = "5.7.284";
const PDFJS_BASE = `https://cdn.jsdelivr.net/npm/pdfjs-dist@${PDFJS_VERSION}`;

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
  shell.className = "pdf-shell";
  shell.innerHTML = `
    <div class="pdf-toolbar">
      <span class="pdf-group pdf-group-pages">
        <button type="button" class="pdf-btn" data-page="prev" aria-label="Previous page">&lsaquo;</button>
        <span class="pdf-pages" aria-live="polite">&nbsp;</span>
        <button type="button" class="pdf-btn" data-page="next" aria-label="Next page">&rsaquo;</button>
      </span>
      <span class="pdf-group">
        <button type="button" class="pdf-btn" data-zoom="out" aria-label="Zoom out">&minus;</button>
        <button type="button" class="pdf-btn" data-zoom="in" aria-label="Zoom in">+</button>
        <a class="pdf-btn" href="${href}" target="_blank" rel="noopener">Open</a>
      </span>
    </div>
    <div class="pdf-frame">
      <div class="pdf-scroll"><div class="pdfViewer"></div></div>
    </div>`;
  container.insertBefore(shell, container.firstChild);
  return shell;
}

async function mount(container) {
  if (container.dataset.pdfState) return;
  container.dataset.pdfState = "loading";

  // Read the path off the link rather than a data attribute, so the basepath
  // rewrite that runs over href="/..." at build time applies to it as well.
  const link = container.querySelector(".pdf-embed-link");
  const url = link && link.getAttribute("href");
  if (!url) {
    container.dataset.pdfState = "failed";
    return;
  }

  try {
    const { core, viewer: v } = await loadPdfjs();
    const shell = buildShell(container, url);
    const scroll = shell.querySelector(".pdf-scroll");
    const label = shell.querySelector(".pdf-pages");

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

    // Fit the page to the box rather than opening at 100%. Tracked so that a
    // resize can re-fit, but only while the reader has not chosen a zoom of
    // their own; re-fitting over a deliberate zoom would be obnoxious.
    let autoFit = true;
    eventBus.on("pagesinit", () => {
      pdfViewer.currentScaleValue = "page-width";
    });

    const setLabel = (page, total) => {
      label.textContent = `${page} / ${total}`;
    };
    eventBus.on("pagechanging", (e) => setLabel(e.pageNumber, pdfViewer.pagesCount));

    const doc = await core.getDocument(url).promise;
    pdfViewer.setDocument(doc);
    linkService.setDocument(doc, null);
    setLabel(1, doc.numPages);

    shell.querySelectorAll("[data-zoom]").forEach((btn) => {
      btn.addEventListener("click", () => {
        autoFit = false;
        const step = btn.dataset.zoom === "in" ? ZOOM_STEP : -ZOOM_STEP;
        const next = pdfViewer.currentScale + step;
        pdfViewer.currentScale = Math.min(MAX_SCALE, Math.max(MIN_SCALE, next));
      });
    });

    shell.querySelectorAll("[data-page]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const delta = btn.dataset.page === "next" ? 1 : -1;
        const target = pdfViewer.currentPageNumber + delta;
        if (target >= 1 && target <= pdfViewer.pagesCount) {
          pdfViewer.currentPageNumber = target;
        }
      });
    });

    // Covers a window dragged to a new width and a phone turned on its side.
    // Guarded on pagesCount because ResizeObserver fires once on observe,
    // which happens before the document has finished loading.
    new ResizeObserver(() => {
      if (autoFit && pdfViewer.pagesCount) {
        pdfViewer.currentScaleValue = "page-width";
      }
    }).observe(scroll);

    // Only now retire the link: until the viewer is on screen it is the only
    // way to read the paper.
    container.classList.add("is-ready");
    container.dataset.pdfState = "ready";
  } catch (err) {
    container.dataset.pdfState = "failed";
    console.error("PDF viewer failed to mount, leaving the download link:", err);
  }
}

document.querySelectorAll(".pdf-embed").forEach(mount);
