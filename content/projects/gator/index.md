# Gator - RSS Feed Aggregator

[< Back to Projects](/projects)

## Command-Line RSS Feed Aggregator Written in Go

Gator is a powerful command-line RSS feed aggregator that allows users to manage and browse RSS feeds from the terminal. Built with Go and PostgreSQL, it supports multiple users, feed following, and automatic content aggregation.

### GitHub Repository

View the source code and contribute: [github.com/aidenament/Gator](https://github.com/aidenament/Gator)

### Overview

Gator brings RSS feed management to the command line with a focus on simplicity and efficiency. It provides a complete ecosystem for discovering, following, and reading RSS content without leaving your terminal. The application leverages Go's concurrency features for efficient feed fetching and PostgreSQL for reliable data persistence.

### Key Features

- **User Management**: Register and login multiple users with isolated feed subscriptions
- **Feed Management**: Add, list, follow, and unfollow RSS feeds with simple commands
- **Content Aggregation**: Automatically fetch and store RSS feed content at specified intervals
- **Content Browsing**: View recent posts from your followed feeds in a clean format
- **HTML to Markdown**: Converts HTML content in RSS feeds to readable Markdown format
- **Database Persistence**: Uses PostgreSQL for storing users, feeds, and posts with proper relationships

### Technical Architecture

#### Database Schema

The application uses a well-structured relational database design:

- **users**: Stores user information (id, name, created_at, updated_at)
- **feeds**: Stores RSS feed information (id, name, url, user_id, created_at, updated_at, last_fetched_at)
- **feed_follows**: Many-to-many relationship between users and feeds
- **posts**: Stores individual RSS posts with deduplication support

#### Code Organization

```
gator/
├── main.go              # Main application logic
├── go.mod               # Go module definition
├── go.sum               # Go module checksums
├── sqlc.yaml            # sqlc configuration
├── internal/
│   ├── config.go        # Configuration management
│   └── database/        # Generated database code
├── sql/
│   ├── schema/          # Database migrations
│   └── queries/         # SQL queries for code generation
└── README.md           # Documentation
```

### Core Components

1. **Command System**: Each CLI command has a dedicated handler function with clear separation of concerns
2. **Middleware**: Authentication middleware ensures certain commands require login
3. **RSS Parser**: Fetches and parses RSS/XML feeds with robust HTTP client
4. **HTML Converter**: Converts HTML content to Markdown for better terminal display
5. **Database Layer**: Uses sqlc for type-safe database operations

### Usage Examples

#### User Management
```bash
# Register a new user
gator register alice

# Login as existing user
gator login bob

# List all users
gator users
```

#### Feed Management
```bash
# Add a new RSS feed
gator addfeed "Tech News" https://example.com/rss

# Follow an existing feed
gator follow https://blog.example.com/feed

# List feeds you're following
gator following

# Unfollow a feed
gator unfollow https://example.com/rss
```

#### Content Aggregation
```bash
# Start aggregator with 1-minute interval
gator agg 1m

# Browse recent posts (default: 2 posts)
gator browse

# Browse more posts
gator browse 10
```

### Advanced Features

#### Authentication Flow

1. User runs `register` or `login` command
2. System validates user exists (login) or creates user (register)
3. Configuration file is updated with current user
4. Subsequent commands requiring authentication check current user from config

#### Feed Aggregation Flow

1. `agg` command starts ticker with specified duration
2. On each tick:
   - Query database for feed with oldest `last_fetched_at`
   - Fetch RSS content via HTTP
   - Parse XML and extract posts
   - Convert HTML content to Markdown
   - Store new posts (skip duplicates)
   - Update feed's `last_fetched_at` timestamp

### Development Highlights

- **Type Safety**: Uses sqlc to generate type-safe Go code from SQL queries
- **Error Handling**: Comprehensive error handling for network, database, and parsing issues
- **Concurrency**: Leverages Go's goroutines for efficient feed fetching
- **Configuration**: Simple JSON-based configuration stored in user's home directory
- **Extensibility**: Clean architecture allows easy addition of new features

### Technologies Used

- **Go 1.24.4+**: Modern Go for performance and simplicity
- **PostgreSQL**: Robust relational database for data persistence
- **sqlc**: Type-safe SQL code generation
- **Standard Library**: Minimal dependencies, leveraging Go's excellent standard library

### Installation

```bash
# Install directly using Go
go install github.com/aidenament/gator@latest

# Set up configuration
echo '{"db_url": "postgres://user:pass@localhost/gator?sslmode=disable"}' > ~/.gatorconfig.json
```

### Future Enhancements

- Web UI for browser-based access
- Feed categorization and tagging
- Full-text search across posts
- Export functionality (OPML, JSON)
- Feed health monitoring and statistics
- Mobile app companion

### Why Gator?

In an age of algorithmic feeds and social media, Gator brings back the simplicity and control of RSS. It's perfect for:
- Developers who live in the terminal
- Privacy-conscious users who want local feed storage
- Power users who need scriptable feed management
- Anyone looking to escape the noise of modern content platforms

### License

This project is provided as-is for educational purposes.