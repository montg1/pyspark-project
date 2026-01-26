# Wine Reviews Dashboard - Vue 3 Frontend

A beautiful, interactive Vue 3 dashboard for exploring wine reviews data processed by the PySpark ETL pipeline and served via FastAPI.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm/yarn
- FastAPI backend running on `http://localhost:8000`

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

Server runs at `http://localhost:5173` with hot module replacement.

### Build for Production

```bash
npm run build
npm run preview
```

## 📦 Dependencies

- **Vue 3** - Progressive JavaScript framework
- **Vite** - Next generation frontend tooling
- **Axios** - HTTP client for API calls
- **Chart.js** - Data visualization library
- **TailwindCSS** - Utility-first CSS framework

## 🎨 Features

- 📊 **Statistics Cards** - Key metrics (total wines, quality distribution, pricing)
- 📈 **Interactive Charts** - Quality distribution (doughnut) and price breakdown (bar chart)
- 📋 **Data Tables** - Top varieties and countries with detailed statistics
- 🔄 **Live Updates** - Auto-refresh data every 30 seconds
- 📱 **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- 🎯 **API Integration** - Seamless connection to FastAPI backend

## 🏗️ Project Structure

```
frontend/
├── src/
│   ├── components/          # Vue components
│   │   ├── StatsCard.vue
│   │   ├── QualityChart.vue
│   │   ├── PriceChart.vue
│   │   ├── TopVarietiesTable.vue
│   │   └── CountriesTable.vue
│   ├── api/
│   │   └── client.js        # Axios API client
│   ├── styles/
│   │   └── main.css         # Global styles with TailwindCSS
│   ├── App.vue              # Root component
│   └── main.js              # Entry point
├── index.html               # HTML template
├── package.json             # Dependencies
├── vite.config.js           # Vite configuration
├── tailwind.config.js       # TailwindCSS configuration
└── postcss.config.js        # PostCSS configuration
```

## 🔗 API Connection

The frontend proxies requests to the FastAPI backend:

- Development: `http://localhost:8000`
- The Vite dev server proxies `/api/*` requests automatically

## 📊 Dashboard Components

### Statistics Cards
Display key metrics with icons and color-coded backgrounds:
- Total wines count
- Excellent quality wines
- Good quality wines
- Average price across all countries

### Charts
- **Quality Chart**: Doughnut chart showing wine distribution by quality category
- **Price Chart**: Bar chart showing wine distribution by price range

### Data Tables
- **Top Varieties**: Top 15 wine varieties by count
- **Top Countries**: Top 10 producing countries with statistics

## 🔄 Data Refresh

Dashboard automatically refreshes data every 30 seconds to reflect any updates from the backend.

## 🛠️ Configuration

### Vite Configuration
- Dev port: 5173
- API proxy: `/api/*` → `http://localhost:8000`
- Vue 3 plugin enabled

### TailwindCSS Configuration
- Includes all Vue files in the `src/` directory
- Extends default theme for customization

## 🚀 Deployment

Build the dashboard and deploy the `dist/` directory to any static hosting:

```bash
npm run build
# Upload dist/ folder to your hosting service
```

## 📝 License

MIT
