# SeamlessFlow.ai → Next.js Conversion Scope

## Current State Analysis

### Site Structure (30+ pages)
```
seamlessflow-site/
├── Core Pages (5)
│   ├── index.html          # Homepage
│   ├── about.html          # About us
│   ├── pricing.html        # Service pricing
│   ├── faq.html           # FAQ
│   └── contract.html       # Contract tool
│
├── Location Pages (7)
│   ├── manhattan-seo.html
│   ├── brooklyn-seo.html
│   ├── queens-seo.html
│   ├── bronx-seo.html
│   ├── albany-seo.html
│   ├── syracuse-seo.html
│   └── rochester-seo.html
│
├── Service Pages (4)
│   ├── local-seo.html
│   ├── cannabis-ai-automation.html
│   ├── marketing-automation.html
│   └── website-development.html
│
├── Tools
│   ├── discovery-call.html
│   └── free-audit.html
│
├── Client Audits (14+ reports)
│   └── audits/*.html
│
└── Client Quotes
    └── quotes/*.html
```

### What's Already Good
- Solid SEO foundation (schema markup, canonical URLs, OG tags)
- Performance optimizations (preconnects, preloads)
- Mobile responsive
- Tailwind CSS styling
- Good meta descriptions and keywords

---

## Next.js Conversion Benefits

| Benefit | Impact |
|---------|--------|
| **Faster page loads** | Server-side rendering = better Core Web Vitals |
| **Component reuse** | Header/footer/nav written once, used everywhere |
| **Dynamic routes** | `/[city]-seo` instead of 7 separate HTML files |
| **API routes** | Form handling built-in (no external services) |
| **Easy updates** | Change one component = updates all pages |
| **Better DX** | Hot reload, TypeScript, modern tooling |

---

## Proposed Next.js Structure

```
seamlessflow-app/
├── app/
│   ├── page.tsx                    # Homepage
│   ├── layout.tsx                  # Global layout (nav, footer)
│   ├── globals.css                 # Global styles
│   │
│   ├── about/page.tsx              # About page
│   ├── pricing/page.tsx            # Pricing page
│   ├── faq/page.tsx               # FAQ page
│   │
│   ├── services/
│   │   ├── page.tsx               # Services overview
│   │   ├── local-seo/page.tsx
│   │   ├── ai-automation/page.tsx
│   │   ├── marketing/page.tsx
│   │   └── website-dev/page.tsx
│   │
│   ├── locations/
│   │   └── [city]/page.tsx        # Dynamic: /locations/manhattan, etc.
│   │
│   ├── tools/
│   │   ├── discovery-call/page.tsx
│   │   ├── free-audit/page.tsx
│   │   └── contract/page.tsx
│   │
│   ├── audits/
│   │   └── [client]/page.tsx      # Dynamic client audits
│   │
│   └── api/
│       ├── submit-form/route.ts   # Form submissions
│       └── generate-audit/route.ts
│
├── components/
│   ├── Header.tsx                 # Reusable header
│   ├── Footer.tsx                 # Reusable footer
│   ├── Hero.tsx                   # Homepage hero
│   ├── ServiceCard.tsx           # Service cards
│   ├── PricingTable.tsx          # Pricing component
│   ├── FAQAccordion.tsx          # FAQ component
│   ├── TestimonialSlider.tsx     # Testimonials
│   ├── CTASection.tsx            # Call-to-action
│   └── LocationPage.tsx          # Template for location pages
│
├── lib/
│   ├── locations.ts              # Location data (cities, keywords)
│   ├── services.ts               # Service definitions
│   └── seo.ts                    # SEO metadata generators
│
├── public/
│   ├── assets/                   # Images, logos
│   └── favicon.ico
│
└── data/
    └── audits/                   # Client audit JSON data
```

---

## Migration Strategy

### Phase 1: Foundation (Day 1)
- [ ] Create Next.js project with Tailwind
- [ ] Set up global layout (nav, footer)
- [ ] Migrate homepage
- [ ] Configure SEO (metadata API)

### Phase 2: Core Pages (Day 2)
- [ ] About page
- [ ] Pricing page
- [ ] FAQ page
- [ ] Service pages (4)

### Phase 3: Dynamic Routes (Day 3)
- [ ] Location pages → `/locations/[city]`
- [ ] Audit pages → `/audits/[client]`
- [ ] Move location data to JSON

### Phase 4: Tools (Day 4)
- [ ] Discovery call form (already built separately)
- [ ] Free audit tool
- [ ] Contract generator (already Next.js)

### Phase 5: Polish (Day 5)
- [ ] 404 page
- [ ] Loading states
- [ ] Analytics integration
- [ ] Sitemap generation
- [ ] Final testing

---

## SEO Preservation Checklist

| Element | Current | Next.js Approach |
|---------|---------|------------------|
| Canonical URLs | ✅ Manual | `metadata.alternates.canonical` |
| OG tags | ✅ Manual | `metadata.openGraph` |
| Schema markup | ✅ JSON-LD | Keep in layout or page |
| Meta descriptions | ✅ Per page | `metadata.description` |
| Sitemap | ✅ robots.txt | `next-sitemap` package |
| Redirects | None | `next.config.js` redirects |

### URL Changes (with redirects)
```
OLD                           NEW
/manhattan-seo.html    →     /locations/manhattan
/brooklyn-seo.html     →     /locations/brooklyn
/local-seo.html        →     /services/local-seo
/audits/greenup.html   →     /audits/greenup-nyc
```

---

## Component Extraction

### Header Component (from all pages)
- Logo
- Navigation links
- Mobile hamburger menu
- CTA button

### Footer Component
- Service links
- Contact info
- Social links
- Legal pages

### Hero Section (homepage)
- Video background
- Headline + subhead
- CTA buttons
- Trust badges

### Location Page Template
- City-specific headline
- Local keywords
- Service descriptions
- Local testimonials
- Map embed

---

## Data Structure for Locations

```typescript
// lib/locations.ts
export const locations = {
  manhattan: {
    name: 'Manhattan',
    slug: 'manhattan',
    title: 'Manhattan Dispensary SEO',
    description: 'Local SEO for Manhattan cannabis dispensaries...',
    keywords: ['manhattan dispensary', 'dispensary near me manhattan'],
    neighborhoods: ['SoHo', 'Chelsea', 'Midtown', 'Upper East Side'],
    mapEmbed: '...'
  },
  brooklyn: {
    name: 'Brooklyn',
    // ...
  }
  // etc.
};
```

---

## Estimated Effort

| Phase | Effort | Priority |
|-------|--------|----------|
| Foundation | 2-3 hours | High |
| Core Pages | 3-4 hours | High |
| Dynamic Routes | 2-3 hours | Medium |
| Tools Integration | 2-3 hours | Medium |
| Polish | 2-3 hours | Low |
| **Total** | **~12-15 hours** | |

---

## Hosting

**Current:** GitHub Pages (seamlessflow-site repo)
**After:** Vercel (auto-deploy from new repo)

### Deployment Steps
1. Create new repo: `seamlessflow-app`
2. Push Next.js project
3. Import to Vercel
4. Add custom domain: `seamlessflow.ai`
5. Set up redirects from old URLs

---

## Questions Before Starting

1. **Keep audit reports static or make dynamic?**
   - Static: Copy HTML as-is
   - Dynamic: Store data in JSON, render from template

2. **Contract generator - merge or keep separate?**
   - Already at `/seamlessflow-contract-generator/`
   - Could merge into main app

3. **Discovery call form - merge or keep separate?**
   - Already built at separate Vercel project
   - Could integrate into main app

4. **Priority: Speed or feature-complete?**
   - Fast: Core pages only, audits stay static
   - Full: Everything converted, dynamic routes

---

## Next Steps

1. Create Next.js project
2. Extract shared components (header, footer)
3. Migrate homepage first
4. Test SEO preservation
5. Continue with remaining pages

Ready to start when you are.
