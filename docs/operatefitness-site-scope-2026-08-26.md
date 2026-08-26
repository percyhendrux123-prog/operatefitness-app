# Operate Fitness site scope — 2026-08-26

## Status

Local preparation and implementation only. No production deploy, billing change, payment, or public campaign was executed.

## Canonical source

- Repository: `/Users/percystewart/github-projects/operatefitness-app`
- Remote: `percyhendrux123-prog/operatefitness-app`
- Current working branch: `feat/calculator-explainer-link`
- Production host observed: `https://operatefitness.app/`
- Production provider observed from headers: Netlify

## What the public site is

A static HTML site. `netlify.toml` copies source files into `dist` and publishes that directory. There is no package.json, React runtime, Supabase client, Resend integration, or Vercel runtime in this repo.

### Public routes before this pass

| Route | Status | Job |
|---|---:|---|
| `/` | 200 | PKFIT offer comparison, mechanism, calculator entry, operator, Axiom lane |
| `/peptides/` | 200 | Research-use mathematical calculator |
| `/policies/` | 200 | PKFIT purchase, fulfillment, refund, cancellation, privacy, support |
| `/about` | 404 | Not implemented |
| `/coachapp/` | 404 | Not implemented |
| `/license` | 404 | Not a route on this domain |

## Separate systems

### Public marketing site — Netlify/static

- Owns domain navigation, SEO metadata, homepage, calculator page, policies page, assets, robots, and sitemap.
- Uses external links for PKFIT Lite, PKFIT Standard Stripe checkout, Axiom, the calculator explainer, and Instagram support.
- Does not own user auth, client data, coach tenants, email delivery, or app provisioning.

### Coachapp — separate product

- Canonical repo: `/Users/percystewart/github-projects/pkfit-coachapp`
- Uses Supabase for auth/data/storage and Supabase Edge Functions for product workflows.
- Has a separate Netlify surface at `pkfit-coachapp.netlify.app`.
- Resend/Supabase/coachapp configuration must remain separate from the static marketing site until an explicit integration is designed and approved.

### Vercel / Resend / Supabase

No evidence in the public-site repo that these services are runtime dependencies of `operatefitness.app`. Treat any dashboard connection as provider/account-level context, not as proof that this static site consumes the service.

## Platform ownership findings

- **Netlify is canonical for `operatefitness.app`.** Account read-only inspection identified site `pkfit-app`, custom domain `operatefitness.app`, repo `https://github.com/percyhendrux123-prog/operatefitness-app`, production branch `main`, publish directory `dist`, and functions directory `netlify/functions`.
- **Local Netlify context is unsafe.** `netlify status` from this checkout reported the stale local project `pkfit-coachapp`; do not run a deploy from this checkout until the local link is corrected through an explicit, approval-bound platform step.
- **Vercel is auxiliary or legacy until proven otherwise.** An AXIOM-owned project named `operatefitness` exists at `operatefitness.vercel.app`, but the public custom domain is attached to Netlify and the committed site source contains no Vercel configuration or runtime dependency.
- **Supabase belongs to the separate Coachapp product.** The active `pkfit-coachapp` Supabase project exists, but this static site has no Supabase client, auth flow, database call, storage call, or edge-function reference.
- **Resend is not used by this site.** No Resend SDK, API endpoint, email form, or environment reference appears in the public-site repo. Any Resend configuration belongs to another surface until an explicit integration is designed.

Do not infer that a dashboard connection means the public site consumes a service. Verify ownership from the custom domain, repository/build settings, committed source, and live behavior before changing provider configuration.

## Approved offer model

### PKFIT personal coaching

- `$250/month per client` when Percy personally coaches that client.

### PKFIT LITE

- `$20 one time`.
- Self-guided training, nutrition/macros/meals, and cardio tools.
- Not a subscription and does not include 1:1 coaching, direct messages, weekly check-ins, or coach adjustments.

### Operate Fitness white-label Coachapp

- Working name: **Operate Fitness**.
- Descriptor: **A branded coaching app for coaches**.
- Evaluation: **14 days** for another coach to market and evaluate the workflow.
- Post-evaluation alternatives:
  - **$50/month Coachapp access**, or
  - **$250 one-time white-label license + $10/month hosting**.
- These alternatives must not be collapsed into one price or presented as PKFIT personal coaching.
- No public checkout is added in this pass. Coachapp CTA routes to a private conversation. There is no charge during the 14-day evaluation; billing begins only after the coach agrees in writing to move forward, with activation and setup confirmed before a charge.

## Implementation in this pass

1. Add `/coachapp/` as a public, non-checkout product page.
2. Add Operate Fitness to homepage navigation and the operator/product lanes.
3. Add the white-label offer to homepage copy without changing PKFIT Lite or Standard pricing.
4. Add white-label terms to the policy page as a plain-language offer clarification.
5. Update `netlify.toml` to copy `/coachapp/` into `dist`.
6. Add `/coachapp/` to `sitemap.xml` and update the last-modified date.
7. Keep the peptide calculator research-only and separate from acquisition claims.
8. Use no client screenshots, account screenshots, testimonials, fabricated metrics, fake scarcity, or public Coachapp checkout links.

## Acquisition readiness gates after implementation

Before public Coachapp traffic:

- Verify the production page is deployed from the intended branch.
- Confirm the page copy and pricing match this document.
- Confirm the private CTA destination and response process are ready.
- Produce sanitized, public-safe product visuals; current coachapp screenshots contain client/account data and are not approved.
- Create platform-specific launch assets and one offer per asset.
- Ensure the written continuation agreement specifies the selected path, license scope, activation/setup work, hosting inclusions, billing date, cancellation terms, and what happens after the evaluation.
- Only then approve a production deploy and public publishing separately.

## Rollback

All changes are local and revertible with git. No production state was touched.
