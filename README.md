# Event Analytics API

A lightweight event tracking and analytics backend built with FastAPI and SQLAlchemy, inspired by PostHog and Mixpanel. Tracks user events with idempotency guarantees and provides analytics endpoints for daily active users (DAU) and other metrics.

## 🚀 Features

- **Event Ingestion** - REST API endpoint for tracking user events with flexible JSON properties
- **Idempotency** - Prevents duplicate events using unique `insert_id` with database constraints
- **Analytics Queries** - Database-optimized aggregations for DAU and other metrics
- **Multi-tenancy** - Support for multiple projects via `project_id`
- **CORS Enabled** - Browser-based tracking with demo website included
- **Session Management** - Proper database session handling with automatic cleanup

## 🛠 Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM for database operations
- **SQLite** - Lightweight database (easily swappable for PostgreSQL)
- **Pydantic** - Data validation using Python type annotations

## 📋 Prerequisites

- Python 3.8+
- pip

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd event_analytics
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the server
```bash
uvicorn app.main:app --reload --port 8001
```

Server will start at `http://localhost:8001`

## 📚 API Documentation

### POST /track

Track an event from your application.

**Request:**
```bash
curl -X POST http://localhost:8001/track \
  -H "Content-Type: application/json" \
  -d '{
    "event_name": "page_view",
    "user_id": "user_123",
    "project_id": "my_website",
    "properties": {
      "page": "/home",
      "browser": "chrome"
    },
    "insert_id": "optional-unique-id"
  }'
```

**Response:**
```json
{
  "message": "Event tracked successfully",
  "event_id": 1
}
```

**Fields:**
- `event_name` (required) - Name of the event (e.g., "button_click", "page_view")
- `project_id` (required) - Identifier for your project/application
- `user_id` (optional) - Unique identifier for the user
- `properties` (optional) - Flexible JSON object with event metadata
- `insert_id` (optional) - Unique ID for idempotency (auto-generated if not provided)

### GET /metrics/dau

Get Daily Active Users for a date range.

**Request:**
```bash
curl "http://localhost:8001/metrics/dau?start_date=2026-03-09T00:00:00&end_date=2026-03-10T00:00:00"
```

**Response:**
```json
{
  "2026-03-09": 42,
  "2026-03-10": 38
}
```

**Query Parameters:**
- `start_date` (required) - ISO format: `YYYY-MM-DDTHH:MM:SS`
- `end_date` (required) - ISO format: `YYYY-MM-DDTHH:MM:SS`

## 🎯 Demo Website

A browser-based demo is included to test event tracking in action.

### Run the demo:
1. Start the API server (see setup above)
2. Open `demo/index.html` in your browser
3. Click buttons to track events
4. Watch events appear in real-time
5. Query metrics to see your activity

The demo shows how to integrate event tracking into a website, similar to how you'd use PostHog or Mixpanel.

## 🏗 Architecture

### Database Schema

**Events Table:**
- `id` - Auto-increment primary key
- `insert_id` - Unique identifier for idempotency (indexed, unique constraint)
- `event_name` - Name of the event (indexed for fast filtering)
- `timestamp` - When the event occurred (indexed for date range queries)
- `user_id` - User identifier (nullable)
- `properties` - JSON field for flexible event data
- `project_id` - Project identifier for multi-tenancy

### Key Design Decisions

**Database Aggregation** - DAU queries use `COUNT(DISTINCT user_id) GROUP BY DATE(timestamp)` to aggregate in the database rather than loading all events into memory. This ensures performance scales with data volume.

**Idempotency** - Network failures can cause duplicate requests. The `insert_id` field with a UNIQUE constraint prevents the same event from being counted twice, ensuring data accuracy.

**Session Management** - FastAPI's dependency injection with `yield` ensures database sessions are created per request and properly closed even if errors occur.

**Flexible Properties** - JSON column allows arbitrary event metadata without schema changes, enabling different event types to coexist in one table.

## 🔍 Example Use Cases

**Product Analytics:**
- Track button clicks, page views, feature usage
- Measure DAU/MAU for growth metrics
- Analyze user behavior patterns

**E-commerce:**
- Track product views, add-to-cart, purchases
- Calculate conversion funnels
- Monitor checkout abandonment

**SaaS Applications:**
- Track feature adoption
- Monitor user engagement
- Identify power users

## 📊 Performance Considerations

- **Indexes** - Created on `timestamp`, `event_name`, `insert_id`, and `user_id` for fast queries
- **Database Aggregation** - Metrics calculated in database, not application memory
- **Connection Pooling** - SQLAlchemy manages connection pool for concurrent requests
- **Scalability** - SQLite works for prototyping; migrate to PostgreSQL for production

## 🚧 Future Enhancements

- [ ] API key authentication for project isolation
- [ ] Additional analytics endpoints (MAU, event counts, funnels)
- [ ] Sessionization (group events into user sessions)
- [ ] Data retention policies
- [ ] Batch event ingestion
- [ ] PostgreSQL deployment
- [ ] Real-time dashboards

## 📝 License

MIT

## 🤝 Contributing

This is a learning project built to understand event analytics architecture. Feedback and suggestions welcome!

---

Built to understand how product analytics platforms like PostHog and Mixpanel work under the hood.
