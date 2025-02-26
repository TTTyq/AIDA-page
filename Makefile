# AIAD Project Makefile

.PHONY: setup start stop dev-backend dev-frontend dev-docs help

# 颜色定义
BLUE=\033[0;34m
GREEN=\033[0;32m
YELLOW=\033[0;33m
RED=\033[0;31m
NC=\033[0m # No Color

# 默认目标
help:
	@echo "${BLUE}AIAD 项目管理命令${NC}"
	@echo ""
	@echo "${GREEN}可用命令:${NC}"
	@echo "  ${YELLOW}make setup${NC}      - 安装所有组件的依赖"
	@echo "  ${YELLOW}make start${NC}      - 启动所有服务 (后端、前端、文档)"
	@echo "  ${YELLOW}make stop${NC}       - 停止所有服务"
	@echo "  ${YELLOW}make dev-backend${NC} - 仅启动后端服务"
	@echo "  ${YELLOW}make dev-frontend${NC} - 仅启动前端服务"
	@echo "  ${YELLOW}make dev-docs${NC}    - 仅启动文档服务"
	@echo ""

# 安装所有依赖
setup:
	@echo "${BLUE}安装后端依赖...${NC}"
	cd backend && python -m venv venv && \
	. venv/bin/activate && pip install -r requirements.txt
	@echo "${BLUE}安装前端依赖...${NC}"
	cd frontend && npm install
	@echo "${BLUE}安装文档依赖...${NC}"
	cd docs && npm install
	@echo "${GREEN}所有依赖安装完成!${NC}"

# 启动所有服务
start:
	@echo "${BLUE}启动所有服务...${NC}"
	@mkdir -p ./.pid
	@# 启动后端
	cd backend && . venv/bin/activate && \
	python -m uvicorn main:app --reload --port 8000 & echo $$! > ./.pid/backend.pid
	@echo "${GREEN}后端服务已启动 - http://localhost:8000${NC}"
	@# 启动前端
	cd frontend && npm run dev & echo $$! > ./.pid/frontend.pid
	@echo "${GREEN}前端服务已启动 - http://localhost:3000${NC}"
	@# 启动文档
	cd docs && npm run dev & echo $$! > ./.pid/docs.pid
	@echo "${GREEN}文档服务已启动 - http://localhost:5173${NC}"
	@echo "${YELLOW}所有服务已启动，使用 'make stop' 停止所有服务${NC}"

# 停止所有服务
stop:
	@echo "${BLUE}停止所有服务...${NC}"
	@if [ -f ./.pid/backend.pid ]; then \
		kill -9 `cat ./.pid/backend.pid` 2>/dev/null || true; \
		rm ./.pid/backend.pid; \
		echo "${GREEN}后端服务已停止${NC}"; \
	fi
	@if [ -f ./.pid/frontend.pid ]; then \
		kill -9 `cat ./.pid/frontend.pid` 2>/dev/null || true; \
		rm ./.pid/frontend.pid; \
		echo "${GREEN}前端服务已停止${NC}"; \
	fi
	@if [ -f ./.pid/docs.pid ]; then \
		kill -9 `cat ./.pid/docs.pid` 2>/dev/null || true; \
		rm ./.pid/docs.pid; \
		echo "${GREEN}文档服务已停止${NC}"; \
	fi
	@echo "${GREEN}所有服务已停止${NC}"

# 仅启动后端
dev-backend:
	@echo "${BLUE}启动后端服务...${NC}"
	cd backend && . venv/bin/activate && \
	python -m uvicorn main:app --reload --port 8000
	@echo "${GREEN}后端服务已启动 - http://localhost:8000${NC}"

# 仅启动前端
dev-frontend:
	@echo "${BLUE}启动前端服务...${NC}"
	cd frontend && npm run dev
	@echo "${GREEN}前端服务已启动 - http://localhost:3000${NC}"

# 仅启动文档
dev-docs:
	@echo "${BLUE}启动文档服务...${NC}"
	cd docs && npm run dev
	@echo "${GREEN}文档服务已启动 - http://localhost:5173${NC}" 