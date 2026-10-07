"""Builds faq.html on the book-call.html shell. Questions ranked from 30 agency FAQ
pages + owner threads (research 2026-10-07). Answers must match terms-of-service.html.
Run site_chrome.py after."""
import json, re, html

BOOK = "book-call.html"

GROUPS = [
 ("Getting started", [
  ("How do we get started?",
   "Book a discovery call. We learn about your business and goals, then audit your Google profile and social accounts to see where you stand. You get a quote with the right package. Once you approve it, we start onboarding."),
  ("How fast can we get going?",
   "It depends on your package and what the audit finds. You can see results in as little as 30, 15, or 7 days depending on the package. By results we mean your first videos live and real numbers coming in."),
  ("Do I have to be on camera?",
   "No, but it helps. People buy from people, and owners on camera usually perform best. If that's not you, your team can be the face, or we build content around the work itself. Either way, we write what to say and coach you through it."),
  ("How much of my time does this take?",
   "Not much. Show up for shoot day, film a few stories from the shot list we send, and review content when it's ready. We handle the planning, editing, posting, and ads."),
 ]),
 ("Pricing and contracts", [
  ("How much does it cost?",
   "Packages start at $3,000, $4,500, and $6,500 a month. Your final price is set after your audit, based on your market, locations, and shoot volume. There's also a one-time onboarding fee set by what the audit finds. Ad spend is separate and paid directly to the platforms. Accounts that are already in good shape cost less to start. <a href=\"/#packages\" class=\"text-blue-700 underline\">See what's in each package</a>."),
  ("Is there a contract?",
   "Launch and Growth have a 3-month minimum. Full Service has 6 months. Content builds on itself, and the first months are when we learn what your audience responds to. After the minimum, it's month to month with 30 days' notice."),
  ("Is ad spend included?",
   "No. You pay the ad platforms directly with your own card, so you always see exactly where your money goes. We never mark up your ad spend."),
  ("Do you travel?",
   "Yes. We're based in New York City and travel for clients. Shoots outside the area include a travel fee, quoted up front."),
 ]),
 ("The content", [
  ("What platforms do you cover?",
   "Instagram, Facebook, TikTok, and YouTube on every package. Full Service also covers Google SEO and your Google Business Profile."),
  ("Do I approve content before it goes live?",
   "Yes. We send everything for review first. You have 2 business days to approve or ask for changes, so your schedule never stalls."),
  ("How many revisions do I get?",
   "One round per video is included. Most changes are small because the scripts are approved before we film."),
  ("Who posts, and do you need my password?",
   "We post for you. Where the platform allows it, we ask to be added as a partner or manager instead of using your password. You always stay the owner of your accounts."),
  ("Will you reply to comments and DMs for me?",
   "On Growth and Full Service, yes. During onboarding we build a reply guide with you: approved answers to the questions you get most. We handle those replies, and Full Service adds auto-replies where the platform allows it. Anything that needs your expertise, like quotes or technical questions, gets sent straight to you so no lead slips through. You're the expert, so you always get the final word."),
  ("Do I own the content?",
   "Yes. Once paid, the final videos are yours to use for your business. Raw footage is available on request for a fee."),
 ]),
 ("Results", [
  ("How long until I see real results?",
   "First videos and numbers come fast. Steady leads usually build over the first 3 to 6 months as we learn what works and put ad money behind it. Every month gets sharper than the last."),
  ("Do you guarantee results?",
   "No honest agency can guarantee views, followers, or sales. Platforms change, and results depend on your market and how you treat your customers. What we guarantee is the work: a clear plan, content on schedule, and honest numbers every month."),
  ("How do you report results?",
   "On the discovery call we agree on the number that matters to you, like calls, bookings, or sales. Reports track that, not just likes. Launch gets a monthly report, Growth every two weeks, and Full Service weekly with a strategy call."),
  ("Do I need ads, or is organic enough?",
   "Both work better together. Organic posts show us which videos people actually like. Ads take those winners and put them in front of more of the right people, faster."),
  ("What if I'm not happy?",
   "Tell us. We'll look at what's not working and change it in the next month's plan. After your minimum term, you can cancel any time with 30 days' notice."),
 ]),
]

shell = open("book-call.html").read()
head = shell[:shell.index("<!-- NAV:START -->")]
tail = shell[shell.index("<!-- FOOTER:START -->"):]
title = "FAQ | SeamlessFlow"
desc = "Answers to common questions about our content and ads packages: pricing, contracts, ad spend, approvals, ownership, and results."
head = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", head)
head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', head)
head = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', head)
head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', head)
head = head.replace("https://www.seamlessflow.ai/book-call", "https://www.seamlessflow.ai/faq")

schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
    for _, qs in GROUPS for q, a in qs]}
head = head.replace("</head>", '<script type="application/ld+json">' + json.dumps(schema) + "</script>\n</head>")

body = ""
for g, qs in GROUPS:
    items = "".join(f'''
                <details class="group bg-white rounded-2xl border border-gray-100 shadow-sm">
                    <summary class="flex items-center justify-between gap-4 cursor-pointer list-none p-5 sm:p-6 font-bold text-gray-900">
                        <span>{q}</span>
                        <i class="fas fa-plus text-blue-600 transition-transform duration-200 group-open:rotate-45"></i>
                    </summary>
                    <p class="px-5 sm:px-6 pb-6 -mt-1 text-gray-600 leading-relaxed">{a}</p>
                </details>''' for q, a in qs)
    body += f'''
            <h2 class="text-sm font-bold uppercase tracking-wider text-blue-600 mt-12 mb-4">{g}</h2>
            <div class="space-y-3">{items}
            </div>'''

main = f'''    <main id="home">
        <section class="pt-32 pb-14 bg-gray-950 text-white">
            <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                <span class="text-blue-400 font-semibold uppercase tracking-wider text-sm">FAQ</span>
                <h1 class="text-4xl sm:text-5xl font-extrabold mt-3 mb-4">Questions, answered</h1>
                <p class="text-lg text-gray-300">The things business owners ask us most. Don't see yours? Ask us on a discovery call.</p>
            </div>
        </section>
        <section class="pb-20 bg-gray-50">
            <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">{body}
                <div class="mt-14 text-center bg-white rounded-2xl border-2 border-dashed border-blue-200 p-8">
                    <h2 class="text-2xl font-bold text-gray-900 mb-2">Still have questions?</h2>
                    <p class="text-gray-600 mb-6">Book a 30-minute discovery call or call us at <a href="tel:+13477498146" class="text-blue-700 font-semibold">(347) 749-8146</a>.</p>
                    <a href="{BOOK}" class="inline-flex items-center bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-bold"><i class="fas fa-calendar-check mr-2"></i>Book a Discovery Call</a>
                </div>
            </div>
        </section>
    </main>

'''
# hide default disclosure marker in Safari
head = head.replace("    </style>", "        details summary::-webkit-details-marker { display: none; }\n    </style>", 1)
open("faq.html", "w").write(head + "<!-- NAV:START -->\n<!-- NAV:END -->\n\n" + main + tail)
print("built faq.html")
