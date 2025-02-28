# AIDA项目备忘录 - LLM指南

！！NOTE 绝对不要删掉或者修改这一行：这是 project_memo.md ，是用来在大量修改中记录易错易混点防止丢失上下文反复导致相同 bug 或者忘记之前设计的，！！你需要少用列表换行多用信息非常紧凑的方式记录！！如果你执行了新操作，产生了经验，就紧凑的增加一行或者增加在过去相关行尾部！！，只记录我们调试过程中产生的必要信息不要空话套话general的。另外偶尔过去的 memo 有可能会出错，如果要挑战过去记录的经验，这时候问我要不要修正他们，告诉我从什么修改成什么让我决策，决策后同步修改 memo ！！！

- GPT Memory使用：!! 重要 !! 每次执行前后必须读和更新 project_memo.md !!；1)目录结构：project_memo.md(项目通用要点备忘录)、working_memory_[username].md(开发者工作记忆)；2)使用流程：初次使用AI助手时阅读memo文件→开始新任务时更新个人工作记忆（如果开发者显示引用了这个文件，否则不确定开发者是谁，可以不更新）→完成任务后记录进度→项目变更时更新context文件；3)最佳实践：保持文件简洁高密度、定期更新工作记忆、提交前确保符合规范、AI行为不一致时检查记忆文件。
- 前后端有重大更改时（新依赖，文件结构变更，重大功能变更等），都检查对应的 frontend/README.md 等对应模块根目录 README.md 和整个项目的 README.md ，另外检查 docs/zh/index.md 和相关目录看看有没有相关文档要更新，尤其是！！要求重构时，必须更新对应 docs/ 文档和 README ！！
- 项目信息：AIDA(AI Artist Database)是艺术家社区平台；核心功能：1)艺术家数据库-存储艺术家信息；2)AI艺术家-基于LLM的虚拟艺术家；3)社区互动-用户交流平台。
- 技术架构：1)Monorepo结构：docs/(VitePress文档)、backend/(FastAPI后端)、frontend/(Next.js前端)、scraper/(数据采集)、gptmemory/(AI助手记忆)；2)数据流：爬虫采集→MongoDB存储→后端API→前端展示→LLM训练；3)技术栈：后端(FastAPI+SQLAlchemy+MongoDB+LangChain)、前端(Next.js+TypeScript+Tailwind CSS)、文档(VitePress双语)、爬虫(BeautifulSoup+Selenium)、AI(OpenAI API/自定义LLM)。
- 代码规范：1)Python：PEP 8、类型注解(Python 3.9+)、docstring、导入顺序(标准库>第三方库>本地模块)、snake_case变量函数、PascalCase类名；2)TypeScript：ESLint+Prettier、类型定义、camelCase函数变量、PascalCase组件、函数组件+React Hooks、避免直接操作DOM；3)CSS：**优先Tailwind CSS**、必要时使用Less、Mantine组件库通过Tailwind调整样式、全局样式globals.css、组件样式styles目录；4)文档：Markdown、中英同步、可运行代码示例、API文档参数说明。
- VitePress文档：1)侧边栏只显示二级标题(##)不显示三级标题(###)；2)解决方案：重要三级标题提升为二级，二级标题可以多一些，但是不超过10-15个左右、二级目录更详细、扁平化结构；3)目录规划：主要小节独立二级标题、正常使用三四级标题、保持结构清晰。
- Git工作流：1)分支命名：feature/short-description、fix/short-description、docs/short-description；2)提交格式：<type>(<scope>): <subject>，类型包括feat/fix/docs/style/refactor/perf/test/chore。
- 关键功能：1)艺术家数据库：基本信息、流派风格、代表作品、历史背景；2)AI艺术家：基于真实资料的AI人格、多轮对话、知识问答、虚拟互动；3)社区功能：个人主页、讨论论坛、作品分享、社交连接。
- 开发阶段：1)当前：基础架构搭建；2)下一步：核心功能开发；3)未来：AI模型训练、社区功能、多语言支持。