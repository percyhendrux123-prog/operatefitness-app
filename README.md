# operatefitness-app

PKFIT production site for **operatefitness.app**

## Contents
- `index.html` - homepage (LITE/Standard comparison, mechanism, free tool, operator, Axiom lane)
- `peptides/index.html` - immediately available research-math calculator
- `policies/index.html` - purchase, fulfillment, refund, cancellation, privacy, and support terms
- `assets/brand.css` - brand system tokens + type
- `robots.txt` / `sitemap.xml` - crawl controls for the static routes

The committed OG image is ready to serve. Its optional regeneration script uses macOS system font files, so non-macOS builds do not need to run the generator.

## Preview changes in this branch
- Homepage clearly separates PKFIT LITE ($20 one time) from PKFIT Standard ($250/month)
- Real LITE, Standard, Axiom, and calculator destinations replace broken routes
- Technical SEO metadata, canonical URLs, offer/FAQ structured data, robots, and sitemap are included
- The calculator is immediately usable; the nonfunctional browser-only email gate is removed
- Accessibility improvements include landmarks, skip links, focus states, labels, and live result status

This branch is not deployed. Production still serves the previous version until an explicit promotion approval.

## Deploy
`netlify.toml` builds the static source into `dist` and publishes `dist`.
Production branch: `main` after explicit approval.
