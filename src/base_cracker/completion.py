from openai import OpenAI
import dotenv
import os
import json
import base64

dotenv.load_dotenv()

endpoint = "https://test1-cityagent-resource.services.ai.azure.com/openai/v1/"
model_name = "gpt-oss-120b"
deployment_name = "gpt-oss-120b"

api_key = os.getenv("AZURE_OPENAI_KEY")

client = OpenAI(base_url=endpoint, api_key=api_key)

# === Local tool implementations ===

def decode_hex_bytes(hex_bytes: str) -> str:
    b = bytes(int(x, 16) for x in hex_bytes.split())
    return b.decode("latin-1", errors="replace")

def decode_base64(s: str) -> str:
    return base64.b64decode(s).decode("latin-1", errors="replace")

def decode_morse(morse: str) -> str:
    MORSE = {
        ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E",
        "..-.": "F", "--.": "G", "....": "H", "..": "I", ".---": "J",
        "-.-": "K", ".-..": "L", "--": "M", "-.": "N", "---": "O",
        ".--.": "P", "--.-": "Q", ".-.": "R", "...": "S", "-": "T",
        "..-": "U", "...-": "V", ".--": "W", "-..-": "X", "-.--": "Y",
        "--..": "Z", "/": " "
    }
    return "".join(MORSE.get(tok, "?") for tok in morse.split())

def dispatch_tool_call(tool_call):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    if name == "decode_hex_bytes":
        return decode_hex_bytes(args["hex_bytes"])
    if name == "decode_base64":
        return decode_base64(args["s"])
    if name == "decode_morse":
        return decode_morse(args["morse"])

    raise ValueError(f"Unknown tool: {name}")

# === Tool schemas ===

tools = [
    {
        "type": "function",
        "function": {
            "name": "decode_hex_bytes",
            "description": "Decode space-separated hex bytes into text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "hex_bytes": {"type": "string"},
                },
                "required": ["hex_bytes"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "decode_base64",
            "description": "Base64 decode a string into text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "s": {"type": "string"},
                },
                "required": ["s"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "decode_morse",
            "description": "Decode Morse code (.- with spaces).",
            "parameters": {
                "type": "object",
                "properties": {
                    "morse": {"type": "string"},
                },
                "required": ["morse"],
            },
        },
    },
]

messages = [
    {
        "role": "system",
        "content": "You are a cryptography assistant working on messages M1–M7. "
                   "Call tools to decode hex, base64, and Morse rather than doing all math in your head.",
    },
    {
        "role": "user",
        "content": (
            "M1: 54 68 65 54 72 00 75 74 68 49 1A 73 4E 7F 65 61 72\n"
            "M2: MkFBMEJCMENNMEYxMkQzMTFBMzEyQjJEMzE1N0U=\n"
            "M3: 178 150 38 118 150 198 41 104 162 104 104 162 153 214 12 200 40 172\n"
            "M4: -.. .. ....- .--. ..... -... -. --- .--. .... --.- -... -.. ..-.\n"
            "M5: S-51.I3,Koo/rDg!vmiv?gmr:13sG\n"
            "M6: Um..VhZ.EVo$Y2h.Nc3l@qY.G$ZnJv.bVN0Y.XJ0VG.9@GaW5..pc2.g==\n"
            "M7: 37 24 31 115 79\n\n"
            "Figure out what you can. Start with the ones that look like hex, base64, or Morse."
        ),
    },
]

# 1) First call – model may request tool calls
first = client.chat.completions.create(
    model=deployment_name,
    messages=messages,
    tools=tools,
    tool_choice="auto",
)

assistant_msg = first.choices[0].message
messages.append(assistant_msg)

if assistant_msg.tool_calls:
    # 2) Execute tools and send results back
    for tc in assistant_msg.tool_calls:
        result = dispatch_tool_call(tc)
        messages.append({
            "role": "tool",
            "tool_call_id": tc.id,
            "name": tc.function.name,
            "content": result,
        })

    # 3) Final answer
    second = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
    )
    final_msg = second.choices[0].message
else:
    final_msg = assistant_msg

print(final_msg.content)
