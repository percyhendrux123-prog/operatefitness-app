# operatefitness-app

PKFIT production site for **operatefitness.app**

## Contents
- `index.html` - homepage (PKFIT LITE/Standard comparison, Operate Fitness coach lane, mechanism, free tool, operator, Axiom lane)
- `coachapp/index.html` - Operate Fitness white-label Coachapp offer page
- `peptides/index.html` - immediately available research-math calculator
- `policies/index.html` - purchase, fulfillment, refund, cancellation, privacy, support, and Coachapp terms
- `assets/brand.css` - brand system tokens + type
- `robots.txt` / `sitemap.xml` - crawl controls for the static routes

The public site is intentionally static. Netlify owns hosting and deployment for this repo. Supabase, Resend, and the separate Coachapp runtime are not dependencies of `operatefitness.app`. Vercel is not referenced by the committed site source.

## Preview changes in this branch
- Homepage clearly separates PKFIT LITE ($20 one time) from PKFIT Standard ($250/month)
- Real LITE, Standard, Axiom, and calculator destinations replace broken routes
- Technical SEO metadata, canonical URLs, offer/FAQ structured data, robots, and sitemap are included
- Fix the calculator explainer CTA: it now jumps to the maintained in-page formula section instead of a dead external URL.
- Accessibility improvements include landmarks, skip links, focus states, labels, and live result status

This branch is not deployed. Production still serves the previous version until an explicit promotion approval.

## Deploy
`netlify.toml` builds the static source into `dist` and publishes `dist`.
Production branch: `main` after explicit approval.
