(function () {
  "use strict";
  const base = "https://iqbal123456780.github.io/public-opinion/";
  const makeSlot = (kind, title, copy) => {
    const box = document.createElement("section");
    box.className = "pon-ad-slot pon-ad-" + kind;
    box.setAttribute("aria-label", "Advertisement placement");
    box.innerHTML = '<span class="pon-ad-label">ADVERTISEMENT</span><strong>' + title + '</strong><p>' + copy + '</p><a href="' + base + 'advertise.html">Promote your business here →</a>';
    return box;
  };
  const style = document.createElement("style");
  style.textContent = `
    .pon-ad-slot{box-sizing:border-box;background:#fff;border:1px dashed #c9c9c9;border-radius:8px;padding:18px;text-align:center;color:#555;font:14px/1.5 Arial,sans-serif;margin:22px 0}
    .pon-ad-slot .pon-ad-label{display:block;color:#888;font-size:10px;font-weight:700;letter-spacing:1.4px;margin-bottom:7px}
    .pon-ad-slot strong{display:block;color:#222;font-size:17px;margin-bottom:4px}
    .pon-ad-slot p{margin:0 0 8px!important;color:#666;font-size:13px}
    .pon-ad-slot a{color:#d71920;font-weight:700;text-decoration:none}
    .pon-ad-slot a:hover{text-decoration:underline}
    .pon-ad-banner{max-width:1200px;margin:22px auto;padding:20px}
    .pon-ad-sidebar{margin:0}
    .pon-ad-inarticle{margin:28px 0;background:#fafafa}
    .pon-article-layout{display:grid;grid-template-columns:minmax(0,1fr) 280px;gap:22px;align-items:start}
    .pon-article-layout>.article-card{min-width:0}\n    .pon-legacy-layout{display:grid;grid-template-columns:minmax(0,1fr) 280px;gap:22px;align-items:start}\n    .pon-legacy-content{min-width:0}\n    .pon-legacy-layout>.pon-article-aside{min-width:0}
    .pon-article-aside{position:sticky;top:18px}
    @media(max-width:850px){.pon-article-layout,.pon-legacy-layout{grid-template-columns:1fr}.pon-article-aside{position:static}.pon-ad-sidebar{max-width:none}}
    @media(max-width:650px){.pon-ad-banner{margin:16px 12px;padding:16px}}
  `;
  document.head.appendChild(style);
  const article = document.querySelector(".article-card");
  const articlePage = document.querySelector(".article-page");
  if (article && articlePage && !document.querySelector(".pon-article-layout")) {
    const layout = document.createElement("div");
    layout.className = "pon-article-layout";
    article.parentNode.insertBefore(layout, article);
    layout.appendChild(article);
    const aside = document.createElement("aside");
    aside.className = "pon-article-aside";
    aside.appendChild(makeSlot("sidebar", "Reach readers while they read", "Reserve this article sidebar placement for your brand."));
    layout.appendChild(aside);
  } else if (!article && !document.querySelector(".pon-legacy-layout")) {
    const main = document.querySelector("main.container");
    if (main && (main.querySelector("article") || main.querySelector(".article"))) {
      const layout = document.createElement("div");
      layout.className = "pon-legacy-layout";
      const content = document.createElement("div");
      content.className = "pon-legacy-content";
      while (main.firstChild) content.appendChild(main.firstChild);
      layout.appendChild(content);
      const aside = document.createElement("aside");
      aside.className = "pon-article-aside";
      aside.appendChild(makeSlot("sidebar", "Reach readers while they read", "Reserve this article sidebar placement for your brand."));
      layout.appendChild(aside);
      main.appendChild(layout);
    }
  }
  const body = document.querySelector(".article-body,.article-content,article.article,.article");
  if (body && !body.querySelector(".pon-ad-inarticle")) {
    const headings = body.querySelectorAll("h2");
    const target = headings.length >= 3 ? headings[2] : (headings.length ? headings[0] : null);
    if (target) target.insertAdjacentElement("afterend", makeSlot("inarticle", "Put your message in the story", "A clearly labelled sponsored placement within this article."));
    else body.appendChild(makeSlot("inarticle", "Put your message in the story", "A clearly labelled sponsored placement within this article."));
  }
})();