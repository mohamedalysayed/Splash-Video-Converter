// Netlify Function — verifies a Stripe Checkout session before the
// /thank-you page reveals the download links.
//
// Flow:
//   1. Page receives ?session_id=cs_xxx from Stripe's success redirect
//   2. Page POSTs that id here
//   3. We call Stripe with the secret key (env: STRIPE_SECRET_KEY)
//   4. We respond with { valid: true, email, ... } or { valid: false, reason }
//
// Both "paid" and "no_payment_required" (100%-off coupons) count as valid.
import Stripe from "stripe";

const cors = {
  "Content-Type": "application/json",
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Cache-Control": "no-store",
};

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: cors });

export default async (request) => {
  if (request.method === "OPTIONS") return new Response("", { headers: cors });

  const url = new URL(request.url);
  const sessionId =
    url.searchParams.get("session_id") ||
    (await request.json().catch(() => ({})))?.session_id;

  if (!sessionId || !sessionId.startsWith("cs_")) {
    return json({ valid: false, reason: "no_session_id" }, 400);
  }

  const key = process.env.STRIPE_SECRET_KEY;
  if (!key) {
    return json({ valid: false, reason: "server_misconfigured" }, 500);
  }

  try {
    const stripe = new Stripe(key, { apiVersion: "2024-12-18.acacia" });
    const session = await stripe.checkout.sessions.retrieve(sessionId);

    const ok =
      session.payment_status === "paid" ||
      session.payment_status === "no_payment_required";

    if (!ok) {
      return json({ valid: false, reason: "not_paid", payment_status: session.payment_status });
    }

    return json({
      valid: true,
      email: session.customer_details?.email ?? null,
      name:  session.customer_details?.name  ?? null,
      amount: session.amount_total,
      currency: session.currency,
    });
  } catch (e) {
    return json({ valid: false, reason: "invalid_session", message: e?.message });
  }
};

export const config = { path: "/api/verify-session" };
