import ModelClient, { isUnexpected } from "@azure-rest/ai-inference";
import { AzureKeyCredential } from "@azure/core-auth";
import * as dotenv from "dotenv";

// Load environment variables from .env file
dotenv.config();

const token = process.env.AZURE_API_KEY;
const endpoint = "https://models.inference.ai.azure.com";
const modelName = "DeepSeek-R1";

export async function main() {
  if (!token) {
    console.error("Missing AZURE_API_KEY in environment variables.");
    return;
  }

  const client = ModelClient(
    endpoint,
    new AzureKeyCredential(token),
  );

  const response = await client.path("/chat/completions").post({
    body: {
      messages: [
        { role: "user", content: "What is the capital of France?" }
      ],
      max_tokens: 1000,
      model: modelName
    }
  });

  if (isUnexpected(response)) {
    throw response.body.error;
  }

  console.log(response.body.choices[0].message.content);
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
