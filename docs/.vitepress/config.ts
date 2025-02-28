import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'AIDA Documentation',
  description: 'Documentation for AI Artist Database',
  
  // Bilingual support
  locales: {
    root: {
      label: 'English',
      lang: 'en-US',
      link: '/en/',
      themeConfig: {
        nav: [
          { text: 'Home', link: '/en/' },
          { text: 'Guide', link: '/en/guide/' },
          { text: 'API', link: '/en/api/' },
        ],
        sidebar: [
          { text: 'Beginner-Friendly Guide', link: '/en/guide/beginners' },
          {
            text: 'Introduction',
            items: [
              { text: 'Getting Started', link: '/en/guide/' },
              { text: 'Architecture', link: '/en/guide/architecture' },
            ]
          },
          {
            text: 'Components',
            items: [
              { text: 'Backend', link: '/en/guide/backend' },
              { text: 'Frontend', link: '/en/guide/frontend' },
              { text: 'Scraper', link: '/en/guide/scraper' },
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
          { text: '宝宝也能看懂的开发指南', link: '/zh/guide/beginners' },
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
      { icon: 'github', link: 'https://github.com/thevertexlab/aida' }
    ],
    footer: {
      message: 'AIDA - AI Artist Database',
      copyright: 'Copyright © 2023-present'
    }
  }
})