import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'AIAD Documentation',
  description: 'Documentation for AI Artist Database',
  
  // Bilingual support
  locales: {
    root: {
      label: 'English',
      lang: 'en-US',
      themeConfig: {
        nav: [
          { text: 'Home', link: '/' },
          { text: 'Guide', link: '/guide/' },
          { text: 'API', link: '/api/' },
        ],
        sidebar: [
          {
            text: 'Introduction',
            items: [
              { text: 'Getting Started', link: '/guide/' },
              { text: 'Architecture', link: '/guide/architecture' },
            ]
          },
          {
            text: 'Components',
            items: [
              { text: 'Backend', link: '/guide/backend' },
              { text: 'Frontend', link: '/guide/frontend' },
              { text: 'Scraper', link: '/guide/scraper' },
            ]
          }
        ]
      }
    },
    zh: {
      label: '中文',
      lang: 'zh-CN',
      link: '/zh/',
      themeConfig: {
        nav: [
          { text: '首页', link: '/zh/' },
          { text: '指南', link: '/zh/guide/' },
          { text: 'API', link: '/zh/api/' },
        ],
        sidebar: [
          {
            text: '介绍',
            items: [
              { text: '快速开始', link: '/zh/guide/' },
              { text: '架构', link: '/zh/guide/architecture' },
            ]
          },
          {
            text: '组件',
            items: [
              { text: '后端', link: '/zh/guide/backend' },
              { text: '前端', link: '/zh/guide/frontend' },
              { text: '爬虫', link: '/zh/guide/scraper' },
            ]
          }
        ]
      }
    }
  },

  themeConfig: {
    logo: '/logo.png',
    socialLinks: [
      { icon: 'github', link: 'https://github.com/thevertexlab/aiad' }
    ],
    footer: {
      message: 'AIAD - AI Artist Database',
      copyright: 'Copyright © 2023-present'
    }
  }
}) 