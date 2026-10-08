pip install -r requirements.txt 
agentcore configure
agentcore ddev
git init
cd ../..
cd .
cd ..
git init
git add .
Get-ChildItem -Force ".\Exercises\cd14763 C2 Executing Code with AgentCore Code Interpreter\Exercise"
git ls-files --stage
bash: Get-ChildItem: command not found
git status
git ls-files --stage
Get-ChildItem -Force ".\Exercises\cd14763 C2 Executing Code with AgentCore Code Interpreter\Exercise"
.git
ls -la "Exercises/cd14763 C2 Executing Code with AgentCore Code Interpreter/Exercise"
git status
Get-ChildItem -Force ".\Exercises\cd14763 C2 Executing Code with AgentCore Code Interpreter\Exercise"
exit
agentcore configure
agencore configure
agentcore configure
agentcore dev
pip show bedrock-agentcore-starter-toolkit
pip install bedrock-agentcore-starter-toolkit
pip show bedrock-agentcore-starter-toolkit
agentcore configure
python -m agentcore --help
agentcore --help
which agentcore
type -a agentcore
agentcore dev
agentcore create
pip show -f bedrock-agentcore-starter-toolkit | grep -E "bin|agentcore"
python -m pip show bedrock-agentcore-starter-toolkit
agentcore configure
python -c "import sys; print(sys.prefix)"
ls -l "$(python -c 'import sys; print(sys.prefix)')/bin/agentcore"
which pip
pip -V
ls -l "$(dirname "$(which pip)")/agentcore"
~/.local/bin/agentcore --help
export PATH="$HOME/.local/bin:$PATH"
agentcore --help
agentcore configure
aws configure
agentcore configure
agentcore deploy
python -m pip install --user uv
agentcore deploy
agentcore destroy -- Wanderbot
agentcore destroy --help
agentcore destroy --agent -a
agentcore configure list
agentcore destroy --agent Wanderbot
agentcore configure
agentcore deploy
agentcore invoke '{"message": "How do I contact Horizon Travel customer support?"}'
agentcore invoke '{"message": "A flight costs $349. Hotel is $175/night for 4 nights. Total?"}'
agetncore dev
agentcore dev
agentcore create
agentcore configure
agentcore --help
cat >> ~/.bashrc <<'EOF'agentcore() {    python3 -c "from bedrock_agentcore_starter_toolkit.cli.cli import main; main()" "$@"}EOF
source ~/.bashrc
agentcore --help
cd ~/Exercises/cd14763\ C2\ Executing\ Code\ with\ AgentCore\ Code\ Interpreter/Demoagentcore --help
agentcore confiugre
agentcore configure
printf '\nagentcore() { python3 -c "from bedrock_agentcore_starter_toolkit.cli.cli import main; main()" "$@"; }\n' >> ~/.bashrc
source ~/.bashrc
type agentcore
uv pip install bedrock-agentcore-starter-toolkit
agentcore configure
agentcore deploy
agentcore invoke '{"message": "How do I contact Horizon Travel customer support?"}'
agentcore invoke '{"message": "How do I contact Horizon Travel customer support?"}'
agentcore configure
agentcore dev
uv pip install strands
agentcore dev
uv pip install strands-agents bedrock-agentcore bedrock-agentcore-starter-toolkit
agentcore dev
uv pip install strands-tools
agentcore configure
agentcore dev
agentcore deploy
agentcore configure
agentcore deploy
agentcore deploy --auto-update-on-conflict
agentcore invoke '{"message": "How do I contact Horizon Travel customer support?"}'
agentcore invoke '{"message": "A flight costs $349. Hotel is $175/night for 4 nights. Total?"}'
agentcore invoke --dev '{"message": "A flight costs $349. Hotel is $175/night for 4 nights. Total?"}'
uv pip install -r requirements.txt
ER=arn:aws:iam::102959685868:role/AmazonBedrockAgentCoreSDKRuntime-us-east-1-a25b0cb827
agentcore configure -e starter.py -n WanderBot -dt container   -rf requirements.txt --disable-memory   -er $ER -ecr $ECR_URI --non-interactive
agentcore configure
agentcore dev
agentcore invoke --dev '{"message": "Find flights from BCN to FCO on 2026-03-20"}'
agentcore deploy
agentcore deploy --auto-update-on-conflict
agentcore invoke '{"message": "Find flights from Barcelona to Rome on 2026-03-20 and convert $500 to EUR"}'
agentcore configure
agentcore dev
agentcore configure
agentcore deploy 
agentcore deploy --auto-update-on-conflict
agentcore invoke '{"message": "Find flights from Barcelona to Rome on 2026-03-20 and convert $500 to EUR"}'
aws logs tail /aws/bedrock-agentcore/runtimes/WanderBot-RwdOTw2AS5-DEFAULT --log-stream-name-prefix "2026/09/12/[runtime-logs" --follow[A
agentcore invoke '{"message": "hotels in japan under 300 usd per night"}'
agentcore invoke '{"message": "hotels in tokyo under 300 usd per night"}'
agentcore --dev '{"message": "Find flights from Barcelona to Rome on 2026-03-20 and convert $500 to EUR"}'
agentcore invoke --dev '{"message": "Find flights from Barcelona to Rome on 2026-03-20 and convert $500 to EUR"}'
agentcore configure
agentcore dev
aws configure
agentcore configure
agentcore configure
agentcore dev
agentcore configure
agentcore dev
agentcore configure
agentcore dev
agentcore invoke --dev '{"message": "Show me hotels in Barcelona under $200 per night"}'
agentcore invoke '{"message": "Look up Horizon Rewards account hz-002"}'
agentcore invoke '{"message": "What are the loyalty points for member hz-001?"}'
aws logs tail /aws/bedrock-agentcore/runtimes/WanderBot-RwdOTw2AS5-DEFAULT --log-stream-name-prefix "2026/09/25/[runtime-logs" --follow 
aws iam list-role-policies   --role-name AmazonBedrockAgentCoreGatewayDefaultServiceRole1789998500206
aws iam list-attached-role-policies \  --role-name AmazonBedrockAgentCoreGatewayDefaultServiceRole1789998500206
aws iam list-attached-role-policies --role-name AmazonBedrockAgentCoreGatewayDefaultServiceRole1789998500206
aws iam get-policy   --policy-arn arn:aws:iam::102959685868:policy/service-role/AmazonBedrockAgentCoreGatewayBasePolicyProd_28A543
aws iam get-policy-version   --policy-arn arn:aws:iam::102959685868:policy/service-role/AmazonBedrockAgentCoreGatewayBasePolicyProd_28A543   --version-id v1
ws secretsmanager list-secrets   --region us-east-1   --output table
aws secretsmanager list-secrets   --region us-east-1   --output table
aws iam put-role-policy   --role-name AmazonBedrockAgentCoreGatewayDefaultServiceRole1789998500206   --policy-name WanderBotLoyaltyApiKeyAccess   --policy-document file://agentcore-api-key-policy.json
aws iam put-role-policy   --role-name AmazonBedrockAgentCoreGatewayDefaultServiceRole1789998500206   --policy-name WanderBotLoyaltyApiKeyAccess   --policy-document file://agentcore-api-key-policy.jsonaws iam put-role-policy   --role-name AmazonBedrockAgentCoreGatewayDefaultServiceRole1789998500206   --policy-name WanderBotLoyaltyApiKeyAccess   --policy-document file://agentcore-api-key-policy.json
clear
aws iam put-role-policy   --role-name AmazonBedrockAgentCoreGatewayDefaultServiceRole1789998500206   --policy-name WanderBotLoyaltyApiKeyAccess \
agentcore invoke '{"message": "What are the loyalty points for member hz-001?"}'
agentcore deploy
agentcore configure
agentcore deploy --auto-update-on-conflict
agentcore invoke '{"message": "What are the loyalty points for member hz-001?"}'
aws logs tail /aws/bedrock-agentcore/runtimes/WanderBot-RwdOTw2AS5-DEFAULT --log-stream-name-prefix "2026/09/25/[runtime-logs" --follow
agentcore invoke '{"message": "What are the loyalty points for member hz-001?"}'
aws logs tail /aws/bedrock-agentcore/runtimes/WanderBot-RwdOTw2AS5-DEFAULT --log-stream-name-prefix "2026/09/25/[runtime-logs" --follow
curl -H "x-api-key: YOUR_ACTUAL_API_KEY" \"https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod/loyalty/hz-001"
curl -H "x-api-key: pYVpCUQOBg6krrp1rA1nX4esq6BvPzb69pgaqqh2" "https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod/loyalty/hz-001"
curl -H "x-api-key: pYVpCUQOBg6krrp1rA1nX4esq6BvPzb69pgaqqh2" "https://wanderbot-loyalty-api.execute-api.us-east-1.amazonaws.com/prod/loyalty/hz-001"
curl -H "x-api-key: pYVpCUQOBg6krrp1rA1nX4esq6BvPzb69pgaqqh2" "https://wanderbot-loyalty-points-api.execute-api.us-east-1.amazonaws.com/prod/loyalty/hz-001"
curl -H "x-api-key: pYVpCUQOBg6krrp1rA1nX4esq6BvPzb69pgaqqh2" "arn:aws:execute-api:us-east-1:102959685868:un7xstrum9/*/GET/loyalty/hz-001"
curl -H "x-api-key: pYVpCUQOBg6krrp1rA1nX4esq6BvPzb69pgaqqh2" "https://un7xstrum9.execute-api.us-east-1.amazonaws.com/prod/loyalty/hz-001"
aws bedrock-agentcore-control get-gateway-target   --gateway-identifier wanderbot-gateway-rhqopos9qz   --target-id KRA7Y0CJVU   --region us-east-1
gentcore invoke '{"message": "Look up Horizon Rewards account hz-002"}'
clear
aws iam put-role-policy   --role-name AmazonBedrockAgentCoreGatewayDefaultServiceRole1789998500206   --policy-name WanderBotLoyaltyApiKeyAccess   --policy-document file://agentcore-api-key-policy.json
awd configure
aws configure
agentcore configure
agentcore configure
agentcore deploy --auto-update-on-conflict
agentcore invoke '{"message": "Hi, I am Alice. I love luxury travel and Japanese cuisine.", "actor_id": "alice-001"}'
aws logs tail /aws/bedrock-agentcore/runtimes/WanderBot-RwdOTw2AS5-DEFAULT --log-stream-name-prefix "2026/09/28/[runtime-logs" --follow
agentcore invoke '{"message": "Hi, I am Alice. I love luxury travel and Japanese cuisine.", "actor_id": "alice-001"}'
aws iam get-role-policy   --role-name AmazonBedrockAgentCoreSDKRuntime-us-east-1-a25b0cb827   --policy-name WanderBotMemoryAccess
agentcore invoke '{"message": "Hi, I am Alice. I love luxury travel and Japanese cuisine.", "actor_id": "alice-001"}'
agentcore stop-session
agentcore invoke '{"message": "My budget is around $5000 per trip.", "actor_id": "alice-001"}'
agentcore invoke '{"message": "Hi, I am Alice. I love luxury travel and Japanese cuisine.", "actor_id": "alice-001"}'
agentcore invoke '{"message": "My budget is around $5000 per trip.", "actor_id": "alice-001"}'
agentcore stop-session
agentcore invoke '{"message": "My budget is around $5000 per trip.", "actor_id": "alice-001"}'
agentcore stop-session
agentcore invoke '{"message": "what do you remember about my trip detail.", "actor_id": "alice-001"}'
agentcore invoke '{"message": "i prefer window seat and im lactose intolernat", "actor_id": "xyuu-001"}'
agentcore stop-session
agentcore invoke '{"message": "Recommend a meal option for my upcoming flight.", "actor_id": "xyuu-001"}'
agentcore memory browser
agentcore memory browse
aws configure
agentcore configure
agentcore deploy --auto-update-on-conflict
agentcore invoke '{"message": "2 rooms for 5 nights at $180/night, plus 12% tax. Total?"}'
agentcore invoke '{"message": "Solo stay: 3 nights at $95/night with breakfast $18/day."}'
agentcore invoke '{"message": "3 nights at $180 for room A, 4 night at 220 for room B, 12% vat, plus 5% loyalty discount applied after tax. total in eur at 0.92 rate"}'
agentcore invoke '{"message": "how many nights between 2026-6-10 - 2026-06-19"}'
aws logs tail /aws/bedrock-agentcore/runtimes/WanderBot-RwdOTw2AS5-DEFAULT --log-stream-name-prefix "2026/09/29/[runtime-logs" --follow   
agentcore configure
agentcore deploy
agentcore invoke '{"prompt": "Can you track order ORD-001?", "customer_id": "CUST-123", "session_id": "t1"}'
aws logs tail /aws/bedrock-agentcore/runtimes/CustomerSupportBot-5uiycrCo8g-DEFAULT --log-stream-name-prefix "2026/09/30/[runtime-logs" --follow  
agentcore configure
agentcore deploy
agentcore invoke '{"prompt": "Can you track order ORD-001?", "customer_id": "CUST-123", "session_id": "t1"}'
agentcore configure
agentcore deploy
agentcore invoke '{"prompt": "Can you track order ORD-001?", "customer_id": "CUST-123", "session_id": "t1"}'
agentcore configure
agentcore deploy
agentcore invoke '{"prompt": "Can you track order ORD-001?", "customer_id": "CUST-123", "session_id": "t1"}'
agentcore dev invoke '{"prompt": "I am a Gold member with 4250 points. Calculate my discount on a $150 order.", "customer_id": "CUST-123", "session_id": "s1"}'
uv pip install _sqlite3
uv pip install sqlite3
uv run main.py '{"prompt": "Hello", "customer_id": "CUST-123", "session_id": "s1"}'
which -a python python3 python3.12 python3.13
/usr/bin/python3 -c "import sys, sqlite3; print(sys.version); print(sqlite3.sqlite_version)"
/voc/work/.venv/bin/python -c "import sys, sqlite3; print(sys.version); print(sqlite3.sqlite_version)"
deactivate 2>/dev/null || true
uv python install 3.13[A
