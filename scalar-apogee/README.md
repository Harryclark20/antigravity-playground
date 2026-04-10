<p align="center">
  <img src="https://img.shields.io/badge/Next.js-16.1.6-black?logo=next.js" alt="Next.js"/>
  <img src="https://img.shields.io/badge/TypeScript-5-blue?logo=typescript" alt="TypeScript"/>
  <img src="https://img.shields.io/badge/Recharts-2.x-green?logo=recharts" alt="Recharts"/>
  <img src="https://img.shields.io/badge/Deployed_on-Vercel-black?logo=vercel" alt="Vercel"/>
  <img src="https://img.shields.io/badge/license-MIT-purple" alt="MIT"/>
</p>

<h1 align="center">🏢 NexusERP</h1>
<p align="center">
  A modern, full-featured <strong>Enterprise Resource Planning</strong> web application built with Next.js 14.<br/>
  Beautiful dark glassmorphism UI, interactive charts, and 8 fully functional business modules.
</p>

<p align="center">
  <a href="https://nexus-erp-pi.vercel.app"><strong>🌐 Live Demo → nexus-erp-pi.vercel.app</strong></a>
</p>

---

## ✨ Features

- **8 ERP Modules** — Dashboard, Inventory, Sales, Customers, Finance, HR, Reports, Settings
- **Dark Glassmorphism UI** — navy + electric indigo palette with CSS custom properties
- **Interactive Charts** — Area, Bar, Line, Pie & Radar charts via Recharts
- **Live Search & Filters** — instant client-side filtering on every data table
- **Animated KPI Cards** — hover lifts, gradient accents, trend badges
- **Fully Responsive** — mobile, tablet, and desktop layouts
- **SEO Optimised** — meta title, description & keywords on every page
- **Auto-Deploy** — every push to `master` triggers a Vercel deployment

---

## 📦 Modules

| Module | Route | What's inside |
|---|---|---|
| Dashboard | `/` | KPI summary, revenue/expense chart, category pie, recent orders & activity |
| Inventory | `/inventory` | SKU table, stock chart, low-stock + out-of-stock alerts, live search |
| Sales & Orders | `/sales` | Order trend chart, status filter tabs, payment methods |
| Customers | `/customers` | VIP/Premium/Regular tiers, LTV, email & phone display |
| Finance | `/finance` | P&L trend, expense breakdown bars, transactions ledger |
| HR | `/hr` | Employee card grid, department bar chart, payroll breakdown |
| Reports | `/reports` | Revenue forecast, customer growth, top products, radar health score |
| Settings | `/settings` | Company info, notification toggles, 2FA security, users & roles |

---

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- npm 9+

### Local Development

```bash
# Clone the repo
git clone https://github.com/Harryclark20/nexus-erp.git
cd nexus-erp

# Install dependencies
npm install

# Start dev server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
npm run build
npm start
```

---

## 🛠 Tech Stack

| Technology | Purpose |
|---|---|
| [Next.js 16](https://nextjs.org) | React framework (App Router, SSG) |
| [TypeScript](https://typescriptlang.org) | Type safety |
| [Recharts](https://recharts.org) | Interactive data charts |
| [Lucide React](https://lucide.dev) | Icon library |
| [Vanilla CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) | Custom design system (no Tailwind) |
| [Vercel](https://vercel.com) | Hosting & CI/CD |

---

## 📁 Project Structure

```
nexus-erp/
├── app/
│   ├── layout.tsx          # Root layout (Sidebar + Topbar)
│   ├── globals.css         # Full design system
│   ├── page.tsx            # Dashboard
│   ├── inventory/page.tsx
│   ├── sales/page.tsx
│   ├── customers/page.tsx
│   ├── finance/page.tsx
│   ├── hr/page.tsx
│   ├── reports/page.tsx
│   └── settings/page.tsx
├── components/
│   ├── Sidebar.tsx
│   └── Topbar.tsx
└── vercel.json
```

---

## 🚢 Deployment

The app automatically deploys to Vercel on every push to `master`.

To deploy your own instance:
1. Fork this repository
2. Import the fork at [vercel.com/new](https://vercel.com/new)
3. Vercel auto-detects Next.js — click **Deploy**

---

## 📄 License

MIT — free to use for personal and commercial projects.

---

<p align="center">Built with ❤️ using <a href="https://nextjs.org">Next.js</a> & <a href="https://vercel.com">Vercel</a></p>
