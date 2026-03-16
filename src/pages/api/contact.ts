import type { APIRoute } from 'astro';
import { Resend } from 'resend';

export const prerender = false;

interface ContactForm {
  name: string;
  email: string;
  phone?: string;
  company?: string;
  service?: string;
  message: string;
}

const EMAIL_REGEX = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
const HEADER_INJECTION_REGEX = /[\r\n\0]/;
const MAX_MESSAGE_LENGTH = 5000;
const MAX_NAME_LENGTH = 100;
const MAX_PHONE_LENGTH = 30;
const MAX_COMPANY_LENGTH = 100;
const MAX_SERVICE_LENGTH = 100;
const TO_EMAIL = 'jobs@romarkengineering.com';
const FROM_EMAIL = 'Romark Engineering <noreply@romarkengineering.com>';

// Rate limiting
const RATE_LIMIT_WINDOW_MS = 3_600_000; // 1 hour
const MAX_REQUESTS_PER_WINDOW = 5;
const requestLog = new Map<string, number[]>();

function isRateLimited(ip: string): boolean {
  const now = Date.now();
  const cutoff = now - RATE_LIMIT_WINDOW_MS;
  const timestamps = (requestLog.get(ip) || []).filter((t) => t > cutoff);

  if (timestamps.length >= MAX_REQUESTS_PER_WINDOW) {
    return true;
  }

  timestamps.push(now);
  requestLog.set(ip, timestamps);

  // Housekeeping: prune stale IPs every 100 entries
  if (requestLog.size > 100) {
    for (const [key, ts] of requestLog) {
      if (ts.every((t) => t <= cutoff)) requestLog.delete(key);
    }
  }

  return false;
}

function getClientIp(request: Request): string {
  return (
    request.headers.get('x-forwarded-for')?.split(',')[0]?.trim() ||
    request.headers.get('cf-connecting-ip') ||
    'unknown'
  );
}

function validate(body: unknown): { data?: ContactForm; error?: string } {
  if (!body || typeof body !== 'object') {
    return { error: 'Invalid request body' };
  }

  const { name, email, phone, company, service, message } = body as Record<string, unknown>;

  if (!name || typeof name !== 'string' || name.trim().length === 0) {
    return { error: 'Name is required' };
  }

  if (name.trim().length > MAX_NAME_LENGTH) {
    return { error: `Name must be ${MAX_NAME_LENGTH} characters or fewer` };
  }

  if (HEADER_INJECTION_REGEX.test(name)) {
    return { error: 'Name contains invalid characters' };
  }

  if (!email || typeof email !== 'string' || email.trim().length === 0) {
    return { error: 'Email is required' };
  }

  if (!EMAIL_REGEX.test(email.trim()) || HEADER_INJECTION_REGEX.test(email)) {
    return { error: 'Please provide a valid email address' };
  }

  if (!message || typeof message !== 'string' || message.trim().length === 0) {
    return { error: 'Message is required' };
  }

  if (message.trim().length > MAX_MESSAGE_LENGTH) {
    return { error: `Message must be ${MAX_MESSAGE_LENGTH} characters or fewer` };
  }

  const trimmedPhone = phone && typeof phone === 'string' ? phone.trim() : undefined;
  const trimmedCompany = company && typeof company === 'string' ? company.trim() : undefined;
  const trimmedService = service && typeof service === 'string' ? service.trim() : undefined;

  if (trimmedPhone && (trimmedPhone.length > MAX_PHONE_LENGTH || HEADER_INJECTION_REGEX.test(trimmedPhone))) {
    return { error: 'Phone number is invalid' };
  }

  if (trimmedCompany && trimmedCompany.length > MAX_COMPANY_LENGTH) {
    return { error: `Company name must be ${MAX_COMPANY_LENGTH} characters or fewer` };
  }

  if (trimmedService && (trimmedService.length > MAX_SERVICE_LENGTH || HEADER_INJECTION_REGEX.test(trimmedService))) {
    return { error: 'Service field contains invalid characters' };
  }

  return {
    data: {
      name: name.trim(),
      email: email.trim(),
      phone: trimmedPhone || undefined,
      company: trimmedCompany || undefined,
      service: trimmedService || undefined,
      message: message.trim(),
    },
  };
}

function buildEmailHtml(data: ContactForm): string {
  const rows: string[] = [];

  rows.push(row('Name', data.name));
  rows.push(row('Email', `<a href="mailto:${escape(data.email)}">${escape(data.email)}</a>`));

  if (data.phone) {
    rows.push(row('Phone', escape(data.phone)));
  }
  if (data.company) {
    rows.push(row('Company', escape(data.company)));
  }
  if (data.service) {
    rows.push(row('Service Interest', escape(data.service)));
  }

  rows.push(row('Message', escape(data.message).replace(/\n/g, '<br>')));

  return `
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: 0 auto;">
  <h2 style="color: #1a365d; border-bottom: 2px solid #e53e3e; padding-bottom: 8px;">
    New Website Enquiry
  </h2>
  <table style="width: 100%; border-collapse: collapse; margin-top: 16px;">
    ${rows.join('\n    ')}
  </table>
  <p style="margin-top: 24px; font-size: 12px; color: #888;">
    Sent from the Romark Engineering website contact form.
  </p>
</body>
</html>`.trim();
}

function row(label: string, value: string): string {
  return `<tr>
      <td style="padding: 8px 12px; font-weight: bold; vertical-align: top; width: 140px; background: #f7f7f7; border: 1px solid #e2e2e2;">${label}</td>
      <td style="padding: 8px 12px; border: 1px solid #e2e2e2;">${value}</td>
    </tr>`;
}

function escape(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

export const POST: APIRoute = async ({ request, url }) => {
  // Rate limiting
  const clientIp = getClientIp(request);
  if (isRateLimited(clientIp)) {
    return new Response(
      JSON.stringify({ error: 'Too many requests. Please try again later.' }),
      { status: 429, headers: { 'Content-Type': 'application/json' } }
    );
  }

  // CSRF: verify request origin matches the site
  const origin = request.headers.get('origin');
  const expectedOrigin = url.origin;
  if (origin && origin !== expectedOrigin) {
    return new Response(JSON.stringify({ error: 'Unauthorized' }), {
      status: 403,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // Validate Content-Type
  const contentType = request.headers.get('content-type');
  if (!contentType?.includes('application/json')) {
    return new Response(JSON.stringify({ error: 'Content-Type must be application/json' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const { data, error } = validate(body);

  if (error || !data) {
    return new Response(JSON.stringify({ error }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const apiKey = import.meta.env.RESEND_API_KEY;

  if (!apiKey) {
    console.error('RESEND_API_KEY is not configured');
    return new Response(JSON.stringify({ error: 'Failed to send message' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  try {
    const resend = new Resend(apiKey);

    const subject = data.service
      ? `Website Enquiry: ${data.service} — ${data.name}`
      : `Website Enquiry from ${data.name}`;

    const { error: sendError } = await resend.emails.send({
      from: FROM_EMAIL,
      to: TO_EMAIL,
      replyTo: data.email,
      subject,
      html: buildEmailHtml(data),
    });

    if (sendError) {
      console.error('Resend API error:', sendError);
      return new Response(JSON.stringify({ error: 'Failed to send message' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    return new Response(JSON.stringify({ success: true }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (err) {
    console.error('Unexpected error sending email:', err);
    return new Response(JSON.stringify({ error: 'Failed to send message' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
};
