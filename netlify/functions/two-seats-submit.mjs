const DEADLINE = Date.parse('2026-09-15T01:00:00Z');
const FORM_NAME = 'pkfit-two-seats-2026';
const REQUIRED = [
  'full-name','city','preferred-contact','primary-contact','adult-confirmation','goal','prior-barrier',
  'commitment-evidence','training-access','reliable-days','schedule-constraint','current-coach',
  'weekly-checkins','safety-gate','health-screen-agreement',
  'terms-agreement','typed-signature'
];
const ALLOWED = new Set(['form-name','state','bot-field',...REQUIRED]);
const MAX_BODY = 64 * 1024;

const reply = (status, text, headers={}) => new Response(text, {
  status,
  headers: {'content-type':'text/plain; charset=utf-8','cache-control':'no-store','x-content-type-options':'nosniff',...headers}
});

function cleanBody(raw) {
  const source = new URLSearchParams(raw);
  const body = new URLSearchParams();
  for (const [key,value] of source) if (ALLOWED.has(key)) body.set(key,String(value).trim());
  return body;
}

function validContact(route, value) {
  if (route === 'email') return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) && value.length <= 254;
  if (route === 'text') {
    const digits=value.replace(/\D/g,'');
    return (digits.length===10 || (digits.length===11 && digits.startsWith('1'))) && value.length<=32;
  }
  return false;
}

export function createApplicationHandler({now=Date.now,forward}={}) {
  const send = forward ?? (async (body,request) => fetch(new URL('/',request.url), {
    method:'POST',headers:{'content-type':'application/x-www-form-urlencoded'},body:body.toString(),redirect:'manual'
  }));
  return async request => {
    if (request.method !== 'POST') return reply(405,'Method not allowed.');
    if (now() >= DEADLINE) return reply(410,'Applications closed Monday, September 14, 2026 at 8:00 p.m. CDT.');
    const declared=Number(request.headers.get('content-length') || 0);
    if (declared > MAX_BODY) return reply(413,'Submission too large.');
    if (!(request.headers.get('content-type') || '').startsWith('application/x-www-form-urlencoded')) return reply(415,'Unsupported form format.');
    const raw=await request.text();
    if (new TextEncoder().encode(raw).length > MAX_BODY) return reply(413,'Submission too large.');
    const body=cleanBody(raw);
    if (body.get('bot-field')) return reply(202,'Received.');
    if (body.get('form-name') !== FORM_NAME || body.get('state') !== 'Louisiana') return reply(400,'Invalid campaign form.');
    if (REQUIRED.some(key => !body.get(key))) return reply(400,'Complete every required field.');
    if ([...body.values()].some(value => value.length > 4000)) return reply(413,'A field is too long.');
    if (!validContact(body.get('preferred-contact'),body.get('primary-contact'))) return reply(400,'Enter a valid primary contact for the selected route.');
    if (body.get('current-coach') === 'pkfit-client') return reply(422,'Current active paid PKFIT clients are not eligible.');
    for (const key of ['adult-confirmation','weekly-checkins','health-screen-agreement','terms-agreement']) {
      if (body.get(key) !== 'yes') return reply(400,'Required acknowledgement missing.');
    }
    const forwarded=await send(body,request);
    if (!forwarded.ok && ![301,302,303].includes(forwarded.status)) return reply(502,'Application service unavailable.');
    return reply(303,'Application received.',{'location':'/two-seats/success.html'});
  };
}

export default createApplicationHandler();
export const config = {path:'/api/two-seats/apply'};
