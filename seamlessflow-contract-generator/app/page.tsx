'use client';

import { useState, useEffect } from 'react';

// Type definitions
interface ClientInfo {
  companyName: string;
  contactName: string;
  title: string;
  email: string;
  phone: string;
  address: string;
  city: string;
  state: string;
  zip: string;
  industry: string;
  industryOther?: string;
}

interface Services {
  seoStarter: boolean;
  seoMarketLeader: boolean;
  seoCityDomination: boolean;
  seoRegional: boolean;
  seoRegionalPrice?: number;
  websiteDev: boolean;
  websiteDevPrice: number;
  marketingAutomation: boolean;
  businessAutomation: boolean;
  businessAutomationPrice?: number;
  foundationPackage: boolean;
  foundationSetupFee: number;
  growthPackage: boolean;
  growthSetupFee: number;
  enterprisePackage: boolean;
  enterpriseMonthlyFee: number;
  enterpriseSetupFee: number;
}

interface Territory {
  primaryCity: string;
  state: string;
  zipCodes: string;
  boroughsDistricts: string;
}

interface ContractTerms {
  startDate: string;
  contractType: string;
  endDate: string;
  paymentDueDay: string;
}

// Contract Document Component
interface ContractDocumentProps {
  clientInfo: ClientInfo;
  services: Services;
  territory: Territory;
  contractTerms: ContractTerms;
  specialTerms: string;
  pricing: { monthlyTotal: number; oneTimeTotal: number; firstPayment: number };
  isSEOSelected: boolean;
}

function ContractDocument({ clientInfo, services, territory, contractTerms, specialTerms, pricing, isSEOSelected }: ContractDocumentProps) {
  const formatDate = (dateString: string) => {
    if (!dateString) return '___________';
    return new Date(dateString).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  };

  return (
    <div className="contract-document text-sm leading-relaxed">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-blue-600 mb-2">DIGITAL MARKETING & AUTOMATION SERVICES AGREEMENT</h1>
        <p className="text-lg font-semibold">SeamlessFlow.ai</p>
        <p className="text-gray-600">info@seamlessflow.ai | (347) 634-6547</p>
      </div>

      {/* Contract Date and Parties */}
      <div className="mb-6">
        <p className="mb-4"><strong>Effective Date:</strong> {formatDate(contractTerms.startDate)}</p>
        <p className="mb-2">This Digital Marketing & Automation Services Agreement ("Agreement") is entered into by and between:</p>
        <div className="ml-6 mb-4">
          <p><strong>SERVICE PROVIDER:</strong> SeamlessFlow.ai</p>
          <p className="ml-4">Email: info@seamlessflow.ai</p>
          <p className="ml-4">Phone: (347) 634-6547</p>
        </div>
        <div className="ml-6">
          <p><strong>CLIENT:</strong> {clientInfo.companyName || '___________________________'}</p>
          <p className="ml-4">Contact: {clientInfo.contactName || '___________________________'}, {clientInfo.title || '_______________'}</p>
          <p className="ml-4">Email: {clientInfo.email || '___________________________'}</p>
          <p className="ml-4">Phone: {clientInfo.phone || '___________________________'}</p>
          <p className="ml-4">Address: {clientInfo.address || '___________________________'}</p>
          {clientInfo.city && clientInfo.state && <p className="ml-4">{clientInfo.city}, {clientInfo.state} {clientInfo.zip}</p>}
          <p className="ml-4">Industry: {clientInfo.industry === 'Other' ? clientInfo.industryOther : clientInfo.industry || '_______________'}</p>
        </div>
      </div>

      <div className="page-break-before">
        <h2 className="text-xl font-bold mb-4 border-b-2 pb-2">1. SERVICES AND DELIVERABLES</h2>
        <p className="mb-3">The Service Provider agrees to provide the following services to the Client:</p>

        {/* SEO Services */}
        {isSEOSelected && (
          <div className="mb-4">
            <h3 className="font-bold mb-2">Local SEO Services:</h3>
            <ul className="list-disc ml-6 space-y-1">
              {services.seoStarter && (
                <>
                  <li><strong>SEO Starter Package ($497/month)</strong></li>
                  <li>Google Business Profile optimization and management</li>
                  <li>Basic on-page SEO (up to 10 pages)</li>
                  <li>Local directory submissions (up to 15 directories)</li>
                  <li>Monthly performance report</li>
                  <li>Review monitoring and response support</li>
                </>
              )}
              {services.seoMarketLeader && (
                <>
                  <li><strong>Market Leader Package ($997/month)</strong></li>
                  <li>Everything in SEO Starter, plus:</li>
                  <li>Advanced on-page SEO (up to 25 pages)</li>
                  <li>Content creation (2 blog posts/month, 500-750 words each)</li>
                  <li>Local link building (5 quality backlinks/month)</li>
                  <li>Competitor analysis and strategy adjustments</li>
                  <li>Monthly video SEO optimization</li>
                  <li>Schema markup implementation</li>
                </>
              )}
              {services.seoCityDomination && (
                <>
                  <li><strong>City Domination Package ($1,497/month)</strong></li>
                  <li>Everything in Market Leader, plus:</li>
                  <li>Comprehensive on-page SEO (unlimited pages)</li>
                  <li>Premium content creation (4 blog posts/month, 1,000+ words each)</li>
                  <li>Advanced link building (10+ quality backlinks/month)</li>
                  <li>Dedicated account manager</li>
                  <li>Weekly progress updates</li>
                  <li>Social media integration (posting and management)</li>
                  <li>Advanced local schema and structured data</li>
                </>
              )}
              {services.seoRegional && (
                <>
                  <li><strong>Regional Dominance Package (${services.seoRegionalPrice}/month)</strong></li>
                  <li>Everything in City Domination, plus:</li>
                  <li>Multi-location SEO strategy</li>
  <li>Separate Google Business Profiles for each location</li>
                  <li>Location-specific landing pages</li>
                  <li>Regional link building and outreach</li>
                  <li>Multi-city content strategy</li>
                  <li>Priority support and strategy calls</li>
                </>
              )}
            </ul>
          </div>
        )}

        {/* Web Design & Automation */}
        {(services.websiteDev || services.marketingAutomation || services.businessAutomation) && (
          <div className="mb-4">
            <h3 className="font-bold mb-2">Web Design & Automation Services:</h3>
            <ul className="list-disc ml-6 space-y-1">
              {services.websiteDev && (
                <>
                  <li><strong>Professional Website Development (${services.websiteDevPrice} one-time)</strong></li>
                  <li>Custom responsive website design</li>
                  <li>Mobile-optimized layout</li>
                  <li>SEO-friendly structure</li>
                  <li>Contact forms and lead capture</li>
                  <li>SSL certificate and security setup</li>
                  <li>Content management system (CMS) integration</li>
                  <li>Up to 10 pages of content</li>
                </>
              )}
              {services.marketingAutomation && (
                <>
                  <li><strong>Marketing Automation Platform ($1,500/month)</strong></li>
                  <li>Email marketing automation setup</li>
                  <li>CRM integration and management</li>
                  <li>Lead nurturing workflows</li>
                  <li>Automated follow-up sequences</li>
                  <li>Customer segmentation and targeting</li>
                  <li>Performance tracking and analytics</li>
                </>
              )}
              {services.businessAutomation && (
                <>
                  <li><strong>Business Operations Automation (${services.businessAutomationPrice}/month)</strong></li>
                  <li>Custom workflow automation</li>
                  <li>Integration with existing business tools</li>
                  <li>Process optimization and efficiency improvements</li>
                  <li>Automated reporting and data collection</li>
                  <li>Staff training on automation tools</li>
                </>
              )}
            </ul>
          </div>
        )}

        {/* Advanced Automation Packages */}
        {(services.foundationPackage || services.growthPackage || services.enterprisePackage) && (
          <div className="mb-4">
            <h3 className="font-bold mb-2">Advanced Automation Packages:</h3>
            <ul className="list-disc ml-6 space-y-1">
              {services.foundationPackage && (
                <>
                  <li><strong>Foundation Package ($1,500/month + ${services.foundationSetupFee} setup)</strong></li>
                  <li>Core business automation infrastructure</li>
                  <li>Email and SMS automation</li>
                  <li>Basic AI chatbot implementation</li>
                  <li>CRM setup and integration</li>
                  <li>Workflow documentation and training</li>
                  <li>Monthly optimization and support</li>
                </>
              )}
              {services.growthPackage && (
                <>
                  <li><strong>Growth Package ($3,000/month + ${services.growthSetupFee} setup)</strong></li>
                  <li>Everything in Foundation, plus:</li>
                  <li>Advanced AI integration (GPT-powered tools)</li>
                  <li>Multi-channel automation (email, SMS, social media)</li>
                  <li>Custom API integrations</li>
                  <li>Advanced analytics and reporting dashboards</li>
                  <li>Dedicated automation specialist</li>
                  <li>Bi-weekly strategy and optimization calls</li>
                </>
              )}
              {services.enterprisePackage && (
                <>
                  <li><strong>Enterprise Package (${services.enterpriseMonthlyFee}/month + ${services.enterpriseSetupFee} setup)</strong></li>
                  <li>Everything in Growth, plus:</li>
                  <li>Enterprise-grade automation architecture</li>
                  <li>Custom AI model training and deployment</li>
                  <li>Full-scale digital transformation consulting</li>
                  <li>Unlimited workflow and integration development</li>
                  <li>24/7 priority support</li>
                  <li>White-glove onboarding and implementation</li>
                  <li>Quarterly business review and strategy planning</li>
                </>
              )}
            </ul>
          </div>
        )}
      </div>

      {/* Territory Protection */}
      {isSEOSelected && (
        <div className="page-break-before">
          <h2 className="text-xl font-bold mb-4 border-b-2 pb-2">2. TERRITORY PROTECTION</h2>
          <p className="mb-3">For SEO services, the Service Provider grants the Client exclusive territory protection within the following defined area:</p>
          <div className="ml-6 mb-4">
            <p><strong>Primary City:</strong> {territory.primaryCity || '___________________________'}</p>
            <p><strong>State:</strong> {territory.state || '___________________________'}</p>
            <p><strong>ZIP Codes:</strong> {territory.zipCodes || '___________________________'}</p>
            {territory.boroughsDistricts && <p><strong>Boroughs/Districts:</strong> {territory.boroughsDistricts}</p>}
          </div>
          <p className="mb-2">The Service Provider agrees that during the term of this Agreement:</p>
          <ul className="list-disc ml-6 space-y-1">
            <li>No direct competitors in the Client's industry will be accepted within the protected territory</li>
            <li>Territory protection begins upon contract signing and first payment</li>
            <li>Territory exclusivity is maintained as long as the agreement remains in good standing</li>
            <li>If the Client cancels services, territory protection ends 30 days after final payment</li>
          </ul>
        </div>
      )}

      <div className="page-break-before">
        <h2 className="text-xl font-bold mb-4 border-b-2 pb-2">{isSEOSelected ? '3' : '2'}. PRICING AND PAYMENT TERMS</h2>
        <div className="mb-4">
          <p className="mb-2"><strong>Service Pricing:</strong></p>
          <div className="ml-6">
            <p>Monthly Recurring Services: <strong>${pricing.monthlyTotal.toFixed(2)}</strong></p>
            <p>One-Time Setup/Development Fees: <strong>${pricing.oneTimeTotal.toFixed(2)}</strong></p>
            <p className="text-lg font-bold mt-2">FIRST PAYMENT DUE: <strong className="text-blue-600">${pricing.firstPayment.toFixed(2)}</strong></p>
            <p className="text-sm text-gray-600 mt-1">Subsequent Monthly Payments: ${pricing.monthlyTotal.toFixed(2)}</p>
          </div>
        </div>
        <p className="mb-2"><strong>Payment Terms:</strong></p>
        <ul className="list-disc ml-6 space-y-1">
          <li>First payment (monthly service + setup fees) is due upon contract signing</li>
          <li>Subsequent payments are due on the {contractTerms.paymentDueDay} of each month</li>
          <li>Payments can be made via ACH transfer, credit card, or check</li>
          <li>A $50 fee will be applied to payments received more than 5 days past the due date</li>
          <li>Services may be suspended if payment is more than 15 days overdue</li>
          <li>All fees are non-refundable once work has commenced</li>
        </ul>
      </div>

      <div className="page-break-before">
        <h2 className="text-xl font-bold mb-4 border-b-2 pb-2">{isSEOSelected ? '4' : '3'}. CONTRACT TERM AND RENEWAL</h2>
        <p className="mb-2"><strong>Term:</strong> {contractTerms.contractType === 'month-to-month' ? 'Month-to-Month' : `${contractTerms.contractType.split('-')[0]}-Month Agreement`}</p>
        {contractTerms.contractType !== 'month-to-month' && (
          <p className="mb-2"><strong>End Date:</strong> {formatDate(contractTerms.endDate)}</p>
        )}
        <ul className="list-disc ml-6 space-y-1 mt-3">
          {contractTerms.contractType === 'month-to-month' ? (
            <>
              <li>This agreement continues on a month-to-month basis until terminated by either party</li>
              <li>Either party may terminate with 30 days written notice</li>
              <li>No early termination penalty applies</li>
            </>
          ) : (
            <>
              <li>This agreement is for a fixed term ending on {formatDate(contractTerms.endDate)}</li>
              <li>Agreement automatically renews for the same term unless either party provides 30 days written notice before the end date</li>
              <li>Early termination requires 30 days notice and may incur penalties (see Section {isSEOSelected ? '8' : '7'})</li>
            </>
          )}
        </ul>
      </div>

      <div className="page-break-before">
        <h2 className="text-xl font-bold mb-4 border-b-2 pb-2">{isSEOSelected ? '5' : '4'}. PERFORMANCE AND REPORTING</h2>
        <ul className="list-disc ml-6 space-y-1">
          <li>The Service Provider will provide monthly performance reports via email</li>
          <li>Reports will include key metrics such as website traffic, rankings, leads, and conversion data</li>
          <li>The Client will have access to a real-time dashboard for tracking progress</li>
          <li>Monthly strategy calls are available for City Domination and above packages</li>
          <li>SEO results typically take 3-6 months to show significant improvement</li>
          <li>The Service Provider does not guarantee specific rankings or traffic numbers due to the nature of search algorithms</li>
        </ul>
      </div>

      <div>
        <h2 className="text-xl font-bold mb-4 border-b-2 pb-2">{isSEOSelected ? '6' : '5'}. CLIENT RESPONSIBILITIES</h2>
        <ul className="list-disc ml-6 space-y-1">
          <li>Provide timely access to website, hosting, and necessary business accounts</li>
          <li>Respond to requests for content, images, and business information within 5 business days</li>
          <li>Review and approve deliverables within 7 business days</li>
          <li>Maintain active business operations and comply with all applicable laws</li>
          <li>Provide feedback and communicate any concerns promptly</li>
        </ul>
      </div>

      <div className="page-break-before">
        <h2 className="text-xl font-bold mb-4 border-b-2 pb-2">{isSEOSelected ? '7' : '6'}. INTELLECTUAL PROPERTY</h2>
        <ul className="list-disc ml-6 space-y-1">
          <li>Upon full payment, the Client owns all custom-developed website code, content, and creative materials</li>
          <li>The Service Provider retains ownership of proprietary tools, software, and methodologies</li>
          <li>The Service Provider may use the Client's logo and business name in portfolio and marketing materials unless otherwise requested</li>
          <li>Third-party software licenses (e.g., WordPress themes, plugins) remain property of their respective owners</li>
        </ul>
      </div>

      <div>
        <h2 className="text-xl font-bold mb-4 border-b-2 pb-2">{isSEOSelected ? '8' : '7'}. TERMINATION</h2>
        <p className="mb-2"><strong>Termination by Client:</strong></p>
        <ul className="list-disc ml-6 space-y-1 mb-3">
          <li>For month-to-month agreements: 30 days written notice with no penalty</li>
          <li>For fixed-term agreements: 30 days notice required; remaining months of contract must be paid at 50% of monthly rate</li>
          <li>Setup fees and one-time charges are non-refundable</li>
        </ul>
        <p className="mb-2"><strong>Termination by Service Provider:</strong></p>
        <ul className="list-disc ml-6 space-y-1">
          <li>The Service Provider may terminate immediately if payment is more than 30 days overdue</li>
          <li>The Service Provider may terminate with 30 days notice if the Client fails to meet their responsibilities</li>
          <li>Upon termination, the Client will receive all completed work and final reports</li>
        </ul>
      </div>

      <div className="page-break-before">
        <h2 className="text-xl font-bold mb-4 border-b-2 pb-2">{isSEOSelected ? '9' : '8'}. LIMITATION OF LIABILITY</h2>
        <ul className="list-disc ml-6 space-y-1">
          <li>The Service Provider's total liability under this agreement shall not exceed the total amount paid by the Client in the preceding 3 months</li>
          <li>The Service Provider is not liable for indirect, incidental, or consequential damages</li>
          <li>The Service Provider is not responsible for changes to search engine algorithms, social media policies, or third-party platform terms</li>
          <li>The Client agrees that SEO and digital marketing results cannot be guaranteed and may vary based on numerous factors beyond the Service Provider's control</li>
        </ul>
      </div>

      {specialTerms && (
        <div className="page-break-before">
          <h2 className="text-xl font-bold mb-4 border-b-2 pb-2">{isSEOSelected ? '10' : '9'}. SPECIAL TERMS AND CONDITIONS</h2>
          <p className="whitespace-pre-wrap">{specialTerms}</p>
        </div>
      )}

      <div className="page-break-before">
        <h2 className="text-xl font-bold mb-4 border-b-2 pb-2">{specialTerms ? (isSEOSelected ? '11' : '10') : (isSEOSelected ? '10' : '9')}. GENERAL PROVISIONS</h2>
        <ul className="list-disc ml-6 space-y-1">
          <li><strong>Entire Agreement:</strong> This agreement constitutes the entire understanding between the parties and supersedes all prior discussions</li>
          <li><strong>Amendments:</strong> Any changes to this agreement must be made in writing and signed by both parties</li>
          <li><strong>Governing Law:</strong> This agreement shall be governed by the laws of the State of New York</li>
          <li><strong>Severability:</strong> If any provision is found unenforceable, the remaining provisions remain in effect</li>
          <li><strong>Assignment:</strong> Neither party may assign this agreement without written consent from the other party</li>
        </ul>
      </div>

      {/* Signature Block */}
      <div className="page-break-before mt-12">
        <h2 className="text-xl font-bold mb-6">AGREEMENT SIGNATURE</h2>
        <p className="mb-6">By signing below, both parties acknowledge that they have read, understood, and agree to be bound by all terms and conditions of this Agreement.</p>

        <div className="grid grid-cols-2 gap-8 mt-12">
          <div>
            <p className="font-bold mb-6">SERVICE PROVIDER:</p>
            <p className="mb-2">SeamlessFlow.ai</p>
            <div className="border-b-2 border-black mb-2 pb-6"></div>
            <p className="text-sm">Authorized Signature</p>
            <div className="border-b-2 border-black mb-2 mt-6 pb-6"></div>
            <p className="text-sm">Printed Name and Title</p>
            <div className="border-b-2 border-black mb-2 mt-6 pb-6"></div>
            <p className="text-sm">Date</p>
          </div>

          <div>
            <p className="font-bold mb-6">CLIENT:</p>
            <p className="mb-2">{clientInfo.companyName || '___________________________'}</p>
            <div className="border-b-2 border-black mb-2 pb-6"></div>
            <p className="text-sm">Authorized Signature</p>
            <div className="border-b-2 border-black mb-2 mt-6 pb-6"></div>
            <p className="text-sm">Printed Name and Title</p>
            <div className="border-b-2 border-black mb-2 mt-6 pb-6"></div>
            <p className="text-sm">Date</p>
          </div>
        </div>

        <div className="mt-12 text-center text-sm text-gray-600">
          <p>Please sign and return this agreement to: info@seamlessflow.ai</p>
          <p>Questions? Contact us at (347) 634-6547</p>
        </div>
      </div>

      <style jsx>{`
        .contract-document {
          font-family: 'Times New Roman', serif;
        }
        @media print {
          .page-break-before {
            page-break-before: always;
          }
          .contract-document {
            font-size: 11pt;
          }
        }
      `}</style>
    </div>
  );
}

export default function ContractGenerator() {
  const [clientInfo, setClientInfo] = useState<ClientInfo>({
    companyName: '',
    contactName: '',
    title: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    state: '',
    zip: '',
    industry: '',
  });

  const [services, setServices] = useState<Services>({
    seoStarter: false,
    seoMarketLeader: false,
    seoCityDomination: false,
    seoRegional: false,
    websiteDev: false,
    websiteDevPrice: 2500,
    marketingAutomation: false,
    businessAutomation: false,
    foundationPackage: false,
    foundationSetupFee: 4500,
    growthPackage: false,
    growthSetupFee: 7500,
    enterprisePackage: false,
    enterpriseMonthlyFee: 6000,
    enterpriseSetupFee: 15000,
  });

  const [territory, setTerritory] = useState<Territory>({
    primaryCity: '',
    state: '',
    zipCodes: '',
    boroughsDistricts: '',
  });

  const [contractTerms, setContractTerms] = useState<ContractTerms>({
    startDate: '',
    contractType: 'month-to-month',
    endDate: '',
    paymentDueDay: '1st',
  });

  const [specialTerms, setSpecialTerms] = useState('');
  const [showPreview, setShowPreview] = useState(false);

  // Calculate pricing
  const calculatePricing = () => {
    let monthlyTotal = 0;
    let oneTimeTotal = 0;

    if (services.seoStarter) monthlyTotal += 497;
    if (services.seoMarketLeader) monthlyTotal += 997;
    if (services.seoCityDomination) monthlyTotal += 1497;
    if (services.seoRegional && services.seoRegionalPrice) monthlyTotal += services.seoRegionalPrice;
    if (services.websiteDev) oneTimeTotal += services.websiteDevPrice;
    if (services.marketingAutomation) monthlyTotal += 1500;
    if (services.businessAutomation && services.businessAutomationPrice) monthlyTotal += services.businessAutomationPrice;
    if (services.foundationPackage) {
      monthlyTotal += 1500;
      oneTimeTotal += services.foundationSetupFee;
    }
    if (services.growthPackage) {
      monthlyTotal += 3000;
      oneTimeTotal += services.growthSetupFee;
    }
    if (services.enterprisePackage) {
      monthlyTotal += services.enterpriseMonthlyFee;
      oneTimeTotal += services.enterpriseSetupFee;
    }

    const firstPayment = monthlyTotal + oneTimeTotal;
    return { monthlyTotal, oneTimeTotal, firstPayment };
  };

  const pricing = calculatePricing();
  const isSEOSelected = services.seoStarter || services.seoMarketLeader || services.seoCityDomination || services.seoRegional;

  // Save to localStorage
  useEffect(() => {
    const formData = { clientInfo, services, territory, contractTerms, specialTerms };
    localStorage.setItem('contractDraft', JSON.stringify(formData));
  }, [clientInfo, services, territory, contractTerms, specialTerms]);

  // Load from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('contractDraft');
    if (saved) {
      try {
        const data = JSON.parse(saved);
        if (data.clientInfo) setClientInfo(data.clientInfo);
        if (data.services) setServices(data.services);
        if (data.territory) setTerritory(data.territory);
        if (data.contractTerms) setContractTerms(data.contractTerms);
        if (data.specialTerms) setSpecialTerms(data.specialTerms);
      } catch (e) {
        console.error('Failed to load draft', e);
      }
    }
  }, []);

  // Calculate end date
  useEffect(() => {
    if (contractTerms.startDate && contractTerms.contractType !== 'month-to-month') {
      const start = new Date(contractTerms.startDate);
      let end = new Date(start);
      switch (contractTerms.contractType) {
        case '3-months': end.setMonth(end.getMonth() + 3); break;
        case '6-months': end.setMonth(end.getMonth() + 6); break;
        case '12-months': end.setMonth(end.getMonth() + 12); break;
      }
      setContractTerms(prev => ({ ...prev, endDate: end.toISOString().split('T')[0] }));
    }
  }, [contractTerms.startDate, contractTerms.contractType]);

  const handlePrint = () => window.print();

  const clearForm = () => {
    if (confirm('Are you sure you want to clear all form data?')) {
      setClientInfo({ companyName: '', contactName: '', title: '', email: '', phone: '', address: '', city: '', state: '', zip: '', industry: '' });
      setServices({ seoStarter: false, seoMarketLeader: false, seoCityDomination: false, seoRegional: false, websiteDev: false, websiteDevPrice: 2500, marketingAutomation: false, businessAutomation: false, foundationPackage: false, foundationSetupFee: 4500, growthPackage: false, growthSetupFee: 7500, enterprisePackage: false, enterpriseMonthlyFee: 6000, enterpriseSetupFee: 15000 });
      setTerritory({ primaryCity: '', state: '', zipCodes: '', boroughsDistricts: '' });
      setContractTerms({ startDate: '', contractType: 'month-to-month', endDate: '', paymentDueDay: '1st' });
      setSpecialTerms('');
      localStorage.removeItem('contractDraft');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="print:hidden">
        <div className="max-w-5xl mx-auto p-6">
          {/* Header */}
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-blue-600">SeamlessFlow.ai</h1>
                <p className="text-gray-600">Contract Generator</p>
              </div>
              <div className="text-right text-sm text-gray-600">
                <p>info@seamlessflow.ai</p>
                <p>(347) 634-6547</p>
              </div>
            </div>
          </div>

          {/* Client Info */}
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-2xl font-bold mb-4">Client Information</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input type="text" placeholder="Company Name *" className="border rounded px-3 py-2" value={clientInfo.companyName} onChange={(e) => setClientInfo({ ...clientInfo, companyName: e.target.value })} />
              <input type="text" placeholder="Contact Name *" className="border rounded px-3 py-2" value={clientInfo.contactName} onChange={(e) => setClientInfo({ ...clientInfo, contactName: e.target.value })} />
              <input type="text" placeholder="Title *" className="border rounded px-3 py-2" value={clientInfo.title} onChange={(e) => setClientInfo({ ...clientInfo, title: e.target.value })} />
              <input type="email" placeholder="Email *" className="border rounded px-3 py-2" value={clientInfo.email} onChange={(e) => setClientInfo({ ...clientInfo, email: e.target.value })} />
              <input type="tel" placeholder="Phone *" className="border rounded px-3 py-2" value={clientInfo.phone} onChange={(e) => setClientInfo({ ...clientInfo, phone: e.target.value })} />
              <input type="text" placeholder="Address" className="border rounded px-3 py-2" value={clientInfo.address} onChange={(e) => setClientInfo({ ...clientInfo, address: e.target.value })} />
              <input type="text" placeholder="City" className="border rounded px-3 py-2" value={clientInfo.city} onChange={(e) => setClientInfo({ ...clientInfo, city: e.target.value })} />
              <input type="text" placeholder="State" className="border rounded px-3 py-2" value={clientInfo.state} onChange={(e) => setClientInfo({ ...clientInfo, state: e.target.value })} />
              <input type="text" placeholder="ZIP Code" className="border rounded px-3 py-2" value={clientInfo.zip} onChange={(e) => setClientInfo({ ...clientInfo, zip: e.target.value })} />
              <select className="border rounded px-3 py-2" value={clientInfo.industry} onChange={(e) => setClientInfo({ ...clientInfo, industry: e.target.value })}>
                <option value="">Select Industry *</option>
                <option value="HVAC">HVAC</option>
                <option value="Plumbing">Plumbing</option>
                <option value="Roofing">Roofing</option>
                <option value="Electrical">Electrical</option>
                <option value="Remodeling">Remodeling/General Contractor</option>
                <option value="Cleaning">Cleaning Services</option>
                <option value="Auto Detailing">Auto Detailing</option>
                <option value="Pet Grooming">Pet Grooming</option>
                <option value="Other">Other</option>
              </select>
              {clientInfo.industry === 'Other' && (
                <input type="text" placeholder="Specify Industry" className="border rounded px-3 py-2" value={clientInfo.industryOther} onChange={(e) => setClientInfo({ ...clientInfo, industryOther: e.target.value })} />
              )}
            </div>
          </div>

          {/* Service Selection */}
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-2xl font-bold mb-4">Service Selection</h2>

            {/* Local SEO Services */}
            <div className="mb-6">
              <h3 className="text-xl font-semibold mb-3 text-blue-600">Local SEO Services</h3>
              <p className="text-sm text-gray-600 mb-3">Select ONE SEO tier (mutually exclusive)</p>
              <div className="space-y-2">
                <label className="flex items-center p-3 border rounded hover:bg-gray-50 cursor-pointer">
                  <input type="checkbox" className="mr-3 w-5 h-5" checked={services.seoStarter} onChange={(e) => setServices({ ...services, seoStarter: e.target.checked, seoMarketLeader: false, seoCityDomination: false, seoRegional: false })} />
                  <span className="flex-1">SEO Starter - Local visibility foundation</span>
                  <span className="font-semibold text-blue-600">$497/month</span>
                </label>
                <label className="flex items-center p-3 border rounded hover:bg-gray-50 cursor-pointer">
                  <input type="checkbox" className="mr-3 w-5 h-5" checked={services.seoMarketLeader} onChange={(e) => setServices({ ...services, seoMarketLeader: e.target.checked, seoStarter: false, seoCityDomination: false, seoRegional: false })} />
                  <span className="flex-1">Market Leader - Competitive dominance</span>
                  <span className="font-semibold text-blue-600">$997/month</span>
                </label>
                <label className="flex items-center p-3 border rounded hover:bg-gray-50 cursor-pointer">
                  <input type="checkbox" className="mr-3 w-5 h-5" checked={services.seoCityDomination} onChange={(e) => setServices({ ...services, seoCityDomination: e.target.checked, seoStarter: false, seoMarketLeader: false, seoRegional: false })} />
                  <span className="flex-1">City Domination - Full market control</span>
                  <span className="font-semibold text-blue-600">$1,497/month</span>
                </label>
                <label className="flex items-center p-3 border rounded hover:bg-gray-50 cursor-pointer">
                  <input type="checkbox" className="mr-3 w-5 h-5" checked={services.seoRegional} onChange={(e) => setServices({ ...services, seoRegional: e.target.checked, seoStarter: false, seoMarketLeader: false, seoCityDomination: false })} />
                  <span className="flex-1">Regional Dominance - Multi-city coverage</span>
                  <span className="font-semibold text-blue-600">Custom Pricing</span>
                </label>
                {services.seoRegional && (
                  <input type="number" placeholder="Enter monthly price" className="ml-8 border rounded px-3 py-2 w-48" value={services.seoRegionalPrice || ''} onChange={(e) => setServices({ ...services, seoRegionalPrice: parseFloat(e.target.value) || 0 })} />
                )}
              </div>
            </div>

            {/* Web Design & Automation */}
            <div className="mb-6">
              <h3 className="text-xl font-semibold mb-3 text-blue-600">Web Design & Automation</h3>
              <p className="text-sm text-gray-600 mb-3">Select any combination</p>
              <div className="space-y-2">
                <label className="flex items-center p-3 border rounded hover:bg-gray-50 cursor-pointer">
                  <input type="checkbox" className="mr-3 w-5 h-5" checked={services.websiteDev} onChange={(e) => setServices({ ...services, websiteDev: e.target.checked })} />
                  <span className="flex-1">Professional Website Development</span>
                  <span className="font-semibold text-green-600">$2,500 one-time</span>
                </label>
                {services.websiteDev && (
                  <input type="number" placeholder="Adjust price if needed" className="ml-8 border rounded px-3 py-2 w-48" value={services.websiteDevPrice} onChange={(e) => setServices({ ...services, websiteDevPrice: parseFloat(e.target.value) || 2500 })} />
                )}
                <label className="flex items-center p-3 border rounded hover:bg-gray-50 cursor-pointer">
                  <input type="checkbox" className="mr-3 w-5 h-5" checked={services.marketingAutomation} onChange={(e) => setServices({ ...services, marketingAutomation: e.target.checked })} />
                  <span className="flex-1">Marketing Automation Platform</span>
                  <span className="font-semibold text-blue-600">$1,500/month</span>
                </label>
                <label className="flex items-center p-3 border rounded hover:bg-gray-50 cursor-pointer">
                  <input type="checkbox" className="mr-3 w-5 h-5" checked={services.businessAutomation} onChange={(e) => setServices({ ...services, businessAutomation: e.target.checked })} />
                  <span className="flex-1">Business Operations Automation</span>
                  <span className="font-semibold text-blue-600">Custom Pricing</span>
                </label>
                {services.businessAutomation && (
                  <input type="number" placeholder="Enter monthly price" className="ml-8 border rounded px-3 py-2 w-48" value={services.businessAutomationPrice || ''} onChange={(e) => setServices({ ...services, businessAutomationPrice: parseFloat(e.target.value) || 0 })} />
                )}
              </div>
            </div>

            {/* Advanced Automation Packages */}
            <div>
              <h3 className="text-xl font-semibold mb-3 text-blue-600">Advanced Automation Packages</h3>
              <p className="text-sm text-gray-600 mb-3">Select ONE package (mutually exclusive)</p>
              <div className="space-y-2">
                <label className="flex items-center p-3 border rounded hover:bg-gray-50 cursor-pointer">
                  <input type="checkbox" className="mr-3 w-5 h-5" checked={services.foundationPackage} onChange={(e) => setServices({ ...services, foundationPackage: e.target.checked, growthPackage: false, enterprisePackage: false })} />
                  <span className="flex-1">Foundation Package - Essential automation suite</span>
                  <span className="font-semibold text-blue-600">$1,500/mo + setup</span>
                </label>
                {services.foundationPackage && (
                  <input type="number" placeholder="Setup fee (default $4,500)" className="ml-8 border rounded px-3 py-2 w-48" value={services.foundationSetupFee} onChange={(e) => setServices({ ...services, foundationSetupFee: parseFloat(e.target.value) || 4500 })} />
                )}
                <label className="flex items-center p-3 border rounded hover:bg-gray-50 cursor-pointer">
                  <input type="checkbox" className="mr-3 w-5 h-5" checked={services.growthPackage} onChange={(e) => setServices({ ...services, growthPackage: e.target.checked, foundationPackage: false, enterprisePackage: false })} />
                  <span className="flex-1">Growth Package - Advanced automation & AI</span>
                  <span className="font-semibold text-blue-600">$3,000/mo + setup</span>
                </label>
                {services.growthPackage && (
                  <input type="number" placeholder="Setup fee (default $7,500)" className="ml-8 border rounded px-3 py-2 w-48" value={services.growthSetupFee} onChange={(e) => setServices({ ...services, growthSetupFee: parseFloat(e.target.value) || 7500 })} />
                )}
                <label className="flex items-center p-3 border rounded hover:bg-gray-50 cursor-pointer">
                  <input type="checkbox" className="mr-3 w-5 h-5" checked={services.enterprisePackage} onChange={(e) => setServices({ ...services, enterprisePackage: e.target.checked, foundationPackage: false, growthPackage: false })} />
                  <span className="flex-1">Enterprise Package - Full automation transformation</span>
                  <span className="font-semibold text-blue-600">Custom monthly + $15,000 setup</span>
                </label>
                {services.enterprisePackage && (
                  <div className="ml-8 space-y-2">
                    <input type="number" placeholder="Enter monthly fee" className="border rounded px-3 py-2 w-48" value={services.enterpriseMonthlyFee} onChange={(e) => setServices({ ...services, enterpriseMonthlyFee: parseFloat(e.target.value) || 6000 })} />
                    <input type="number" placeholder="Setup fee (default $15,000)" className="border rounded px-3 py-2 w-48" value={services.enterpriseSetupFee} onChange={(e) => setServices({ ...services, enterpriseSetupFee: parseFloat(e.target.value) || 15000 })} />
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Territory Information (only if SEO selected) */}
          {isSEOSelected && (
            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
              <h2 className="text-2xl font-bold mb-4">Territory Information</h2>
              <p className="text-sm text-gray-600 mb-4">Define your exclusive service territory for SEO protection</p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <input type="text" placeholder="Primary City *" className="border rounded px-3 py-2" value={territory.primaryCity} onChange={(e) => setTerritory({ ...territory, primaryCity: e.target.value })} />
                <input type="text" placeholder="State *" className="border rounded px-3 py-2" value={territory.state} onChange={(e) => setTerritory({ ...territory, state: e.target.value })} />
                <input type="text" placeholder="ZIP Codes (comma-separated)" className="border rounded px-3 py-2 md:col-span-2" value={territory.zipCodes} onChange={(e) => setTerritory({ ...territory, zipCodes: e.target.value })} />
                <input type="text" placeholder="Boroughs/Districts (if applicable)" className="border rounded px-3 py-2 md:col-span-2" value={territory.boroughsDistricts} onChange={(e) => setTerritory({ ...territory, boroughsDistricts: e.target.value })} />
              </div>
            </div>
          )}

          {/* Contract Terms */}
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-2xl font-bold mb-4">Contract Terms</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Start Date *</label>
                <input type="date" className="border rounded px-3 py-2 w-full" value={contractTerms.startDate} onChange={(e) => setContractTerms({ ...contractTerms, startDate: e.target.value })} />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Contract Type *</label>
                <select className="border rounded px-3 py-2 w-full" value={contractTerms.contractType} onChange={(e) => setContractTerms({ ...contractTerms, contractType: e.target.value })}>
                  <option value="month-to-month">Month-to-Month</option>
                  <option value="3-months">3-Month Agreement</option>
                  <option value="6-months">6-Month Agreement</option>
                  <option value="12-months">12-Month Agreement</option>
                </select>
              </div>
              {contractTerms.contractType !== 'month-to-month' && (
                <div>
                  <label className="block text-sm font-medium mb-1">End Date (auto-calculated)</label>
                  <input type="date" className="border rounded px-3 py-2 w-full bg-gray-100" value={contractTerms.endDate} readOnly />
                </div>
              )}
              <div>
                <label className="block text-sm font-medium mb-1">Payment Due Day *</label>
                <select className="border rounded px-3 py-2 w-full" value={contractTerms.paymentDueDay} onChange={(e) => setContractTerms({ ...contractTerms, paymentDueDay: e.target.value })}>
                  <option value="1st">1st of the month</option>
                  <option value="15th">15th of the month</option>
                </select>
              </div>
            </div>
          </div>

          {/* Special Terms */}
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-2xl font-bold mb-4">Special Terms & Conditions</h2>
            <textarea placeholder="Add any special terms, discounts, or custom conditions..." className="border rounded px-3 py-2 w-full h-32" value={specialTerms} onChange={(e) => setSpecialTerms(e.target.value)} />
          </div>

          {/* Pricing Summary at Bottom */}
          <div className="bg-blue-50 rounded-lg shadow-md p-6 mb-6 border-2 border-blue-200">
            <h2 className="text-2xl font-bold mb-4">Pricing Summary</h2>
            <div className="space-y-2 text-lg">
              <div className="flex justify-between font-semibold"><span>Monthly Recurring:</span><span className="text-blue-600">${pricing.monthlyTotal.toFixed(2)}</span></div>
              <div className="flex justify-between font-semibold"><span>One-Time Setup/Fees:</span><span className="text-blue-600">${pricing.oneTimeTotal.toFixed(2)}</span></div>
              <div className="flex justify-between text-xl font-bold border-t-2 border-blue-300 pt-2 mt-2"><span>FIRST PAYMENT DUE:</span><span className="text-blue-700">${pricing.firstPayment.toFixed(2)}</span></div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-4 mb-6">
            <button onClick={() => setShowPreview(!showPreview)} className="flex-1 bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700">
              {showPreview ? 'Hide Preview' : 'Preview Contract'}
            </button>
            <button onClick={handlePrint} className="flex-1 bg-green-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-green-700">Print / Save as PDF</button>
            <button onClick={clearForm} className="bg-gray-300 text-gray-700 px-6 py-3 rounded-lg font-semibold hover:bg-gray-400">Clear Form</button>
          </div>

          {/* Preview Section */}
          {showPreview && (
            <div className="bg-white rounded-lg shadow-md p-8 mb-6">
              <h2 className="text-3xl font-bold mb-6 text-center">CONTRACT PREVIEW</h2>
              <ContractDocument
                clientInfo={clientInfo}
                services={services}
                territory={territory}
                contractTerms={contractTerms}
                specialTerms={specialTerms}
                pricing={pricing}
                isSEOSelected={isSEOSelected}
              />
            </div>
          )}
        </div>
      </div>

      {/* Print View */}
      <div className="hidden print:block">
        <ContractDocument
          clientInfo={clientInfo}
          services={services}
          territory={territory}
          contractTerms={contractTerms}
          specialTerms={specialTerms}
          pricing={pricing}
          isSEOSelected={isSEOSelected}
        />
      </div>
    </div>
  );
}
