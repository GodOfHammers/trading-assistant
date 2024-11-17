# Stock Trading Dashboard Frontend

## Overview

The Stock Trading Dashboard Frontend is a React-based application that provides users with a comprehensive interface to monitor and manage their stock trading activities. It integrates with a backend API and WebSocket service to fetch real-time data and enable interactive features such as executing trades, setting alerts, and analyzing market trends.

## Key Features

- Real-time stock data updates via WebSocket subscriptions
- Top stock opportunities and trade recommendations
- Detailed stock analysis with technical indicators, sentiment analysis, and risk assessment
- Market analysis with sector performance and volatility metrics
- Active position tracking with real-time updates
- Trade execution and position management (increase, decrease, close)
- Customizable alerts and notifications
- Responsive and intuitive user interface

## Architecture

The frontend application follows a modular architecture, separating concerns into distinct components, services, and utilities. The main components include:

- Dashboard: The main entry point of the application, orchestrating data flow and rendering sub-components.
- StockList: Displays a list of top bullish stocks with key metrics and sorting options.
- TechnicalChart: Renders a technical chart with price, volume, and various technical indicators.
- AnalysisPanel: Presents various analysis sections such as technical analysis, sentiment analysis, profit analysis, and risk assessment.
- MarketAnalysis: Provides market overview, sector analysis, and technical overview tabs with data visualizations.
- TradeRecommendations: Shows a list of trade recommendations with key metrics and trade execution functionality.
- PositionTracker: Tracks active positions in the user's portfolio with real-time updates and position management options.

The application integrates with the backend API using the `stockApi` service, which provides methods for fetching stock data, market data, and executing trades. Real-time updates are handled through the `WebSocketService`, which establishes a WebSocket connection and subscribes to relevant events.

## API Documentation

The frontend interacts with the following backend API endpoints:

- `/api/stocks/:symbol/analyze`: Fetches stock analysis data for a given symbol.
- `/api/stocks/opportunities`: Retrieves top stock opportunities.
- `/api/market/data`: Fetches market data and analysis.
- `/api/trades/execute`: Executes a trade for a specific stock.

For detailed information about the request/response formats and authentication requirements, please refer to the backend API documentation.

## Usage Examples

1. Viewing Top Stock Opportunities:
   - Navigate to the dashboard.
   - The top bullish stocks will be displayed in the StockList component.
   - Click on a stock to view its detailed analysis and technical chart.

2. Executing a Trade:
   - Browse through the TradeRecommendations component.
   - Click on a recommended trade to view more details.
   - Click the "Execute Trade" button to open a trade execution dialog.
   - Confirm the trade details and click "Submit" to execute the trade.

3. Monitoring Active Positions:
   - The PositionTracker component displays the user's active positions.
   - Real-time updates are received via WebSocket subscriptions.
   - Click on a position to view more details and access position management options.

## Dependencies

The frontend application relies on the following key dependencies:

- React: JavaScript library for building user interfaces.
- axios: Promise-based HTTP client for making API requests.
- recharts: Library for creating interactive charts and data visualizations.
- lucide-react: Icon library for React.
- tailwindcss: Utility-first CSS framework for rapid UI development.
- react-notifications-component: Library for displaying notifications.
- websocket: Library for establishing WebSocket connections.

For a complete list of dependencies, please refer to the `package.json` file.

## Integration Guide

To integrate the frontend application with your backend system, follow these steps:

1. Set up the backend API endpoints according to the provided API documentation.
2. Configure the WebSocket server to handle real-time data updates.
3. Update the `stockApi` service in the frontend codebase to point to your backend API endpoints.
4. Modify the `WebSocketService` to establish a connection with your WebSocket server.
5. Ensure that the data formats and interfaces in the frontend match those provided by the backend.
6. Build and deploy the frontend application to a web server or hosting platform.
7. Test the integration by running the application and verifying that data is being fetched and updated correctly.

For detailed instructions on building and deploying the frontend application, please refer to the development documentation.