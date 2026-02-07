export async function POST(request: Request) {
  try {
    const body = await request.json();
    const url = typeof body?.url === "string" ? body.url.trim() : "";

    if (!url) {
      return new Response(JSON.stringify({ detail: "URL is required." }), {
        status: 400,
        headers: {
          "Content-Type": "application/json"
        }
      });
    }

    const apiBaseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    console.log(`Forwarding request to backend API at ${apiBaseUrl}/shorten`);
    const response = await fetch(`${apiBaseUrl}/shorten`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url })
    });

    const payload = await response.text();
    return new Response(payload, {
      status: response.status,
      headers: {
        "Content-Type": response.headers.get("content-type") ?? "application/json"
      }
    });
  } catch (error) {
    return new Response(
      JSON.stringify({ detail: "Failed to process request." }),
      {
      status: 500,
      headers: {
        "Content-Type": "application/json"
      }
    });
  }
}
