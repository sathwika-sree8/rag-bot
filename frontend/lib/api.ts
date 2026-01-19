const BACKEND_URL = "http://127.0.0.1:8000";

export async function ingest(text: string) {
  const res = await fetch(`${BACKEND_URL}/ingest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      text,
      source: "frontend",
      title: "User Input"
    })
  });

  if (!res.ok) {
    throw new Error("Failed to ingest text");
  }

  return res.json();
}

export async function query(question: string) {
  const res = await fetch(`${BACKEND_URL}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: question })
  });

  if (!res.ok) {
    throw new Error("Failed to query");
  }

  return res.json();
}
