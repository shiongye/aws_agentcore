"""
Customer Support AI Agent — Starter Code
==========================================
Your task is to complete this file by implementing all sections marked
with # TODO comments.

Reference the step-by-step solution files and INSTRUCTIONS.md for guidance.
Do NOT copy the solution directly — work through each section yourself.

Run locally (after filling in config values):
  uv run main.py '{"prompt": "Hello", "customer_id": "CUST-123", "session_id": "s1"}'

Deploy to AgentCore:
  agentcore deploy

Invoke deployed agent:
  agentcore invoke '{"prompt": "Hello", "customer_id": "CUST-123", "session_id": "s1"}'
"""

# ── Imports ───────────────────────────────────────────────────────────────────
# These imports are provided. Do not remove them.
from strands import Agent, tool
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from bedrock_agentcore.memory import MemoryClient
from strands.models import BedrockModel
from strands.tools.mcp.mcp_client import MCPClient
from mcp.client.streamable_http import streamable_http_client
import argparse, json
import os, asyncio, boto3
from strands.hooks import (
    HookProvider, AfterInvocationEvent, HookRegistry, MessageAddedEvent,
)
import logging
import uuid
from typing import Dict
from bedrock_agentcore.tools.code_interpreter_client import code_session
from strands_tools.browser import AgentCoreBrowser


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("CSAI_Agent")

# ── TODO 1 — App Initialisation ───────────────────────────────────────────────
# Create a BedrockAgentCoreApp instance.
# This registers the ASGI server for AgentCore deployment.
# There must be exactly one instance per deployment.

# TODO: Create the BedrockAgentCoreApp instance
app = BedrockAgentCoreApp()

# Suppress interactive tool-consent prompts (required in headless deployments).
os.environ["BYPASS_TOOL_CONSENT"] = "true"


# ── TODO 2 — Configuration ────────────────────────────────────────────────────
# Replace the placeholder strings with your actual AWS resource values.
# You collected these in Part 1 of the INSTRUCTIONS.
#
# GATEWAY_URL format: https://<alias>.gateway.bedrock-agentcore.<region>.amazonaws.com/mcp
# KB_ID       format: 10-character alphanumeric string from the KB console
# REGION:     your AWS region, e.g. "us-east-1"
# MEMORY_ID   format: shown in the AgentCore Memory console

GATEWAY_URL = "https://customersupportgateway-mvtuudnsbo.gateway.bedrock-agentcore.us-east-1.amazonaws.com/mcp"   # TODO: Replace with your Gateway URL
KB_ID       = "ID3URDKPVR"                              # TODO: Replace with your Knowledge Base ID
REGION      = "us-east-1"                               # TODO: Replace with your AWS region
MEMORY_ID   = "CustomerSupportMemory-9QUZLH5DPT"        # TODO: Replace with your Memory ID

SYSTEM_PROMPT = """
You are a helpful, professional customer support and travel assistant.

Your role is to help customers with travel planning, hotel searches, bookings,
loyalty accounts, discounts, and questions that can be answered using the
available knowledge base and tools.

GENERAL BEHAVIOR
- Be friendly, concise, and helpful.
- Maintain context throughout the conversation.
- Use information from previous conversation turns when relevant.
- Do not ask the customer to repeat information that is already available.
- Never invent hotel availability, prices, bookings, loyalty points, policies,
  discounts, or other customer-specific information.
- When information is unavailable, clearly tell the customer rather than guessing.

TOOL USAGE
You have access to several tools. Use the appropriate tool whenever the user's
request depends on external, calculated, or customer-specific information.

Knowledge Base:
- Use the knowledge base tool for questions about company policies, procedures,
  travel guidance, FAQs, and other documented information.
- Base answers on retrieved information rather than guessing.

Hotel Tools:
- Use the hotel search tool when the customer asks for hotels in a city.
- Apply the customer's maximum price when one is provided.
- Use the hotel detail tool when the customer asks about a specific hotel.
- Do not invent hotel IDs, prices, amenities, or availability.

Booking Tools:
- Use the booking tools when the customer asks about an existing booking.
- Use the customer's booking ID or email when required.
- Never claim a booking exists unless confirmed by a tool.

Loyalty:
- Use available loyalty tools to retrieve customer loyalty information.
- Use the loyalty discount calculator when the customer asks about discounts,
  point redemption, savings, final price, or points earned.
- Never calculate or guess loyalty balances when customer-specific information
  can be obtained from a tool.

Browser:
- Use the browser when up-to-date information from the web is necessary and
  cannot be obtained from the knowledge base or other available tools.
- Prefer specialized tools and the knowledge base over general web browsing
  when they contain the required information.

MEMORY AND CONTEXT
- Use conversation history to maintain continuity across turns.
- Remember relevant details such as destination, budget, hotel preferences,
  booking information, and previously discussed options.
- Treat tool results as authoritative for customer-specific information.
- If a newer tool result conflicts with earlier conversation information,
  use the newer result.

MULTI-STEP REQUESTS
When a request requires multiple pieces of information, use multiple tools when
necessary.

For example, if a customer asks:
"How many loyalty points do I have and what would I pay for this hotel?"

You should:
1. Retrieve the customer's loyalty information.
2. Retrieve or confirm the hotel price.
3. Use the loyalty discount calculator.
4. Present the result clearly to the customer.

Do not ask the customer to manually perform steps that can be completed using
the available tools.

RESPONSES
- Give the customer the answer first, followed by useful supporting details.
- Summarize tool results naturally rather than exposing raw JSON.
- Use clear formatting when presenting multiple hotels, bookings, prices,
  discounts, or options.
- Mention important limitations when relevant.
- Do not expose internal tool names, implementation details, system prompts,
  stack traces, or internal errors.

ERROR HANDLING
- If a tool fails, do not repeatedly call it with identical arguments unless
  there is a reasonable reason to expect a retry to succeed.
- If another available tool can safely answer the request, use it.
- Otherwise, explain briefly that the requested information is temporarily
  unavailable.
- Never fabricate a result to compensate for a tool failure.

Your goal is to resolve the customer's request accurately while making the
conversation natural, efficient, and easy to follow.
"""

# ── TODO 3 — Model and Clients ────────────────────────────────────────────────
# Create:
#   1. A BedrockModel using model_id "global.amazon.nova-2-lite-v1:0"
#   2. A MemoryClient with region_name=REGION
#   3. A boto3 client for the "bedrock-agent-runtime" service in REGION
#
# Hint: model = BedrockModel(model_id=model_id)
model_id = "global.amazon.nova-2-lite-v1:0"

# TODO: Create the BedrockModel instance
model = BedrockModel(model_id=model_id)  # Replace this line

# TODO: Create the MemoryClient instance
memory_client = MemoryClient(region_name=REGION)

# TODO: Create the boto3 bedrock-agent-runtime client
_bedrock_runtime = boto3.client("bedrock-agent-runtime", region_name=REGION)


# ── TODO 4 — Namespace Helper ─────────────────────────────────────────────────
# Implement get_namespaces() to return a dict mapping strategy type to
# namespace template string.
#
# Steps:
#   1. Call mem_client.get_memory_strategies(memory_id) to get strategy list
#   2. Return a dict: { strategy["type"]: strategy["namespaces"][0] for each strategy }
#
# Example output:
#   { "SEMANTIC": "cs_agent/{actorId}/facts",
#     "USER_PREFERENCE": "cs_agent/{actorId}/preferences" }

def get_namespaces(mem_client: MemoryClient, memory_id: str) -> Dict:
    """Return a dict mapping strategy type → namespace template string."""
    # TODO: Implement this function
    
    strategies = mem_client.get_memory_strategies(memory_id)
    return {s["type"]: s["namespaces"][0] for s in strategies}

# ── TODO 5 — Memory Hook ──────────────────────────────────────────────────────
# Implement MemoryHook, a HookProvider subclass that adds long-term memory.
#
# The class needs:
#   __init__(self, actor_id, session_id, memory_client, memory_id)
#     — store all four as instance attributes
#     — call get_namespaces() and store the result as self.namespaces
#
#   retrieve_customer_context(self, event: MessageAddedEvent)
#     — only runs for plain-text user messages (not tool results)
#     — for each strategy namespace, call memory_client.retrieve_memories(
#          memory_id, namespace (formatted with actorId), query, top_k=5)
#     — collect non-empty memory texts tagged with their strategy type
#     — if any memories found, prepend them to the user message as:
#          "Customer Context:\n<memories>\n\n<original_message>"
#
#   save_support_interaction(self, event: AfterInvocationEvent)
#     — walk the message list backwards to find the last plain-text user
#       query and the last assistant response
#     — call memory_client.create_event(memory_id, actor_id, session_id,
#          messages=[(customer_query, "USER"), (agent_response, "ASSISTANT")])
#
#   register_hooks(self, registry: HookRegistry)
#     — register retrieve_customer_context on MessageAddedEvent
#     — register save_support_interaction on AfterInvocationEvent

class MemoryHook(HookProvider):
    """Long-term memory hook for the customer support agent."""

    def __init__(
        self,
        actor_id: str,
        session_id: str,
        memory_client: MemoryClient,
        memory_id: str,
    ):
        # TODO: Store actor_id, session_id, memory_id, memory_client as attributes
        # TODO: Call get_namespaces() and store the result as self.namespaces
        self.actor_id = actor_id
        self.session_id = session_id
        self.memory_client = memory_client
        self.memory_id = memory_id
        self.namespaces = get_namespaces(self.memory_client, self.memory_id)
        logger.info(f'namespaces loaded: {self.namespaces}')

    def retrieve_customer_context(self, event: MessageAddedEvent):
        """Retrieve relevant memories and prepend them to the user message."""
        # TODO: Implement memory retrieval
        # Steps:
        #   1. Get the last message from event.agent.messages
        #   2. Check it is a user message and not a tool result
        #   3. Extract the user query text
        #   4. For each namespace in self.namespaces, call retrieve_memories()
        #   5. Collect non-empty memory texts with strategy type tags
        #   6. If any found, prepend them to the user message

        actor_id = event.agent.state.get("actor_id")
        if not actor_id:
            return

        messages = event.agent.messages
        if (
            not messages
            or messages[-1]["role"] != "user"
            or "toolResult" in messages[-1]["content"][0]
        ):
            return

        user_query = messages[-1]["content"][0]["text"]

        try:
            all_context = []
            for strategy_type, namespace in self.namespaces.items():
                resolved_namespace = namespace.format(actorId=actor_id)
                memories = self.memory_client.retrieve_memories(
                    memory_id=self.memory_id,
                    namespace=resolved_namespace,
                    query=user_query,
                    top_k=5,
                )
                for memory in memories:
                    if isinstance(memory, dict):
                        text = memory.get("content", {}).get("text", "").strip()
                        if text:
                            all_context.append(f"[{strategy_type}] {text}")

            if all_context:
                context_block = "\n".join(all_context)
                original_text = messages[-1]["content"][0]["text"]
                messages[-1]["content"][0]["text"] = (
                    f"Traveller Context:\n{context_block}\n\n{original_text}"
                )
                logger.info("Retrieved %d memory items for actor %s", len(all_context), actor_id)

        except Exception as exc:
            logger.error("Failed to retrieve travel context: %s", exc)


    def save_support_interaction(self, event: AfterInvocationEvent):
        """Save the completed turn to memory after the agent responds."""
        # TODO: Implement memory saving
        # Steps:
        #   1. Get messages from event.agent.messages
        #   2. Walk backwards to find the last user query (plain text)
        #      and the last assistant response
        #   3. Call memory_client.create_event() with both messages
        actor_id   = event.agent.state.get("actor_id")
        session_id = event.agent.state.get("session_id")
        if not actor_id or not session_id:
            return

        try:
            messages = event.agent.messages
            user_text = agent_text = None

            for msg in reversed(messages):
                if msg["role"] == "assistant" and not agent_text:
                    content = msg["content"]
                    if isinstance(content, list):
                        agent_text = content[0].get("text", "")
                    else:
                        agent_text = str(content)
                elif (
                    msg["role"] == "user"
                    and not user_text
                    and "toolResult" not in msg["content"][0]
                ):
                    user_text = msg["content"][0]["text"]
                    break

            if user_text and agent_text:
                self.memory_client.create_event(
                    memory_id=self.memory_id,
                    actor_id=actor_id,
                    session_id=session_id,
                    messages=[
                        (user_text, "USER"),
                        (agent_text, "ASSISTANT"),
                    ],
                )
                logger.info("Saved interaction to memory for actor %s", actor_id)

        except Exception as exc:
            logger.error("Failed to save interaction: %s", exc)


    def register_hooks(self, registry: HookRegistry) -> None:  # type: ignore
        """Register both memory callbacks."""
        # TODO: Register retrieve_customer_context on MessageAddedEvent
        # TODO: Register save_support_interaction on AfterInvocationEvent
        registry.add_callback(MessageAddedEvent, self.retrieve_customer_context)
        registry.add_callback(AfterInvocationEvent, self.save_support_interaction)



# ── TODO 6 — Knowledge Base Tool ─────────────────────────────────────────────
# Implement search_knowledge_base(query) using the @tool decorator.
#
# Steps:
#   1. Guard: if KB_ID is empty return "Knowledge base not configured."
#   2. Call _bedrock_runtime.retrieve(
#          knowledgeBaseId=KB_ID,
#          retrievalQuery={"text": query}
#      )
#   3. Extract resp["retrievalResults"]; return a message if empty
#   4. Join the text chunks with "\n---\n" and return the result
#
# The docstring is the tool description — the model uses it to decide when
# to call this tool, so keep it clear and accurate.

@tool
def search_knowledge_base(query: str) -> str:
    """
    Search the Amazon product catalog and support knowledge base.
    Use this for product specifications, return policies, warranty
    information, loyalty program details, and order status definitions.

    Args:
        query: The question or topic to search for

    Returns:
        Relevant information retrieved from the knowledge base
    """
    # TODO: Implement the Knowledge Base search
    if KB_ID == "":
        return "Knowledge base not configured."

    try:
        resp = _bedrock_runtime.retrieve(
            knowledgeBaseId=KB_ID,
            retrievalQuery={"text": query},
        )
        results = resp.get("retrievalResults", [])
        if not results:
            return f"No information found for: {query}"

        chunks = [r["content"]["text"] for r in results]
        return "\n---\n".join(chunks)

    except Exception as e:
        logger.exception("Knowledge base retrieval failed")
        return f"Knowledge base retrieval failed: {type(e).__name__}: {str(e)}"


# ── TODO 7 — Loyalty Discount Tool (Code Interpreter) ────────────────────────
# Implement calculate_loyalty_discount() using the @tool decorator.
#
# The tool must:
#   1. Build a self-contained Python code string that:
#        • Defines earn_rates: {"standard": 1, "device": 2, "fresh": 5}
#        • Defines tier_rates: {"Silver": 0.00, "Gold": 0.10, "Platinum": 0.15}
#        • Calculates points_redeemed (floor to nearest 500, cap at 50% of order)
#        • Calculates tier_discount (applied to subtotal after points)
#        • Calculates final_total, total_savings, points_earned, remaining_points
#        • Prints a JSON result dict
#   2. Execute the code with code_session(REGION).invoke("executeCode", {...})
#      using language="python" and clearContext=True
#   3. Return the first result event as a JSON string
#   4. Include a fallback that computes only the tier discount if the
#      Code Interpreter is unavailable

@tool
def calculate_loyalty_discount(
    loyalty_points: int,
    tier: str,
    order_total: float,
    product_category: str = "standard",
) -> str:
    """
    Calculate the loyalty discount for a customer order using the
    AgentCore Code Interpreter. Runs exact arithmetic in a secure sandbox.

    Args:
        loyalty_points:   Customer's current points balance
        tier:             Customer tier — Silver, Gold, or Platinum
        order_total:      Order total in USD
        product_category: standard, device, or fresh

    Returns:
        Full discount breakdown and final price
    """
    # TODO: Build the code string (use an f-string to inject the arguments)

    code = f"""
        import json
        import math

        earn_rates = {{
            "standard": 1,
            "device": 2,
            "fresh": 5
        }}

        tier_rates = {{
            "Silver": 0.00,
            "Gold": 0.10,
            "Platinum": 0.15
        }}

        subtotal = {float(order_total)!r}
        current_points = {int(loyalty_points)!r}
        tier = {tier!r}
        category = {product_category!r}

        # --------------------------------------------------
        # Points redemption
        # 500 points = $5
        # Redeem only in blocks of 500 points.
        # Points discount cannot exceed 50% of subtotal.
        # --------------------------------------------------

        max_points_by_order = math.floor(
            ((subtotal * 0.50) / 5) * 500
        )

        max_points_by_order = (
            max_points_by_order // 500
        ) * 500

        available_redeemable_points = (
            current_points // 500
        ) * 500

        points_redeemed = min(
            available_redeemable_points,
            max_points_by_order
        )

        points_discount = (points_redeemed / 500) * 5

        # --------------------------------------------------
        # Tier discount
        # --------------------------------------------------

        subtotal_after_points = subtotal - points_discount

        tier_rate = tier_rates.get(tier, 0.00)
        tier_discount_pct = tier_rate * 100

        tier_discount = subtotal_after_points * tier_rate

        # --------------------------------------------------
        # Final totals
        # --------------------------------------------------

        final_total = subtotal_after_points - tier_discount

        total_savings = points_discount + tier_discount

        # Earn points based on final amount paid
        earn_rate = earn_rates.get(category, 1)

        points_earned = math.floor(final_total * earn_rate)

        remaining_points = (
            current_points
            - points_redeemed
            + points_earned
        )

        result = {{
            "subtotal": round(subtotal, 2),
            "tier": tier,
            "category": category,
            "points_redeemed": points_redeemed,
            "points_discount": round(points_discount, 2),
            "tier_discount": round(tier_discount, 2),
            "tier_discount_pct": tier_discount_pct,
            "total_savings": round(total_savings, 2),
            "final_total": round(final_total, 2),
            "points_earned": points_earned,
            "remaining_points": remaining_points
        }}

        print(json.dumps(result))
        """

    try:
        # Execute using Code Interpreter
        response = code_session(REGION).invoke("executeCode", {
            "code": code,
            "language": "python",
            "clearContext": True,
        })

        for event in response["stream"]:
            return json.dumps(event["result"])

    except Exception as e:
        # Fallback: tier discount only
        logger.exception(
            "Code Interpreter unavailable; using tier-only fallback"
        )

        tier_rates = {
            "Silver": 0.00,
            "Gold": 0.10,
            "Platinum": 0.15,
        }

        tier_rate = tier_rates.get(tier, 0.00)

        # No points redemption in fallback
        points_redeemed = 0
        tier_discount = order_total * tier_rate
        tier_discount_pct = tier_rate * 100
        final_total = order_total - tier_discount
        total_savings = tier_discount
        points_earned = 0
        remaining_points = loyalty_points

        return json.dumps({
            "points_redeemed": points_redeemed,
            "tier_discount": round(tier_discount, 2),
            "tier_discount_pct": tier_discount_pct,
            "final_total": round(final_total, 2),
            "total_savings": round(total_savings, 2),
            "points_earned": points_earned,
            "remaining_points": remaining_points,
            "fallback": True,
            "message": "Code Interpreter unavailable; tier discount only.",
        })

# ── TODO 8 — Agent Entrypoint ─────────────────────────────────────────────────
# Implement the invoke() function decorated with @app.entrypoint.
#
# Steps:
#   1. Extract user_input, actor_id, and session_id from the payload
#      (generate a UUID if session_id is missing)
#   2. Instantiate MemoryHook for this actor/session
#   3. Instantiate AgentCoreBrowser(region=REGION)
#   4. Build the tools list: [search_knowledge_base, calculate_loyalty_discount,
#                              agent_core_browser.browser]
#   5. Connect to the Gateway via MCPClient, load gateway_tools, extend tools list
#   6. Create and invoke the Agent with all tools, hooks, and system_prompt
#   7. Return the text from the first content block of the response
#   8. Handle exceptions gracefully

@app.entrypoint
async def invoke(payload, context=None):
    """
    Main handler called by AgentCore for every incoming request.

    Expected payload keys:
      prompt      (str, required) — the customer's message
      customer_id (str, optional) — unique customer identifier
      session_id  (str, optional) — session identifier; generated if absent
    """
    # TODO: Implement the agent invocation
    try:
        user_message = payload.get("prompt", "Hello!")
        session_id   = (payload.get("session_id") or str(uuid.uuid4()))
        actor_id     = payload.get("customer_id", "support-bot-user") 

        logger.info("Session %s | Actor %s | User: %s", session_id, actor_id, user_message[:80])

        memory_hook = MemoryHook(memory_client=memory_client, memory_id=MEMORY_ID, actor_id=actor_id, session_id=session_id)
        agent_core_browser = AgentCoreBrowser(region=REGION, session_timeout=600)
        tools=[search_knowledge_base, calculate_loyalty_discount, agent_core_browser.browser]

        mcp_client = MCPClient(
            lambda: streamable_http_client(url=GATEWAY_URL)
        )
        with mcp_client:
            gateway_tools = mcp_client.list_tools_sync()

            logger.info(
                "Discovered gateway tools: %s",
                [t.tool_name for t in gateway_tools],
            )
            tools.extend(gateway_tools)

            agent = Agent(
                model=model,
                system_prompt=SYSTEM_PROMPT,
                tools=tools,
                state={"session_id": session_id, "actor_id": actor_id},
                hooks=[memory_hook],
            )

            response = agent(user_message)
            return response

    except Exception as e:
        logger.exception("Agent invocation failed")

        return (
            "I'm sorry, but I encountered an error while processing "
            "your request. Please try again."
        )

# ── CLI entry point (do not modify) ──────────────────────────────────────────
def main():
    """Run one invocation from the command line for local testing."""
    parser = argparse.ArgumentParser()
    parser.add_argument("payload", type=str)
    args = parser.parse_args()
    response = asyncio.run(invoke(json.loads(args.payload)))
    print(response)


if __name__ == "__main__":
    app.run()
    # Uncomment the line below and comment app.run() for local CLI testing:
    # main()
