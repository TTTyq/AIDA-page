# 前端开发

本指南提供了 AIDA 平台的前端架构、技术栈和开发工作流程的相关信息。

## 技术栈

AIDA 前端使用以下技术构建：

- **Next.js**：用于服务器渲染应用的 React 框架
- **TypeScript**：类型安全的 JavaScript
- **Mantine**：React UI 组件库
- **Tailwind CSS**：实用优先的 CSS 框架
- **Less**：用于高级样式的 CSS 预处理器
- **Jotai**：React 原子状态管理
- **SWR**：用于数据获取的 React Hooks
- **Axios**：基于 Promise 的 HTTP 客户端

## 项目结构

```
frontend/
├── app/                 # Next.js 应用目录
│   ├── (routes)/        # 应用路由（分组组织）
│   │   ├── page.tsx     # 首页
│   │   ├── table/       # 数据表格页面
│   │   └── test/        # API 测试页面
│   ├── api/             # API 路由处理器
│   ├── layout.tsx       # 根布局
│   ├── globals.css      # 全局 CSS 样式
│   ├── metadata.ts      # 应用元数据
│   ├── page.tsx         # 根页面
│   ├── services/        # API 服务
│   └── store/           # 状态管理
├── components/          # 可复用的 React 组件
│   ├── ui/              # 基础 UI 组件
│   ├── layout/          # 布局组件
│   ├── forms/           # 表单组件
│   └── features/        # 特定功能组件
├── hooks/               # 自定义 React 钩子
├── lib/                 # 实用函数和常量
│   ├── utils.ts         # 通用实用函数
│   └── constants.ts     # 应用常量
├── services/            # API 服务
│   ├── api.ts           # API 客户端
│   └── endpoints/       # API 端点服务
├── store/               # 状态管理
│   ├── atoms.ts         # Jotai 原子
│   └── selectors.ts     # 派生状态选择器
├── styles/              # 全局样式
│   ├── globals.css      # 全局 CSS
│   └── globals.less     # 全局 Less 样式
├── types/               # TypeScript 类型定义
│   ├── api.ts           # API 响应类型
│   ├── models.ts        # 数据模型类型
│   └── common.ts        # 通用类型定义
├── public/              # 静态资源
├── tailwind.config.js   # Tailwind CSS 配置
├── postcss.config.js    # PostCSS 配置
├── next.config.js       # 带有 Less 支持的 Next.js 配置
└── package.json         # 项目依赖
```

## 状态管理

应用使用 Jotai 进行状态管理。Jotai 提供了一种原子化的 React 状态管理方法，使得以可预测的方式管理和更新状态变得容易。

```tsx
// 使用 Jotai 原子的示例
import { useAtom } from 'jotai';
import { artistsAtom } from '../store/atoms';

function ArtistList() {
  const [artists, setArtists] = useAtom(artistsAtom);
  // ...
}
```

## 样式

应用使用 Mantine 组件、Tailwind CSS 工具类和 Less 的组合进行样式设计：

- **Tailwind CSS**：主要的样式设计方法，使用工具类
- **Mantine**：提供预构建的 React 组件
- **Less**：用于 Tailwind 无法实现的复杂样式

```tsx
// 使用 Mantine 和 Tailwind CSS 的示例
import { Button } from '@mantine/core';

function MyComponent() {
  return (
    <Button className="mt-4 hover:shadow-lg">
      点击我
    </Button>
  );
}
```

## API 集成

前端使用 Axios 与后端 API 通信。API 服务定义在 `app/services/api.ts` 中：

```tsx
// API 服务示例
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const artistService = {
  getArtists: async () => {
    const response = await api.get('/artists');
    return response.data;
  },
  // ...
};
```

## 开发工作流程

1. 启动开发服务器：
   ```bash
   npm run dev
   ```

2. 在浏览器中打开 [http://localhost:3000](http://localhost:3000) 查看应用。

3. 修改代码，在浏览器中查看变化。

4. 运行代码检查以确保代码质量：
   ```bash
   npm run lint
   ```

5. 为生产环境构建应用：
   ```bash
   npm run build
   ``` 