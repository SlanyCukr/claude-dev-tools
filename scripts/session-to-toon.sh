#!/bin/bash
# session-to-toon.sh - Convert Claude Code session JSONL to TOON format
# Usage: session-to-toon.sh <session-id> [output-file]
#
# Strips: tool details, system messages, file contents, repetitive patterns
# Outputs: Clean TOON format for AI analysis

set -euo pipefail

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1" >&2; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1" >&2; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

# Validate dependencies
command -v jq >/dev/null 2>&1 || { log_error "jq is required but not installed"; exit 1; }

# Parse arguments
SESSION_ID="${1:-}"
OUTPUT_FILE="${2:-}"

# Validate output file path (prevent command injection)
if [[ -n "$OUTPUT_FILE" ]]; then
    if [[ "$OUTPUT_FILE" =~ [\;\&\|\$\`\<\>] ]]; then
        log_error "Invalid output file path. Must not contain shell metacharacters."
        exit 1
    fi
fi

if [[ -z "$SESSION_ID" ]]; then
    echo "Usage: session-to-toon.sh <session-id> [output-file]"
    echo ""
    echo "Arguments:"
    echo "  session-id   The UUID of the session to analyze"
    echo "  output-file  Optional output file (default: stdout)"
    echo ""
    echo "Examples:"
    echo "  session-to-toon.sh abc123-def456"
    echo "  session-to-toon.sh abc123-def456 /tmp/session.toon"
    exit 1
fi

# Validate session ID format (UUID-like, alphanumeric with hyphens)
if [[ ! "$SESSION_ID" =~ ^[a-zA-Z0-9-]+$ ]]; then
    log_error "Invalid session ID format. Must be alphanumeric with hyphens."
    exit 1
fi

# Find session file in ~/.claude/projects/*/
CLAUDE_PROJECTS="$HOME/.claude/projects"
SESSION_FILE=""
PROJECT_DIR=""

for dir in "$CLAUDE_PROJECTS"/*; do
    if [[ -d "$dir" ]]; then
        candidate="$dir/$SESSION_ID.jsonl"
        if [[ -f "$candidate" ]]; then
            SESSION_FILE="$candidate"
            PROJECT_DIR="$dir"
            break
        fi
    fi
done

if [[ -z "$SESSION_FILE" ]]; then
    log_error "Session '$SESSION_ID' not found in $CLAUDE_PROJECTS/*/"
    log_info "Available sessions in most recent project:"
    # Show recent sessions
    RECENT_PROJECT=$(ls -td "$CLAUDE_PROJECTS"/*/ 2>/dev/null | head -1)
    if [[ -n "$RECENT_PROJECT" ]]; then
        ls -t "$RECENT_PROJECT"/*.jsonl 2>/dev/null | head -5 | while read -r f; do
            basename "$f" .jsonl
        done
    fi
    exit 1
fi

log_info "Found session: $SESSION_FILE"

# Find related agent files (they have the same sessionId in their content)
AGENT_FILES=()
shopt -s nullglob  # Make globs that don't match expand to nothing
for agent_file in "$PROJECT_DIR"/agent-*.jsonl; do
    # Check if this agent belongs to our session
    if jq -e --arg sid "$SESSION_ID" 'select(.sessionId == $sid)' "$agent_file" >/dev/null 2>&1; then
        AGENT_FILES+=("$agent_file")
    fi
done
shopt -u nullglob  # Reset nullglob

log_info "Found ${#AGENT_FILES[@]} related agent transcript(s)"

# Function to extract and format messages from a JSONL file
process_jsonl() {
    local file="$1"
    local is_agent="${2:-false}"
    local agent_id=""

    if [[ "$is_agent" == "true" ]]; then
        agent_id=$(basename "$file" .jsonl | sed 's/agent-//')
    fi

    jq -r --arg is_agent "$is_agent" --arg agent_id "$agent_id" '
        # Skip meta messages and file-history-snapshot
        select(.type != null and .type != "file-history-snapshot" and .isMeta != true) |

        # Extract timestamp
        .timestamp as $ts |

        # Determine role/type
        (if .type == "user" then "USER"
         elif .type == "assistant" then "ASSISTANT"
         elif .type == "tool_result" then "TOOL_RESULT"
         else .type | ascii_upcase
         end) as $role |

        # Process message content
        (if .message.content then
            # Handle array of content blocks
            if (.message.content | type) == "array" then
                [.message.content[] |
                    # Skip thinking blocks and signatures
                    select(.type != "thinking" and .type != "signature" and .signature == null) |

                    # Format based on type
                    if .type == "text" then
                        # Clean up system reminders and command XML tags from text
                        .text | gsub("<system-reminder>[^<]*</system-reminder>"; "")
                              | gsub("<command-name>[^<]*</command-name>"; "")
                              | gsub("<command-message>[^<]*</command-message>"; "")
                              | gsub("<command-args>[^<]*</command-args>"; "")
                              | gsub("<local-command-stdout>[^<]*</local-command-stdout>"; "")
                              | gsub("\\s*\\n\\s*\\n\\s*"; "\n")
                              | gsub("^\\s+|\\s+$"; "")
                    elif .type == "tool_use" then
                        # Summarize tool use
                        "→ Tool: \(.name)(" + (
                            if .name == "Read" then .input.file_path
                            elif .name == "Write" then .input.file_path
                            elif .name == "Edit" then .input.file_path
                            elif .name == "Bash" then (.input.command | .[0:80] | gsub("\\n"; " "))
                            elif .name == "Grep" then .input.pattern
                            elif .name == "Glob" then .input.pattern
                            elif .name == "Task" then "\(.input.subagent_type): \(.input.description // .input.prompt[0:50])"
                            elif .name == "WebFetch" then .input.url
                            elif .name == "WebSearch" then .input.query
                            elif .name == "TodoWrite" then "update todos"
                            elif .name == "AskUserQuestion" then "asking user"
                            else (.input | tostring | .[0:60])
                            end
                        ) + ")"
                    elif .type == "tool_result" then
                        # Truncate tool results
                        "← Result: " + ((.content // .output // "") | tostring | .[0:100] | gsub("\\n"; " ")) + "..."
                    else
                        (.text // .content // "" | tostring | .[0:200])
                    end
                ] | map(select(. != "" and . != null)) | join("\n")
            else
                # Plain string content
                .message.content | tostring
                    | gsub("<system-reminder>[^<]*</system-reminder>"; "")
                    | gsub("<command-name>[^<]*</command-name>"; "")
                    | gsub("<command-message>[^<]*</command-message>"; "")
                    | gsub("<command-args>[^<]*</command-args>"; "")
                    | gsub("<local-command-stdout>[^<]*</local-command-stdout>"; "")
                    | gsub("\\s*\\n\\s*\\n\\s*"; "\n")
                    | .[0:500]
            end
         elif .message.role == "user" then
            .message.content // ""
         else ""
         end) as $content |

        # Skip empty content
        select($content != "" and $content != null) |

        # Format output with agent prefix if applicable
        (if $is_agent == "true" then "[AGENT:\($agent_id)] " else "" end) +
        "[\($ts | split("T")[1] | split(".")[0] // "??:??:??")] \($role):\n\($content)"
    ' "$file" 2>/dev/null || true
}

# Post-process to collapse repeated tool calls (same tool within 3 lines)
collapse_repeated_tools() {
    awk '
    BEGIN {
        prev_tool = ""
        count = 0
        first_line = ""
        lines_since_tool = 0
    }
    /→ Tool: / {
        # Extract tool name (everything before the opening paren)
        if (match($0, /→ Tool: ([^(]+)\(/, arr)) {
            tool_name = arr[1]
        } else {
            tool_name = $0
        }

        if (tool_name == prev_tool && lines_since_tool <= 2) {
            count++
            lines_since_tool = 0
            next  # Skip this duplicate tool line
        } else {
            # Print previous collapsed tool if needed
            if (count > 1) {
                print first_line " [+" (count-1) " similar]"
            } else if (count == 1) {
                print first_line
            }
            # Start new tool tracking
            prev_tool = tool_name
            first_line = $0
            count = 1
            lines_since_tool = 0
        }
        next
    }
    {
        lines_since_tool++
        # If too many lines since last tool, flush pending
        if (lines_since_tool > 2 && count > 0) {
            if (count > 1) {
                print first_line " [+" (count-1) " similar]"
            } else {
                print first_line
            }
            prev_tool = ""
            count = 0
            first_line = ""
        }
        print
    }
    END {
        if (count > 1) {
            print first_line " [+" (count-1) " similar]"
        } else if (count == 1) {
            print first_line
        }
    }
    '
}

# Generate TOON output
generate_toon() {
    # Header
    cat << EOF
metadata:
  session_id: $SESSION_ID
  project_dir: $(basename "$PROJECT_DIR")
  conversion_date: $(date -Iseconds)
  agent_count: ${#AGENT_FILES[@]}

EOF

    echo "messages:"
    echo ""

    # Process main session
    echo "# === MAIN SESSION ==="
    process_jsonl "$SESSION_FILE" "false"
    echo ""

    # Process agent transcripts
    for agent_file in "${AGENT_FILES[@]}"; do
        agent_id=$(basename "$agent_file" .jsonl | sed 's/agent-//')
        echo ""
        echo "# === AGENT: $agent_id ==="
        process_jsonl "$agent_file" "true"
    done
}

# Output (with post-processing to collapse repeated tools)
if [[ -n "$OUTPUT_FILE" ]]; then
    generate_toon | collapse_repeated_tools > "$OUTPUT_FILE"
    log_info "TOON output written to: $OUTPUT_FILE"
else
    generate_toon | collapse_repeated_tools
fi
