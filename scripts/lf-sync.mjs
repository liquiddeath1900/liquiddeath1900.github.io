#!/usr/bin/env node
/**
 * Local Falcon → Supabase Sync
 * Fetches latest campaign report via MCP SSE and saves to Supabase.
 * Run: node lf-sync.mjs [--run-campaign]
 */

const LF_API_KEY = 'e1f852bd19131d0be43892072caf7de8';
const CAMPAIGN_KEY = 'aec26b9aaa8f068';
const SUPABASE_URL = 'https://ytwfjflhgengnxgfzghz.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl0d2ZqZmxoZ2VuZ254Z2Z6Z2h6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU4MzQ2OTgsImV4cCI6MjA4MTQxMDY5OH0.2hYFyS6eZjKxfnAAyfjZ4wUKRor6T9K_dB4jdIs81y8';
const MCP_BASE = 'https://mcp.localfalcon.com';
const DOMAIN = 'seamlessflow.ai';

let msgId = 0;

async function main() {
  const runCampaign = process.argv.includes('--run-campaign');
  console.log(`[${new Date().toISOString()}] Local Falcon sync starting...`);

  try {
    // Connect to SSE
    console.log('Connecting to MCP SSE...');
    const response = await fetch(`${MCP_BASE}/sse`, {
      headers: { 'Authorization': `Bearer ${LF_API_KEY}` }
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    let sessionUrl = null;
    let initialized = false;
    let step = 0; // 0=waiting for session, 1=init sent, 2=campaign run sent, 3=report requested

    const timeout = setTimeout(() => {
      console.error('TIMEOUT after 45s');
      reader.cancel();
      process.exit(1);
    }, 45000);

    while (true) {
      const { done, value } = await reader.read();
      if (done) { console.log('Stream ended'); break; }

      buffer += decoder.decode(value, { stream: true });

      // Process complete lines one at a time
      while (buffer.includes('\n')) {
        const idx = buffer.indexOf('\n');
        const line = buffer.slice(0, idx);
        buffer = buffer.slice(idx + 1);

        if (line.startsWith('data: ')) {
          const data = line.slice(6).trim();

          // Step 0: Get session URL from endpoint event
          if (!sessionUrl && data.startsWith('/sse/messages')) {
            sessionUrl = data;
            console.log('Session established, initializing...');
            const id = ++msgId;
            await fetch(`${MCP_BASE}${sessionUrl}`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                jsonrpc: '2.0', id,
                method: 'initialize',
                params: {
                  protocolVersion: '2024-11-05',
                  capabilities: {},
                  clientInfo: { name: 'lf-sync', version: '1.0' }
                }
              })
            });
            step = 1;
            continue;
          }

          // Parse JSON messages
          if (!sessionUrl) continue;
          let msg;
          try { msg = JSON.parse(data); } catch { continue; }

          // Step 1: After init response
          if (msg.id === 1 && step === 1) {
            initialized = true;

            if (runCampaign) {
              console.log('Triggering campaign run...');
              const id = ++msgId;
              await fetch(`${MCP_BASE}${sessionUrl}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  jsonrpc: '2.0', id,
                  method: 'tools/call',
                  params: { name: 'runLocalFalconCampaign', arguments: { reportKey: CAMPAIGN_KEY } }
                })
              });
              step = 2;
            } else {
              // Skip campaign run, go straight to report fetch
              console.log('Fetching campaign report...');
              const id = ++msgId;
              await fetch(`${MCP_BASE}${sessionUrl}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  jsonrpc: '2.0', id,
                  method: 'tools/call',
                  params: {
                    name: 'getLocalFalconCampaignReport',
                    arguments: {
                      reportKey: CAMPAIGN_KEY,
                      fieldmask: 'report_key,name,arp,atrp,solv,grid_size,last_run,run_data'
                    }
                  }
                })
              });
              step = 3;
            }
            continue;
          }

          // Step 2: After campaign run response (if --run-campaign)
          if (step === 2 && msg.id === 2) {
            console.log('Campaign triggered, waiting 120s for scans...');
            await new Promise(r => setTimeout(r, 120000));
            console.log('Fetching campaign report...');
            const id = ++msgId;
            await fetch(`${MCP_BASE}${sessionUrl}`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                jsonrpc: '2.0', id,
                method: 'tools/call',
                params: {
                  name: 'getLocalFalconCampaignReport',
                  arguments: {
                    reportKey: CAMPAIGN_KEY,
                    fieldmask: 'report_key,name,arp,atrp,solv,grid_size,last_run,run_data'
                  }
                }
              })
            });
            step = 3;
            continue;
          }

          // Step 3: Got campaign report
          if (step === 3 && msg.result) {
            clearTimeout(timeout);
            reader.cancel();

            // Check for errors
            if (msg.result.isError) {
              console.error('MCP error:', msg.result.content?.[0]?.text);
              process.exit(1);
            }

            // Parse result
            const text = msg.result.content?.[0]?.text;
            if (!text) { console.error('Empty result'); process.exit(1); }

            let reportData;
            try { reportData = JSON.parse(text); } catch {
              console.log('Non-JSON response:', text.slice(0, 200));
              process.exit(1);
            }

            const d = reportData.data;
            const scanDate = d.run_data?.run || new Date().toISOString().split('T')[0];
            const scans = d.run_data?.scans || [];
            const gridSize = d.grid_size || '5';
            const rows = scans.map(scan => {
              const arp = parseFloat(scan.arp) || 21;
              const atrp = parseFloat(scan.atrp) || 21;
              const solv = parseFloat(scan.solv) || 0;
              return {
                domain: DOMAIN,
                keyword: scan.keyword || 'unknown',
                location: scan.location?.name || 'NYC',
                grid_size: `${gridSize}x${gridSize}`,
                avg_rank: arp,
                top_3_pct: solv,
                top_10_pct: arp <= 10 ? 100 : 0,
                not_ranking_pct: arp >= 21 ? 100 : 0,
                scan_date: scanDate,
                raw_data: scan
              };
            });

            if (rows.length === 0) {
              console.log('No scans in report. Raw keys:', Object.keys(reportData?.data || reportData || {}));
              process.exit(1);
            }

            console.log(`Parsed ${rows.length} scans, saving to Supabase...`);
            console.log('Sample row:', JSON.stringify(rows[0]).slice(0, 300));
            const res = await fetch(`${SUPABASE_URL}/rest/v1/local_rankings`, {
              method: 'POST',
              headers: {
                'apikey': SUPABASE_KEY,
                'Authorization': `Bearer ${SUPABASE_KEY}`,
                'Content-Type': 'application/json',
                'Prefer': 'return=representation'
              },
              body: JSON.stringify(rows)
            });
            console.log('Supabase status:', res.status);
            const saved = await res.json();
            if (res.status >= 400) {
              console.error('Supabase error:', JSON.stringify(saved));
              process.exit(1);
            }
            console.log(`Done! Saved ${Array.isArray(saved) ? saved.length : 0} rows.`);
            process.exit(0);
          }
        }
      }
    }
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

main();
