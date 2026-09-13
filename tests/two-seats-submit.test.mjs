import test from 'node:test';
import assert from 'node:assert/strict';
import { createApplicationHandler } from '../netlify/functions/two-seats-submit.mjs';

const valid = {
  'form-name': 'pkfit-two-seats-2026', state: 'Louisiana', 'full-name': 'Test Applicant', city: 'Baton Rouge',
  'preferred-contact': 'email', 'primary-contact': 'test@example.com', 'adult-confirmation': 'yes',
  goal: 'Build a consistent training structure.', 'prior-barrier': 'Schedule drift.',
  'commitment-evidence': 'I kept three weekly sessions for six months.', 'training-access': 'Local gym.',
  'reliable-days': '4', 'schedule-constraint': 'Work travel once monthly.', 'current-coach': 'no',
  'weekly-checkins': 'yes', 'public-checkpoints': 'yes', 'identity-format': 'first-name-last-initial',
  'safety-gate': 'clear', 'health-screen-agreement': 'yes', 'terms-agreement': 'yes',
  'typed-signature': 'Test Applicant', 'bot-field': ''
};

function request(fields=valid, method='POST') {
  return new Request('https://operatefitness.app/api/two-seats/apply', {
    method,
    headers: {'content-type': 'application/x-www-form-urlencoded'},
    body: method === 'POST' ? new URLSearchParams(fields) : undefined
  });
}

test('forwards one valid submission before the server deadline', async () => {
  let forwarded;
  const handler = createApplicationHandler({now: () => Date.parse('2026-09-14T12:00:00Z'), forward: async body => {forwarded=body; return new Response('', {status: 200});}});
  const response = await handler(request());
  assert.equal(response.status, 303);
  assert.equal(response.headers.get('location'), '/two-seats/success.html');
  assert.equal(forwarded.get('form-name'), 'pkfit-two-seats-2026');
});

test('rejects a submission at or after the server deadline', async () => {
  let calls=0;
  const handler = createApplicationHandler({now: () => Date.parse('2026-09-15T01:00:00Z'), forward: async () => {calls++; return new Response('', {status: 200});}});
  const response = await handler(request());
  assert.equal(response.status, 410);
  assert.equal(calls, 0);
});

test('validates the contact against the selected route', async () => {
  const fields={...valid, 'primary-contact':'not-an-email'};
  const handler=createApplicationHandler({now:()=>Date.parse('2026-09-14T12:00:00Z'),forward:async()=>new Response('',{status:200})});
  assert.equal((await handler(request(fields))).status,400);
});

test('silently accepts honeypot traffic without forwarding', async () => {
  let calls=0;
  const handler=createApplicationHandler({now:()=>Date.parse('2026-09-14T12:00:00Z'),forward:async()=>{calls++;return new Response('',{status:200})}});
  const response=await handler(request({...valid,'bot-field':'spam'}));
  assert.equal(response.status,202);
  assert.equal(calls,0);
});

test('rejects non-POST methods', async () => {
  const handler=createApplicationHandler({now:()=>0,forward:async()=>new Response('',{status:200})});
  assert.equal((await handler(request(valid,'GET'))).status,405);
});
