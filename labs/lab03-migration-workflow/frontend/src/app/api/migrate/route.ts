const BACKEND_URL = "https://migration-workflow-production.up.railway.app/migrate";

export async function POST(request: Request) {
  try {
    const body = await request.json();

    const response = await fetch(BACKEND_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
    });

    const payload = await response.text();

    return new Response(payload, {
      status: response.status,
      headers: {
        "Content-Type": response.headers.get("content-type") ?? "application/json"
      }
    });
  } catch {
    return new Response(JSON.stringify({ detail: "Failed to process migration request." }), {
      status: 500,
      headers: {
        "Content-Type": "application/json"
      }
    });
  }
}
