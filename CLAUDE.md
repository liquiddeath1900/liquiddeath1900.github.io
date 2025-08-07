# seamlessflow.ai Development Profile

## Business
Multi-service digital agency: **Automation • SEO • Cybersecurity • Voice Agents**

## Learning Status
Building coding skills while delivering client projects. **Explain all code and tool choices thoroughly.**

## Core Tech Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+, responsive, modern)
- **Backend:** Python (automation, scripting, security tools)
- **Version Control:** Git/GitHub (collaboration, project management)
- **Runtime:** Node.js/npm (package management, build tools)

## Automation Arsenal

### AUTOMATION TOOLS:
- n8n (primary - visual + code, AI agents, cost-effective)
- Voiceflow (voice agents, conversational AI, client demos)
- Playwright (browser automation, testing, scraping, SEO auditing)
- Firecrawl (competitor analysis, bulk site crawling, content research)
- Context-7 (advanced data analysis, SEO reporting, performance tracking)
- Selenium (web automation backup)
- Zapier/Make.com integration knowledge
- API integrations and webhooks

### Primary Tools
```yaml
# TOOL SELECTION HIERARCHY
Primary: n8n              # Visual + code, AI agents, cost-effective
Voice: Voiceflow          # Conversational AI, client demos
Testing: Playwright       # Modern browser automation
Scraping: Firecrawl       # Bulk site crawling, competitor analysis
Analytics: Context-7      # Advanced data analysis, SEO reporting
Backup: Selenium          # Legacy web automation support
Integrations: Zapier/Make # Client existing workflows
```

### n8n (Primary Automation Platform)
```javascript
// WHY n8n: Visual workflow builder + custom code nodes
// BUSINESS VALUE: Clients can see/modify workflows, reduces costs
// WHEN TO USE: Complex multi-step automations, AI integrations

// Example: Lead qualification workflow
const qualifyLead = {
  trigger: 'webhook',           // Form submission
  steps: [
    'validateInput',            // Clean/verify data
    'enrichWithLinkedIn',       // Company research
    'scoreWithAI',              // GPT-based qualification
    'routeToSales',             // Assign to rep
    'updateCRM'                 // Log in database
  ]
};
```

### Voiceflow (Voice Agent Platform)
```javascript
// WHY Voiceflow: Drag-drop voice flows, easy client demos
// BUSINESS VALUE: Voice agents for customer service, sales
// WHEN TO USE: Conversational interfaces, phone automation

const voiceAgentFlow = {
  intent: 'customer_support',
  response: 'How can I help you today?',
  actions: [
    'capture_issue_type',       // Route to department
    'check_account_status',     // API call to CRM
    'provide_solution',         // Knowledge base lookup
    'escalate_if_needed'        // Transfer to human
  ]
};
```

### Playwright (Modern Browser Automation)
```python
# WHY Playwright: Fast, reliable, modern browser support
# BUSINESS VALUE: SEO audits, competitor analysis, testing
# WHEN TO USE: Modern websites, JavaScript-heavy sites

from playwright.async_api import async_playwright

async def audit_competitor_seo(url):
    """
    PURPOSE: Extract SEO data from competitor sites
    BUSINESS VALUE: Helps clients outrank competition
    PERFORMANCE: 3x faster than Selenium, handles SPAs
    """
    async with async_playwright() as p:
        # Launch browser (headless for production)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # Navigate and wait for content
            await page.goto(url, wait_until='networkidle')
            
            # Extract SEO elements
            seo_data = await page.evaluate("""
                () => ({
                    title: document.title,
                    meta_description: document.querySelector('meta[name="description"]')?.content,
                    h1_tags: Array.from(document.querySelectorAll('h1')).map(h => h.textContent),
                    internal_links: document.querySelectorAll('a[href^="/"]').length,
                    images_without_alt: document.querySelectorAll('img:not([alt])').length
                })
            """)
            
            return seo_data
            
        except Exception as e:
            logger.error(f"SEO audit failed for {url}: {e}")
            return {'error': 'Unable to audit site'}
        finally:
            await browser.close()
```

## SEO Tools & Workflows

### Google APIs Integration
```python
# GOOGLE ANALYTICS/SEARCH CONSOLE: Official APIs for data access
# BUSINESS VALUE: Automated reporting, performance tracking
# WHEN TO USE: Client dashboards, monthly reports

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.oauth2.service_account import Credentials

class SEOAnalytics:
    def __init__(self, credentials_path):
        """
        PURPOSE: Automated SEO reporting and monitoring
        SETUP: Requires Google Cloud project + service account
        """
        self.credentials = Credentials.from_service_account_file(credentials_path)
        self.analytics_client = BetaAnalyticsDataClient(credentials=self.credentials)
    
    def get_organic_traffic(self, property_id, start_date, end_date):
        # Fetch organic search traffic data
        request = {
            'property': f'properties/{property_id}',
            'date_ranges': [{'start_date': start_date, 'end_date': end_date}],
            'metrics': [{'name': 'sessions'}, {'name': 'users'}],
            'dimensions': [{'name': 'sessionDefaultChannelGroup'}],
            'dimension_filter': {
                'filter': {
                    'field_name': 'sessionDefaultChannelGroup',
                    'string_filter': {'value': 'Organic Search'}
                }
            }
        }
        
        response = self.analytics_client.run_report(request)
        return self.process_analytics_data(response)
```

### Performance Monitoring
```javascript
// LIGHTHOUSE CI: Automated performance audits
// BUSINESS VALUE: Track Core Web Vitals, SEO scores
// WHEN TO USE: After site changes, monthly monitoring

const lighthouse = require('lighthouse');
const chromeLauncher = require('chrome-launcher');

async function auditWebsitePerformance(url) {
    // Launch Chrome instance
    const chrome = await chromeLauncher.launch({chromeFlags: ['--headless']});
    
    // Run Lighthouse audit
    const options = {
        logLevel: 'info',
        output: 'json',
        onlyCategories: ['performance', 'seo', 'accessibility'],
        port: chrome.port,
    };
    
    const runnerResult = await lighthouse(url, options);
    await chrome.kill();
    
    // Extract key metrics
    const metrics = {
        performance_score: runnerResult.lhr.categories.performance.score * 100,
        seo_score: runnerResult.lhr.categories.seo.score * 100,
        first_contentful_paint: runnerResult.lhr.audits['first-contentful-paint'].numericValue,
        largest_contentful_paint: runnerResult.lhr.audits['largest-contentful-paint'].numericValue,
        core_web_vitals_passed: runnerResult.lhr.audits['core-web-vitals'].score === 1
    };
    
    return metrics;
}
```

## Cybersecurity Tools

### Vulnerability Scanning
```python
# PYTHON-NMAP: Network vulnerability scanning
# BUSINESS VALUE: Security audits, compliance reporting
# WHEN TO USE: Initial security assessments, monthly scans

import nmap
import requests
from urllib.parse import urljoin

class SecurityAuditor:
    def __init__(self):
        self.nm = nmap.PortScanner()
        
    def scan_network_ports(self, target):
        """
        PURPOSE: Identify open ports and services
        BUSINESS VALUE: Find potential security vulnerabilities
        SECURITY: Only scan systems you own/have permission for
        """
        try:
            # Scan common ports
            self.nm.scan(target, '22-443,3306,5432,27017')
            
            results = {}
            for host in self.nm.all_hosts():
                results[host] = {
                    'state': self.nm[host].state(),
                    'open_ports': [],
                    'services': {}
                }
                
                for port in self.nm[host]['tcp'].keys():
                    if self.nm[host]['tcp'][port]['state'] == 'open':
                        results[host]['open_ports'].append(port)
                        results[host]['services'][port] = self.nm[host]['tcp'][port]['name']
            
            return results
            
        except Exception as e:
            logger.error(f"Network scan failed: {e}")
            return {'error': 'Scan failed'}
    
    def check_ssl_certificate(self, domain):
        """
        PURPOSE: Validate SSL certificate security
        BUSINESS VALUE: Prevent security warnings, maintain trust
        """
        import ssl
        import socket
        from datetime import datetime
        
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Check expiration
                    expiry_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_until_expiry = (expiry_date - datetime.now()).days
                    
                    return {
                        'valid': True,
                        'expires_in_days': days_until_expiry,
                        'issuer': cert['issuer'],
                        'subject': cert['subject']
                    }
                    
        except Exception as e:
            return {'valid': False, 'error': str(e)}
```

## Advanced Integrations

### MCP (Model Context Protocol)
```python
# MCP: Live system connections for AI agents
# BUSINESS VALUE: AI agents can access real-time data
# WHEN TO USE: AI-powered automation with live data needs

from mcp import create_server, types

class MCPSystemConnector:
    """
    PURPOSE: Connect AI agents to live business systems
    BUSINESS VALUE: Real-time data access for AI workflows
    SECURITY: Implement proper authentication and rate limiting
    """
    
    def __init__(self):
        self.server = create_server("business-systems")
        self.setup_tools()
    
    def setup_tools(self):
        @self.server.call_tool()
        async def get_customer_data(customer_id: str):
            # Connect to CRM system
            customer = await self.crm_client.get_customer(customer_id)
            return {
                'name': customer.name,
                'status': customer.status,
                'last_contact': customer.last_contact_date,
                'lifetime_value': customer.total_purchases
            }
        
        @self.server.call_tool()
        async def update_inventory(product_id: str, quantity: int):
            # Update inventory system
            result = await self.inventory_client.update_stock(product_id, quantity)
            return {'success': result.success, 'new_quantity': result.current_stock}
```

### Semantic Reader MCPs
```python
# SEMANTIC READER: Advanced document analysis and understanding
# BUSINESS VALUE: Extract insights from client documents, contracts, reports
# WHEN TO USE: PDF analysis, document workflows, knowledge extraction

from mcp_semantic_reader import SemanticReader
import asyncio

class DocumentAnalyzer:
    """
    PURPOSE: Intelligent document processing for client automation
    BUSINESS VALUE: Convert unstructured docs into actionable data
    TOOLS: PDF parsing, semantic search, persistent memory
    """
    
    def __init__(self):
        self.semantic_reader = SemanticReader()
        self.memory_store = {}  # Persistent document memory
    
    async def analyze_contract(self, pdf_path, client_id):
        """
        PURPOSE: Extract key terms, dates, obligations from contracts
        BUSINESS VALUE: Automate contract review, deadline tracking
        PERFORMANCE: Processes 100-page docs in <10 seconds
        """
        try:
            # Read and parse PDF with semantic understanding
            document = await self.semantic_reader.read_pdf(pdf_path)
            
            # Extract structured data using AI
            contract_data = await self.semantic_reader.extract_entities(
                document.content,
                entity_types=[
                    'contract_parties',
                    'key_dates', 
                    'payment_terms',
                    'obligations',
                    'termination_clauses'
                ]
            )
            
            # Store in persistent memory for future reference
            self.memory_store[f"{client_id}_contract"] = {
                'content': document.content,
                'entities': contract_data,
                'processed_date': datetime.now(),
                'document_hash': document.hash
            }
            
            # Generate actionable insights
            insights = await self.generate_contract_insights(contract_data)
            
            return {
                'success': True,
                'entities': contract_data,
                'insights': insights,
                'memory_key': f"{client_id}_contract"
            }
            
        except Exception as e:
            logger.error(f"Contract analysis failed: {e}")
            return {'success': False, 'error': 'Document processing failed'}
    
    async def semantic_search_documents(self, query, client_id):
        """
        PURPOSE: Search across all client documents using natural language
        BUSINESS VALUE: Instant answers from document libraries
        """
        # Search persistent memory for relevant documents
        relevant_docs = await self.semantic_reader.search(
            query=query,
            documents=self.get_client_documents(client_id),
            similarity_threshold=0.8
        )
        
        return {
            'query': query,
            'results': relevant_docs,
            'context': self.build_answer_context(relevant_docs)
        }
```

### Claude Usage Monitor MCP
```python
# CLAUDE USAGE MONITOR: Real-time cost tracking and session monitoring
# BUSINESS VALUE: Control AI costs, optimize usage, client billing accuracy
# WHEN TO USE: Production automations, client billing, budget management

from mcp_claude_monitor import ClaudeMonitor
import asyncio
from datetime import datetime, timedelta

class AIUsageTracker:
    """
    PURPOSE: Monitor and optimize Claude API usage across all automations
    BUSINESS VALUE: Prevent cost overruns, accurate client billing
    MONITORING: Real-time costs, session tracking, usage patterns
    """
    
    def __init__(self, budget_limits=None):
        self.monitor = ClaudeMonitor()
        self.budget_limits = budget_limits or {}
        self.session_data = {}
        
    async def start_tracked_session(self, client_id, workflow_name):
        """
        PURPOSE: Begin monitoring AI usage for specific client workflow
        BUSINESS VALUE: Track costs per client, per automation
        """
        session_id = f"{client_id}_{workflow_name}_{datetime.now().isoformat()}"
        
        self.session_data[session_id] = {
            'client_id': client_id,
            'workflow_name': workflow_name,
            'start_time': datetime.now(),
            'total_tokens': 0,
            'total_cost': 0.0,
            'request_count': 0,
            'model_usage': {}
        }
        
        return session_id
    
    async def track_claude_request(self, session_id, model, input_tokens, output_tokens):
        """
        PURPOSE: Log individual Claude API calls with cost calculation
        BUSINESS VALUE: Granular cost tracking, optimization insights
        """
        if session_id not in self.session_data:
            raise ValueError("Session not found")
        
        # Calculate costs based on current Claude pricing
        cost_per_input_token = self.get_model_pricing(model, 'input')
        cost_per_output_token = self.get_model_pricing(model, 'output')
        
        request_cost = (input_tokens * cost_per_input_token) + (output_tokens * cost_per_output_token)
        
        # Update session data
        session = self.session_data[session_id]
        session['total_tokens'] += (input_tokens + output_tokens)
        session['total_cost'] += request_cost
        session['request_count'] += 1
        
        if model not in session['model_usage']:
            session['model_usage'][model] = {'requests': 0, 'cost': 0.0}
        
        session['model_usage'][model]['requests'] += 1
        session['model_usage'][model]['cost'] += request_cost
        
        # Check budget limits
        await self.check_budget_alerts(session_id)
        
        return {
            'session_cost': session['total_cost'],
            'request_cost': request_cost,
            'budget_remaining': self.get_remaining_budget(session['client_id'])
        }
    
    async def get_usage_report(self, client_id, date_range=None):
        """
        PURPOSE: Generate detailed usage reports for client billing
        BUSINESS VALUE: Transparent billing, usage optimization insights
        """
        if not date_range:
            date_range = (datetime.now() - timedelta(days=30), datetime.now())
        
        # Aggregate usage data for time period
        client_sessions = [
            session for session in self.session_data.values()
            if session['client_id'] == client_id and 
            date_range[0] <= session['start_time'] <= date_range[1]
        ]
        
        total_cost = sum(session['total_cost'] for session in client_sessions)
        total_requests = sum(session['request_count'] for session in client_sessions)
        
        # Workflow breakdown
        workflow_costs = {}
        for session in client_sessions:
            workflow = session['workflow_name']
            if workflow not in workflow_costs:
                workflow_costs[workflow] = 0
            workflow_costs[workflow] += session['total_cost']
        
        return {
            'client_id': client_id,
            'date_range': date_range,
            'total_cost': total_cost,
            'total_requests': total_requests,
            'workflow_breakdown': workflow_costs,
            'cost_per_request': total_cost / total_requests if total_requests > 0 else 0,
            'recommendations': await self.generate_optimization_recommendations(client_sessions)
        }
    
    def get_model_pricing(self, model, token_type):
        """Current Claude pricing per token (update as needed)"""
        pricing = {
            'claude-3-haiku': {'input': 0.00000025, 'output': 0.00000125},
            'claude-3-sonnet': {'input': 0.000003, 'output': 0.000015},
            'claude-3-opus': {'input': 0.000015, 'output': 0.000075}
        }
        return pricing.get(model, {}).get(token_type, 0)
```

### Database Connections
```python
# DATABASE: PostgreSQL/MySQL connections for automation
# BUSINESS VALUE: Store automation results, track performance
# WHEN TO USE: Data persistence, reporting, complex queries

import asyncpg
import mysql.connector
from contextlib import asynccontextmanager

class DatabaseManager:
    def __init__(self, db_type='postgresql'):
        self.db_type = db_type
        self.connection_pool = None
    
    async def init_postgres_pool(self, database_url):
        """
        PURPOSE: Efficient database connections for automation
        BUSINESS VALUE: Fast data access, connection reuse
        """
        self.connection_pool = await asyncpg.create_pool(database_url)
    
    @asynccontextmanager
    async def get_connection(self):
        """Context manager for safe database operations"""
        async with self.connection_pool.acquire() as connection:
            try:
                yield connection
            except Exception as e:
                await connection.execute("ROLLBACK")
                raise e
    
    async def log_automation_result(self, workflow_name, status, data):
        """
        PURPOSE: Track automation performance and results
        BUSINESS VALUE: Monitor success rates, debug failures
        """
        async with self.get_connection() as conn:
            await conn.execute("""
                INSERT INTO automation_logs (workflow_name, status, data, created_at)
                VALUES ($1, $2, $3, NOW())
            """, workflow_name, status, data)
```

## Tool Selection Guide

### When to Use Each Automation Tool
```yaml
n8n:
  use_when:
    - Complex multi-step workflows
    - AI/LLM integrations needed
    - Client wants to see/modify process
    - Cost-effective solution required
  avoid_when:
    - Simple one-off tasks
    - Real-time performance critical

Playwright:
  use_when:
    - Modern websites (React, Vue, Angular)
    - JavaScript-heavy applications
    - Need reliable element detection
    - Performance testing required
  avoid_when:
    - Simple form submissions
    - Legacy websites work fine with Selenium

Voiceflow:
  use_when:
    - Voice/chat interfaces needed
    - Client wants demo-friendly tool
    - Conversational AI required
    - Non-technical client management
  avoid_when:
    - Text-only automation
    - Complex business logic required

Selenium:
  use_when:
    - Legacy website compatibility
    - Existing Selenium infrastructure
    - Specific browser version testing
  avoid_when:
    - Modern websites available
    - Performance is critical
```

## Coding Standards

### Project Structure
```
project-name/
├── src/
│   ├── automation/         # n8n workflows, Python scripts
│   ├── web/               # HTML/CSS/JavaScript
│   ├── voice/             # Voiceflow exports
│   └── security/          # Security audit scripts
├── config/
│   ├── env.example        # Environment variables template
│   └── database.sql       # Database schema
├── tests/
│   ├── automation/        # Workflow tests
│   └── integration/       # API tests
├── docs/
│   ├── setup.md          # Installation instructions
│   └── workflows.md      # Process documentation
├── package.json          # Node.js dependencies
├── requirements.txt      # Python dependencies
└── README.md            # Project overview
```

### Code Quality Standards
```python
# REQUIRED: Every function needs this structure
def automation_function(parameters):
    """
    PURPOSE: What this function accomplishes
    BUSINESS VALUE: Why client needs this
    TOOL CHOICE: Why we selected this approach
    PERFORMANCE: Expected execution time/resources
    SECURITY: What protections are in place
    """
    try:
        # Step 1: Validate inputs (prevent security issues)
        validated_data = validate_inputs(parameters)
        
        # Step 2: Execute main logic (with progress logging)
        result = perform_main_operation(validated_data)
        
        # Step 3: Handle success response
        logger.info(f"Automation completed successfully: {result}")
        return {'success': True, 'data': result}
        
    except ValidationError as e:
        logger.error(f"Input validation failed: {e}")
        return {'success': False, 'error': 'Invalid input data'}
    except Exception as e:
        logger.error(f"Automation failed: {e}")
        return {'success': False, 'error': 'Process failed'}
```

### Performance Targets
- **n8n Workflows:** <30 seconds execution time
- **Web Scraping:** <5 seconds per page (Playwright)
- **API Responses:** <2 seconds response time
- **Database Queries:** <1 second for standard operations
- **Voice Agents:** <3 seconds response time

### TODO Template
```markdown
## After Every Code Delivery:
- [ ] Test automation workflow end-to-end
- [ ] Check error handling with invalid inputs
- [ ] Verify performance meets target times
- [ ] Run security scan (input validation, XSS prevention)
- [ ] Update documentation with new features
- [ ] Commit code with descriptive message
- [ ] Deploy to staging environment
- [ ] Schedule client demo/walkthrough

## Next Steps:
- [ ] Scale workflow for higher volume
- [ ] Add monitoring and alerting  
- [ ] Integrate with client's existing systems
- [ ] Create user training materials
```

## Communication Protocol
**Direct approach:** Show file structure → Write code → Explain choices → Add TODOs
- Focus on business impact and ROI
- Explain tool selection rationale
- Provide ready-to-deploy solutions
- Include performance metrics and security measures
- Always explain when to use each tool vs alternatives

**Code explanation format:**
1. **What:** High-level purpose and outcome
2. **Why:** Business value and client benefit  
3. **How:** Technical implementation details
4. **Tool Choice:** Why this tool vs alternatives
5. **Security:** What protections are included
6. **Performance:** Expected speed and resource usage
7. **Next Steps:** How to scale or improve