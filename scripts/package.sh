#!/bin/bash
# Redmine MCP Client 打包脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="${SCRIPT_DIR}/dist"
VERSION="1.1.0"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Redmine MCP Client 打包脚本 ===${NC}\n"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 检查必需文件
echo -e "${YELLOW}检查必需文件...${NC}"
REQUIRED_FILES=(
    ".claude-plugin/plugin.json"
    ".mcp.json"
    "commands/redmine.md"
    "skills/redmine-assistant/SKILL.md"
    "skills/redmine-assistant/SKILL-report-builder.md"
    "skills/redmine-assistant/references/mcp-tools.md"
    "skills/redmine-assistant/references/workflows.md"
    "skills/redmine-assistant/references/data-schema.md"
    "README.md"
    "CLAUDE.md"
    "INSTALL.md"
    "REPORT_DEV_GUIDE.md"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$PROJECT_DIR/$file" ]; then
        echo -e "  ${GREEN}✓${NC} $file"
    else
        echo -e "  ${RED}✗${NC} $file (缺失)"
        exit 1
    fi
done

# 打包为 ZIP
echo -e "\n${YELLOW}打包为 ZIP...${NC}"
cd "$PROJECT_DIR"
ZIP_FILE="$OUTPUT_DIR/redmine-mcp-client-${VERSION}.zip"

# 打包必需文件
zip -r "$ZIP_FILE" \
    .claude-plugin/ \
    commands/ \
    skills/ \
    .mcp.json \
    .env.example \
    README.md \
    CLAUDE.md \
    INSTALL.md \
    -x "*.git*" -x "*.pyc" -x "__pycache__/*"

echo -e "${GREEN}✓ 打包完成：$ZIP_FILE${NC}"
echo -e "  文件大小：$(du -h "$ZIP_FILE" | cut -f1)\n"

# 显示安装说明
echo -e "${YELLOW}=== 安装说明 ===${NC}"
echo ""
echo "详细安装说明请参考：INSTALL.md"
echo ""
echo "1. 本地测试安装 (临时加载):"
echo "   claude --plugin-dir $PROJECT_DIR"
echo ""
echo "2. 永久安装:"
echo "   claude plugin marketplace add $PROJECT_DIR"
echo "   claude plugin install redmine-mcp-client"
echo ""
echo "3. 分发 ZIP 包给其他客户端:"
echo "   unzip $ZIP_FILE -d ~/redmine-mcp-client"
echo "   claude plugin marketplace add ~/redmine-mcp-client"
echo "   claude plugin install redmine-mcp-client"
echo ""

echo -e "${GREEN}=== 打包成功 ===${NC}"
