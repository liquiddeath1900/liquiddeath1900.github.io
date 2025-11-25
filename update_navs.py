#!/usr/bin/env python3
"""
Update navigation bars in blog posts and root pages
"""

# Navigation HTML from index.html for blog pages (with ../ prefix)
BLOG_NAV = '''    <!-- Navigation Bar -->
    <nav class="fixed top-0 w-full bg-white shadow-lg z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center">
                    <a href="../index.html#home" class="flex items-center">
                        <img src="../assets/website homelogo.png" alt="SeamlessFlow.ai" class="h-8 sm:h-10" loading="eager" style="image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges;">
                    </a>
                </div>
                <div class="hidden md:block">
                    <div class="ml-10 flex items-baseline space-x-4">
                        <div class="relative group">
                            <button class="text-gray-900 hover:text-blue-600 px-3 py-2 flex items-center">
                                Services <i class="fas fa-chevron-down ml-1 text-sm"></i>
                            </button>
                            <div class="absolute top-full left-0 bg-white shadow-xl rounded-lg py-2 w-48 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                                <a href="../local-seo.html" class="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600">Local SEO (Primary)</a>
                                <a href="../website-development.html" class="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600">Website Development</a>
                                <a href="../marketing-automation.html" class="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600">Marketing Automation</a>
                            </div>
                        </div>
                        <div class="relative group">
                            <button class="text-gray-900 hover:text-blue-600 px-3 py-2 flex items-center">
                                Industries <i class="fas fa-chevron-down ml-1 text-sm"></i>
                            </button>
                            <div class="absolute top-full left-0 bg-white shadow-xl rounded-lg py-2 w-48 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                                <a href="../hvac-seo.html" class="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600">HVAC SEO</a>
                                <a href="../plumber-seo.html" class="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600">Plumber SEO</a>
                                <a href="../electrician-seo.html" class="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600">Electrician SEO</a>
                                <a href="../roofing-seo.html" class="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600">Roofing SEO</a>
                                <a href="../cleaning-service-seo.html" class="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600">Cleaning Service SEO</a>
                            </div>
                        </div>
                        <div class="relative group">
                            <button class="text-gray-900 hover:text-blue-600 px-3 py-2 flex items-center">
                                Locations <i class="fas fa-chevron-down ml-1 text-sm"></i>
                            </button>
                            <div class="absolute top-full left-0 bg-white shadow-xl rounded-lg py-2 w-56 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                                <!-- New York Nested -->
                                <div class="relative group/ny">
                                    <button class="w-full text-left px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600 flex items-center justify-between">
                                        New York <i class="fas fa-chevron-right text-xs"></i>
                                    </button>
                                    <div class="absolute left-full top-0 bg-white shadow-xl rounded-lg py-2 w-48 opacity-0 invisible group-hover/ny:opacity-100 group-hover/ny:visible transition-all duration-200 z-50">
                                        <a href="../manhattan-seo.html" class="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600">Manhattan</a>
                                        <a href="../brooklyn-seo.html" class="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600">Brooklyn</a>
                                        <a href="../queens-seo.html" class="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600">Queens</a>
                                        <a href="../bronx-seo.html" class="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600">Bronx</a>
                                        <a href="../albany-seo.html" class="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600">Albany</a>
                                        <a href="../syracuse-seo.html" class="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600">Syracuse</a>
                                        <a href="../rochester-seo.html" class="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600">Rochester</a>
                                    </div>
                                </div>
                                <!-- Pennsylvania Nested -->
                                <div class="relative group/pa">
                                    <button class="w-full text-left px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600 flex items-center justify-between">
                                        Pennsylvania <i class="fas fa-chevron-right text-xs"></i>
                                    </button>
                                    <div class="absolute left-full top-0 bg-white shadow-xl rounded-lg py-2 w-48 opacity-0 invisible group-hover/pa:opacity-100 group-hover/pa:visible transition-all duration-200 z-50">
                                        <a href="../pittsburgh-seo.html" class="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600">Pittsburgh</a>
                                        <a href="../philadelphia-seo.html" class="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600">Philadelphia</a>
                                    </div>
                                </div>
                                <!-- Virginia Nested -->
                                <div class="relative group/va">
                                    <button class="w-full text-left px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600 flex items-center justify-between">
                                        Virginia <i class="fas fa-chevron-right text-xs"></i>
                                    </button>
                                    <div class="absolute left-full top-0 bg-white shadow-xl rounded-lg py-2 w-48 opacity-0 invisible group-hover/va:opacity-100 group-hover/va:visible transition-all duration-200 z-50">
                                        <a href="../richmond-seo.html" class="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600">Richmond</a>
                                        <a href="../norfolk-seo.html" class="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600">Norfolk</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <a href="../pricing.html" class="text-gray-900 hover:text-blue-600 px-3 py-2">Pricing</a>
                        <a href="../faq.html" class="text-gray-900 hover:text-blue-600 px-3 py-2">FAQ</a>
                        <a href="../index.html#results" class="text-gray-900 hover:text-blue-600 px-3 py-2">Case Studies</a>
                        <a href="../contact.html" class="text-gray-900 hover:text-blue-600 px-3 py-2">Contact</a>
                    </div>
                </div>
                <div class="md:hidden">
                    <button class="hamburger" id="mobile-menu-button" aria-label="Toggle mobile menu">
                        <span></span>
                        <span></span>
                        <span></span>
                    </button>
                </div>
            </div>
            <!-- Mobile Menu -->
            <div id="mobile-menu" class="md:hidden bg-white shadow-xl border-t border-gray-100 relative z-[60]">
                <div class="px-6 py-4 space-y-1">
                    <a href="../index.html#home" class="block text-gray-800 hover:text-blue-600 hover:bg-blue-50 py-3 px-4 rounded-lg font-medium transition-colors">
                        <i class="fas fa-home mr-3 text-blue-500"></i>Home
                    </a>

                    <!-- Services Collapsible -->
                    <div class="mobile-dropdown">
                        <button class="mobile-dropdown-btn w-full text-left text-gray-800 hover:text-blue-600 hover:bg-blue-50 py-3 px-4 rounded-lg font-medium transition-colors flex items-center justify-between">
                            <span><i class="fas fa-cogs mr-3 text-green-500"></i>Services</span>
                            <i class="fas fa-chevron-right transition-transform duration-200"></i>
                        </button>
                        <div class="mobile-dropdown-content pl-6 space-y-1" style="max-height: 0; overflow-y: auto; transition: max-height 0.3s ease;">
                            <a href="../local-seo.html" class="block text-gray-700 hover:text-blue-600 hover:bg-blue-50 py-2 px-4 rounded-lg transition-colors">
                                <i class="fas fa-map-marker-alt mr-3 text-blue-500"></i>Local SEO (Primary)
                            </a>
                            <a href="../website-development.html" class="block text-gray-700 hover:text-blue-600 hover:bg-blue-50 py-2 px-4 rounded-lg transition-colors">
                                <i class="fas fa-laptop-code mr-3 text-green-500"></i>Website Development
                            </a>
                            <a href="../marketing-automation.html" class="block text-gray-700 hover:text-blue-600 hover:bg-blue-50 py-2 px-4 rounded-lg transition-colors">
                                <i class="fas fa-robot mr-3 text-purple-500"></i>Marketing Automation
                            </a>
                        </div>
                    </div>

                    <!-- Industries Collapsible -->
                    <div class="mobile-dropdown">
                        <button class="mobile-dropdown-btn w-full text-left text-gray-800 hover:text-blue-600 hover:bg-blue-50 py-3 px-4 rounded-lg font-medium transition-colors flex items-center justify-between">
                            <span><i class="fas fa-industry mr-3 text-purple-500"></i>Industries</span>
                            <i class="fas fa-chevron-right transition-transform duration-200"></i>
                        </button>
                        <div class="mobile-dropdown-content pl-6 space-y-1" style="max-height: 0; overflow-y: auto; transition: max-height 0.3s ease;">
                            <a href="../hvac-seo.html" class="block text-gray-700 hover:text-blue-600 hover:bg-blue-50 py-2 px-4 rounded-lg transition-colors">
                                <i class="fas fa-thermometer-half mr-3 text-red-500"></i>HVAC SEO
                            </a>
                            <a href="../plumber-seo.html" class="block text-gray-700 hover:text-blue-600 hover:bg-blue-50 py-2 px-4 rounded-lg transition-colors">
                                <i class="fas fa-wrench mr-3 text-blue-500"></i>Plumber SEO
                            </a>
                            <a href="../electrician-seo.html" class="block text-gray-700 hover:text-blue-600 hover:bg-blue-50 py-2 px-4 rounded-lg transition-colors">
                                <i class="fas fa-bolt mr-3 text-yellow-500"></i>Electrician SEO
                            </a>
                            <a href="../roofing-seo.html" class="block text-gray-700 hover:text-blue-600 hover:bg-blue-50 py-2 px-4 rounded-lg transition-colors">
                                <i class="fas fa-home mr-3 text-brown-500"></i>Roofing SEO
                            </a>
                            <a href="../cleaning-service-seo.html" class="block text-gray-700 hover:text-blue-600 hover:bg-blue-50 py-2 px-4 rounded-lg transition-colors">
                                <i class="fas fa-broom mr-3 text-green-500"></i>Cleaning Service SEO
                            </a>
                        </div>
                    </div>

                    <!-- Locations Collapsible -->
                    <div class="mobile-dropdown">
                        <button class="mobile-dropdown-btn w-full text-left text-gray-800 hover:text-blue-600 hover:bg-blue-50 py-3 px-4 rounded-lg font-medium transition-colors flex items-center justify-between">
                            <span><i class="fas fa-map-marked-alt mr-3 text-red-500"></i>Locations</span>
                            <i class="fas fa-chevron-right transition-transform duration-200"></i>
                        </button>
                        <div class="mobile-dropdown-content pl-6 space-y-1" style="max-height: 0; overflow-y: auto; transition: max-height 0.3s ease;">
                            <!-- New York State -->
                            <div class="mobile-dropdown">
                                <button class="mobile-dropdown-btn w-full text-left text-gray-700 hover:text-blue-600 hover:bg-blue-50 py-2 px-4 rounded-lg transition-colors flex items-center justify-between">
                                    <span><i class="fas fa-apple-alt mr-3 text-green-600"></i>New York</span>
                                    <i class="fas fa-chevron-right transition-transform duration-200"></i>
                                </button>
                                <div class="mobile-dropdown-content pl-6 space-y-1" style="max-height: 0; overflow-y: auto; transition: max-height 0.3s ease;">
                                    <a href="../manhattan-seo.html" class="block text-gray-600 hover:text-blue-600 hover:bg-blue-50 py-1 px-4 rounded-lg transition-colors">Manhattan</a>
                                    <a href="../brooklyn-seo.html" class="block text-gray-600 hover:text-blue-600 hover:bg-blue-50 py-1 px-4 rounded-lg transition-colors">Brooklyn</a>
                                    <a href="../queens-seo.html" class="block text-gray-600 hover:text-blue-600 hover:bg-blue-50 py-1 px-4 rounded-lg transition-colors">Queens</a>
                                    <a href="../bronx-seo.html" class="block text-gray-600 hover:text-blue-600 hover:bg-blue-50 py-1 px-4 rounded-lg transition-colors">Bronx</a>
                                    <a href="../albany-seo.html" class="block text-gray-600 hover:text-blue-600 hover:bg-blue-50 py-1 px-4 rounded-lg transition-colors">Albany</a>
                                    <a href="../syracuse-seo.html" class="block text-gray-600 hover:text-blue-600 hover:bg-blue-50 py-1 px-4 rounded-lg transition-colors">Syracuse</a>
                                    <a href="../rochester-seo.html" class="block text-gray-600 hover:text-blue-600 hover:bg-blue-50 py-1 px-4 rounded-lg transition-colors">Rochester</a>
                                </div>
                            </div>
                            <!-- Pennsylvania -->
                            <div class="mobile-dropdown">
                                <button class="mobile-dropdown-btn w-full text-left text-gray-700 hover:text-blue-600 hover:bg-blue-50 py-2 px-4 rounded-lg transition-colors flex items-center justify-between">
                                    <span><i class="fas fa-liberty-bell mr-3 text-blue-600"></i>Pennsylvania</span>
                                    <i class="fas fa-chevron-right transition-transform duration-200"></i>
                                </button>
                                <div class="mobile-dropdown-content pl-6 space-y-1" style="max-height: 0; overflow-y: auto; transition: max-height 0.3s ease;">
                                    <a href="../pittsburgh-seo.html" class="block text-gray-600 hover:text-blue-600 hover:bg-blue-50 py-1 px-4 rounded-lg transition-colors">Pittsburgh</a>
                                    <a href="../philadelphia-seo.html" class="block text-gray-600 hover:text-blue-600 hover:bg-blue-50 py-1 px-4 rounded-lg transition-colors">Philadelphia</a>
                                </div>
                            </div>
                            <!-- Virginia -->
                            <div class="mobile-dropdown">
                                <button class="mobile-dropdown-btn w-full text-left text-gray-700 hover:text-blue-600 hover:bg-blue-50 py-2 px-4 rounded-lg transition-colors flex items-center justify-between">
                                    <span><i class="fas fa-monument mr-3 text-gray-600"></i>Virginia</span>
                                    <i class="fas fa-chevron-right transition-transform duration-200"></i>
                                </button>
                                <div class="mobile-dropdown-content pl-6 space-y-1" style="max-height: 0; overflow-y: auto; transition: max-height 0.3s ease;">
                                    <a href="../richmond-seo.html" class="block text-gray-600 hover:text-blue-600 hover:bg-blue-50 py-1 px-4 rounded-lg transition-colors">Richmond</a>
                                    <a href="../norfolk-seo.html" class="block text-gray-600 hover:text-blue-600 hover:bg-blue-50 py-1 px-4 rounded-lg transition-colors">Norfolk</a>
                                </div>
                            </div>
                        </div>
                    </div>

                    <a href="../pricing.html" class="block text-gray-800 hover:text-blue-600 hover:bg-blue-50 py-3 px-4 rounded-lg font-medium transition-colors">
                        <i class="fas fa-dollar-sign mr-3 text-yellow-500"></i>Pricing
                    </a>
                    <a href="../faq.html" class="block text-gray-800 hover:text-blue-600 hover:bg-blue-50 py-3 px-4 rounded-lg font-medium transition-colors">
                        <i class="fas fa-question-circle mr-3 text-purple-500"></i>FAQ
                    </a>
                    <a href="../index.html#results" class="block text-gray-800 hover:text-blue-600 hover:bg-blue-50 py-3 px-4 rounded-lg font-medium transition-colors">
                        <i class="fas fa-chart-line mr-3 text-green-500"></i>Case Studies
                    </a>
                    <a href="../contact.html" class="block text-gray-800 hover:text-blue-600 hover:bg-blue-50 py-3 px-4 rounded-lg font-medium transition-colors">
                        <i class="fas fa-envelope mr-3 text-red-500"></i>Contact
                    </a>
                    <div class="pt-4 border-t border-gray-100 mt-4 space-y-2">
                        <a href="../free-audit.html" class="bg-gradient-to-r from-yellow-500 to-yellow-600 text-black px-6 py-4 rounded-lg block text-center font-bold shadow-lg hover:shadow-xl transform hover:scale-105 transition-all">
                            <i class="fas fa-search mr-2"></i>Get Free Audit
                        </a>
                        <a href="tel:+13477498146" class="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-6 py-3 rounded-lg block text-center font-semibold shadow-lg hover:shadow-xl transform hover:scale-105 transition-all">
                            <i class="fas fa-phone mr-2"></i>Call (347) 749-8146
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </nav>'''

print("Helper script created - use directly in files")
