"""Builds terms-of-service.html, privacy-policy.html, cookies-policy.html on the
book-call.html shell (same head CSS, nav, footer, scripts). Run site_chrome.py after."""
import re

UPDATED = "October 2026"
EMAIL = '<a href="mailto:info@seamlessflow.ai" class="text-blue-700 underline">info@seamlessflow.ai</a>'

def h2(n, t): return f'<h2 id="s{n}" class="text-2xl font-bold text-gray-900 mt-12 mb-4">{n}. {t}</h2>'
def p(t): return f'<p class="text-gray-700 leading-relaxed mb-4">{t}</p>'
def ul(items): return '<ul class="list-disc pl-6 space-y-2 text-gray-700 mb-4">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'

TERMS = [
 ("Agreement to these terms", [
   p("These Terms of Service (the \"Terms\") are an agreement between you and SeamlessFlow.ai (\"SeamlessFlow\", \"we\", \"us\"). They apply when you use seamlessflow.ai, book a call with us, or buy any of our services. By doing any of those, you agree to these Terms."),
   p("If you sign a quote, proposal, or service agreement with us, that document is part of these Terms. If the two ever conflict, the signed document wins."),
   p("You must be at least 18 years old and able to enter a contract on behalf of your business."),
 ]),
 ("What we do", [
   p("We help businesses grow through content. Our monthly packages can include:"),
   ul(["A discovery call and a full audit of your online presence (Google Business Profile, Instagram, Facebook, TikTok, YouTube, and website)",
       "A brand roadmap and a monthly content plan",
       "Scripts, shot lists, and story talking points",
       "Shoot days, editing, and posting",
       "Analytics tracking and reporting",
       "Paid ads on content that is already performing",
       "Add-ons such as Google SEO, Google Business Profile work, lead follow-up automation, AI chat assistants, websites, and security audits"]),
   p("What is included for you is set by your package and your approved quote. Anything outside that is extra and will be quoted before we do it."),
 ]),
 ("Discovery call, audit, and quotes", [
   p("Every new client starts with a discovery call and an audit of their accounts. The audit tells us what needs to be set up or fixed before monthly work can start."),
   p("You can choose to handle that setup yourself using the list we give you, or have us do it for a one-time onboarding fee. We send a written quote with your package and any onboarding fee. No work starts until you approve it."),
 ]),
 ("Fees, billing, and minimum terms", [
   ul(["<strong>Onboarding fee.</strong> Due when you approve your quote. It is non-refundable once audit or setup work has started.",
       "<strong>Monthly fee.</strong> Billed in advance on the same day each month.",
       "<strong>Minimum term.</strong> Launch and Growth packages have a 3-month minimum. Full Service has a 6-month minimum. After that, your plan continues month to month.",
       "<strong>Late payments.</strong> If a payment is more than 7 days late, we may pause work until the account is current. Paused time does not extend your minimum term.",
       "<strong>Changing packages.</strong> You can move up a package at any time. Moving down takes effect at the start of your next billing month after the minimum term."]),
 ]),
 ("Ad spend", [
   p("Ad spend is separate from our fees. You pay it directly to the ad platform (Meta, TikTok, YouTube, or Google) using your own payment method. We manage the campaigns. We are not responsible for platform charges, billing errors, or decisions the platforms make, including rejected ads or restricted accounts."),
 ]),
 ("Results", [
   p("When we say you can see results in as little as 30, 15, or 7 days depending on your package, we mean your first videos are live and real numbers are coming in. It does not mean a set number of views, followers, leads, or sales."),
   p("<strong>We do not guarantee specific views, followers, leads, rankings, or revenue.</strong> Platforms change how they show content, and results depend on your market, your offer, how you treat your customers, and things outside our control. Any examples or estimates we share are not promises."),
 ]),
 ("Your part", [
   p("Good content needs you to show up. You agree to:"),
   ul(["Be on time and prepared for shoot days, and follow the scripts and shot lists we provide",
       "Film your stories from the shot list and talking points we send",
       "Give us the account access we need, and keep your accounts in good standing",
       "Give us accurate information about your business, offers, and pricing",
       "Review content when we send it (see Approvals below)",
       "Take care of your customers and ask them for reviews. We can grow your reach. How you treat the people who show up is on you."]),
 ]),
 ("Shoot days", [
   p("Shoot dates are agreed in advance. If you need to reschedule, tell us at least 48 hours before. With less notice, or if you don't show up, the shoot may count as used for that month or carry a rescheduling fee."),
   p("You are responsible for having permission to film at your location. If customers, staff, or anyone else appears on camera, you are responsible for getting their consent. We can provide a simple release form."),
 ]),
 ("Travel", [
   p("We are based in New York City and travel for clients. Shoots outside the New York City area include a travel fee for transportation, lodging, and time on the road. The travel fee is quoted up front and added to your quote or invoice."),
   p("We book all travel ourselves so schedules and gear stay under our control. The travel fee is a set amount agreed in advance, not a pass-through of individual receipts."),
 ]),
 ("Approvals and revisions", [
   p("We send content for review before it is posted. You have 2 business days to approve it or ask for changes. If we don't hear back, we may post it as planned so your schedule doesn't slip."),
   p("Each video includes one round of revisions. Extra rounds, or changes that need a reshoot, may cost extra."),
 ]),
 ("Ownership and use of content", [
   p("Once your fees are paid in full, the final edited videos and posts we deliver are yours to use for your business."),
   p("Raw footage, project files, templates, and our methods stay ours. We can provide raw footage on request for a fee."),
   p("We may show work we made for you in our portfolio and on our own channels. If you don't want that, tell us in writing and we'll leave it out."),
   p("You confirm that anything you give us to use (logos, photos, music, product images, and so on) is yours or that you have the right to use it."),
 ]),
 ("Account access and security", [
   p("Where a platform allows it, we ask to be added as a partner or manager instead of using your password. You stay the owner of your accounts. When our work ends, you can remove our access, and we will stop using it."),
 ]),
 ("AI tools", [
   p("We use AI tools to help with research, planning, and drafting. A person on our team reviews everything before it goes to you or gets posted."),
 ]),
 ("Cancellation and termination", [
   p("After your minimum term, you can cancel with 30 days' written notice to " + EMAIL + ". Fees already paid are not refunded, and we will finish the work covered by them."),
   p("We may end our work with you if fees go unpaid, if you ask us to make content that is illegal or misleading, or if our team is treated with abuse. Fees for work already done are still owed."),
 ]),
 ("Confidentiality", [
   p("We keep your business information, numbers, and account access private and only use them to do the work. You agree to keep our pricing, methods, and internal documents private too."),
 ]),
 ("Limitation of liability", [
   p("To the fullest extent the law allows, we are not liable for indirect or consequential losses such as lost profits, lost data, or platform account actions. Our total liability for any claim is limited to the fees you paid us in the 3 months before the claim."),
 ]),
 ("Indemnification", [
   p("You agree to cover us against claims that come from content or materials you provided, from your products or services, or from your breach of these Terms."),
 ]),
 ("Governing law", [
   p("These Terms are governed by the laws of the State of New York. Any dispute will be handled in the state or federal courts located in New York County, New York."),
 ]),
 ("Changes to these terms", [
   p("We may update these Terms. If a change affects active clients, we will give 30 days' notice by email. The date at the top of this page shows when they were last updated."),
 ]),
 ("Contact", [
   p(f"Questions about these Terms? Email {EMAIL} or call <a href=\"tel:+13477498146\" class=\"text-blue-700 underline\">(347) 749-8146</a>."),
 ]),
]

PRIVACY = [
 ("Who we are", [
   p("This Privacy Policy explains how SeamlessFlow.ai (\"SeamlessFlow\", \"we\", \"us\") collects and uses information when you visit seamlessflow.ai, book a call, or work with us."),
 ]),
 ("Information you give us", [
   ul(["<strong>Discovery call form:</strong> your name, business name, email, phone, social or website links, your goals, timeline, which package interests you, and which accounts you already have",
       "<strong>Call booking:</strong> what you enter when you schedule through Calendly",
       "<strong>Client work:</strong> business details, brand materials, account access we are granted, and the footage and photos we film with you",
       "<strong>Messages:</strong> anything you send us by email, phone, text, or social media"]),
 ]),
 ("Information collected automatically", [
   p("When you visit the site, Google Analytics collects basic usage data such as pages viewed, device type, approximate location, and how you arrived. See our <a href=\"cookies-policy.html\" class=\"text-blue-700 underline\">Cookies Policy</a> for details."),
   p("When we manage your social or ad accounts, we see the analytics those platforms provide, such as views, engagement, and ad performance."),
 ]),
 ("How we use it", [
   ul(["To prepare for and hold your discovery call",
       "To audit your accounts, quote, and deliver our services",
       "To plan, film, edit, post, and report on your content",
       "To send invoices and handle billing",
       "To improve our site and services",
       "To meet legal obligations"]),
   p("We do not sell your personal information."),
 ]),
 ("Who we share it with", [
   p("We use trusted services to run our business. They only get what they need to do their job:"),
   ul(["<strong>Supabase:</strong> stores form submissions and powers client login",
       "<strong>Calendly:</strong> call scheduling",
       "<strong>Google Analytics:</strong> website analytics",
       "<strong>Meta, TikTok, YouTube, and Google:</strong> posting and ads on your behalf, using the access you grant",
       "<strong>Email and payment providers:</strong> communication and billing"]),
   p("We may also share information if the law requires it, or to protect our rights or someone's safety."),
 ]),
 ("Footage and people on camera", [
   p("Footage we film for you is used to make your content. We store it securely and only use it for your work, or in our portfolio unless you opt out. If you want footage of a specific person removed, contact us and we will work with you on it."),
 ]),
 ("How long we keep it", [
   p("Discovery form details are kept for up to 2 years if we don't end up working together. Client records are kept while we work together and as long as needed for billing, tax, and legal reasons after that. Raw footage is kept for up to 12 months after a project ends unless we agree otherwise."),
 ]),
 ("Security", [
   p("We use access controls and encrypted services to protect your information, and we ask for partner or manager access to your accounts instead of passwords wherever platforms allow. No system is perfectly secure, but if a breach affects your information, we will notify you as New York law requires."),
 ]),
 ("Your choices and rights", [
   p(f"You can ask to see, correct, or delete the personal information we hold about you by emailing {EMAIL}. You can opt out of marketing emails at any time with the unsubscribe link or by replying to us."),
 ]),
 ("Children", [
   p("Our site and services are for businesses and are not directed at anyone under 18. We do not knowingly collect information from children."),
 ]),
 ("Changes to this policy", [
   p("If we change this policy, we will update the date at the top of this page. Big changes will be emailed to active clients."),
 ]),
 ("Contact", [
   p(f"Questions about your privacy? Email {EMAIL} or call <a href=\"tel:+13477498146\" class=\"text-blue-700 underline\">(347) 749-8146</a>."),
 ]),
]

COOKIES = [
 ("What cookies are", [
   p("Cookies are small files a website stores in your browser. Some are needed for the site to work. Others help us understand how people use it."),
 ]),
 ("Cookies and similar tools we use", [
   '<div class="overflow-x-auto mb-4"><table class="w-full text-sm text-left text-gray-700 border border-gray-200 rounded-lg">'
   '<thead class="bg-gray-50 text-gray-900"><tr><th class="p-3 border-b">Tool</th><th class="p-3 border-b">What it does</th><th class="p-3 border-b">Type</th></tr></thead><tbody>'
   '<tr><td class="p-3 border-b font-semibold">Google Analytics (_ga, _ga_*)</td><td class="p-3 border-b">Counts visits and shows which pages people use</td><td class="p-3 border-b">Analytics</td></tr>'
   '<tr><td class="p-3 border-b font-semibold">Calendly</td><td class="p-3 border-b">Runs the booking calendar on our Book a Call page</td><td class="p-3 border-b">Third-party, needed to book</td></tr>'
   '<tr><td class="p-3 border-b font-semibold">Supabase (browser storage)</td><td class="p-3 border-b">Keeps clients signed in on the client login</td><td class="p-3 border-b">Essential</td></tr>'
   '<tr><td class="p-3 font-semibold">Font and style libraries</td><td class="p-3">Load icons and styles from public CDNs. They don\'t set cookies, but your browser connects to their servers.</td><td class="p-3">Essential</td></tr>'
   '</tbody></table></div>',
 ]),
 ("Third-party cookies", [
   p("Calendly and Google set their own cookies under their own privacy policies. We don't control them. You can read <a href=\"https://calendly.com/privacy\" class=\"text-blue-700 underline\" target=\"_blank\" rel=\"noopener noreferrer\">Calendly's privacy notice</a> and <a href=\"https://policies.google.com/privacy\" class=\"text-blue-700 underline\" target=\"_blank\" rel=\"noopener noreferrer\">Google's privacy policy</a>."),
 ]),
 ("Your choices", [
   p("You can block or delete cookies in your browser settings. The site will still work, but the booking calendar may not load if third-party cookies are blocked. In that case, call us at <a href=\"tel:+13477498146\" class=\"text-blue-700 underline\">(347) 749-8146</a> to book."),
   p("To opt out of Google Analytics on every site, you can use <a href=\"https://tools.google.com/dlpage/gaoptout\" class=\"text-blue-700 underline\" target=\"_blank\" rel=\"noopener noreferrer\">Google's opt-out add-on</a>."),
 ]),
 ("Changes", [
   p("If we add or remove tools, we will update this page and the date at the top."),
 ]),
 ("Contact", [
   p(f"Questions? Email {EMAIL}."),
 ]),
]

PAGES = [
 ("terms-of-service.html", "Terms of Service", "The terms for working with SeamlessFlow: packages, onboarding, billing, shoot days, approvals, content ownership, and more.", TERMS),
 ("privacy-policy.html", "Privacy Policy", "How SeamlessFlow collects, uses, and protects your information.", PRIVACY),
 ("cookies-policy.html", "Cookies Policy", "The cookies and similar tools seamlessflow.ai uses and how to control them.", COOKIES),
]

shell = open("book-call.html").read()
head_end = shell.index("<!-- NAV:START -->")
main_start = shell.index("    <!-- Discovery call funnel")
foot_start = shell.index("<!-- FOOTER:START -->")
head, tail = shell[:head_end], shell[foot_start:]

for fname, title, desc, sections in PAGES:
    slug = fname[:-5]
    h = re.sub(r"<title>.*?</title>", f"<title>{title} | SeamlessFlow</title>", head)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', h)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title} | SeamlessFlow">', h)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', h)
    h = h.replace("https://www.seamlessflow.ai/book-call", f"https://www.seamlessflow.ai/{slug}")
    toc = "".join(f'<li><a href="#s{i}" class="hover:text-blue-700">{i}. {t}</a></li>' for i, (t, _) in enumerate(sections, 1))
    body = "".join(h2(i, t) + "".join(parts) for i, (t, parts) in enumerate(sections, 1))
    main = f'''    <main id="home" class="pt-28 pb-20 bg-white">
        <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
            <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 mb-2">{title}</h1>
            <p class="text-gray-500 mb-8">Last updated: {UPDATED}</p>
            <div role="navigation" aria-label="On this page" class="bg-gray-50 border border-gray-100 rounded-2xl p-6 mb-4">
                <p class="font-bold text-gray-900 mb-3">On this page</p>
                <ol class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1 text-sm text-gray-600">{toc}</ol>
            </div>
            {body}
        </div>
    </main>

'''
    open(fname, "w").write(h + "<!-- NAV:START -->\n<!-- NAV:END -->\n\n" + main + tail)
    print("built", fname)
