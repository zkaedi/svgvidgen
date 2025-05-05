export default {
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === "/render" && request.method === "POST") {
      const body = await request.json();
      const width = body.width || 800;
      const height = body.height || 600;
      const message = body.message || "Hello from svgvidgen";

      const svg = `
        <svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}">
          <rect width="100%" height="100%" fill="#111"/>
          <text x="50" y="100" fill="#0ff" font-size="48">${message}</text>
        </svg>
      `;

      return new Response(svg, {
        headers: { "Content-Type": "image/svg+xml" },
      });
    }

    return new Response("svgvidgen is live!", {
      headers: { "Content-Type": "text/plain" },
    });
  }
};
