const AGENTS = [
  {
    name: "Research Agent",
    system: "You are a research specialist. Provide clear research and approach for solving the user request.",
  },
  {
    name: "Coding Agent",
    system: "You are a coding expert. Write clean and practical code for the user request.",
  },
  {
    name: "Review Agent",
    system: "You are a senior reviewer. Improve and optimize the proposed solution.",
  },
  {
    name: "Explanation Agent",
    system: "You are a teacher. Explain the final solution in simple beginner-friendly words.",
  },
];

async function callModel(provider, model, apiKey, messages) {
  let url = "";
  if (provider === "openai") {
    url = "https://api.openai.com/v1/chat/completions";
  } else {
    url = "https://router.huggingface.co/v1/chat/completions";
  }

  const response = await fetch(url, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model,
      messages,
      temperature: 0.3,
    }),
  });

  if (!response.ok) {
    const errText = await response.text();
    throw new Error(`${provider} API error ${response.status}: ${errText}`);
  }

  const data = await response.json();
  const content = data?.choices?.[0]?.message?.content;
  if (!content) {
    throw new Error("Model response was empty.");
  }
  return content;
}

export default async function handler(req, res) {
  if (req.method === "OPTIONS") {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");
    return res.status(200).end();
  }

  if (req.method !== "POST") {
    return res.status(405).json({ ok: false, error: "Use POST for this endpoint." });
  }

  try {
    const body = typeof req.body === "string" ? JSON.parse(req.body) : req.body;
    const problem = (body?.problem || "").trim();
    if (!problem) {
      return res.status(400).json({ ok: false, error: "Please enter a valid problem statement." });
    }

    const provider = (process.env.LLM_PROVIDER || "huggingface").trim().toLowerCase();
    let model = "";
    let apiKey = "";

    if (provider === "openai") {
      model = (process.env.OPENAI_MODEL_NAME || "gpt-4o-mini").trim();
      apiKey = (process.env.OPENAI_API_KEY || "").trim();
    } else {
      model = (process.env.HUGGINGFACE_MODEL_NAME || "Qwen/Qwen2.5-7B-Instruct").trim();
      apiKey = ((process.env.HUGGINGFACE_API_KEY || process.env.OPENAI_API_KEY || "")).trim();
    }

    if (!apiKey) {
      return res.status(400).json({
        ok: false,
        error: "Missing API key in environment variables.",
      });
    }

    const steps = [];
    const logs = [];
    let sharedContext = `User request:\n${problem}\n`;

    for (let i = 0; i < AGENTS.length; i += 1) {
      const agent = AGENTS[i];
      logs.push(`Starting ${agent.name}`);

      const output = await callModel(provider, model, apiKey, [
        { role: "system", content: agent.system },
        {
          role: "user",
          content: `${sharedContext}\nProduce your output for this step only.`,
        },
      ]);

      steps.push({
        step: i + 1,
        agent: agent.name,
        description: agent.system,
        output,
      });

      sharedContext += `\n${agent.name} output:\n${output}\n`;
      logs.push(`Completed ${agent.name}`);
    }

    const finalOutput = steps[steps.length - 1]?.output || "No final output.";

    return res.status(200).json({
      ok: true,
      message: "All agents completed successfully.",
      steps,
      terminal_logs: logs.join("\n"),
      final_output: finalOutput,
    });
  } catch (error) {
    return res.status(500).json({
      ok: false,
      error: error.message || "Unexpected server error.",
    });
  }
}
