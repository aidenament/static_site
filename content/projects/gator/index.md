# Gator - RSS Feed Aggregator

[< Back to Projects](/projects)

## Command-Line RSS Feed Aggregator Written in Go

Gator is a powerful command-line RSS feed aggregator that allows users to manage and browse RSS feeds from the terminal. Built with Go and PostgreSQL, it supports multiple users, feed following, and automatic content aggregation.

### GitHub Repository

View the source code: [github.com/aidenament/Gator](https://github.com/aidenament/Gator)

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

- **users**: Stores user information (**id**, **name**, **created_at**, **updated_at**)
- **feeds**: Stores RSS feed information (**id**, **name**, **url**, **user_id**, **created_at**, **updated_at**, **last_fetched_at**)
- **feed_follows**: Many-to-many relationship between users and feeds
- **posts**: Stores individual RSS posts with deduplication support

### Core Components

- **Command System**: Each CLI command has a dedicated handler function with clear separation of concerns
- **Middleware**: Authentication middleware ensures certain commands require login
- **RSS Parser**: Fetches and parses RSS/XML feeds with robust HTTP client
- **HTML Converter**: Converts HTML content to Markdown for better terminal display
- **Database Layer**: Uses sqlc for type-safe database operations

### Usage Examples

#### User Management

> Register a new user <br>
> **gator register alice**

> Login as existing user <br>
> **gator login bob**

> List all users <br>
> **gator users**

#### Feed Management

> Add a new RSS feed <br>
>**gator addfeed "Tech News" https://example.com/rss**

> Follow an existing feed <br>
> **gator follow https://blog.example.com/feed**

> List feeds you're following <br>
> **gator following**

> Unfollow a feed <br>
> **gator unfollow https://example.com/rss**

#### Content Aggregation

> Start aggregator with 1-minute interval<br>
> **gator agg 1m**

> Browse recent posts (default: 2 posts) <br>
> **gator browse**

> Browse more posts <br>
> **gator browse 10**

### Advanced Features

#### Authentication Flow

1. User runs register or login command
2. System validates user exists (login) or creates user (register)
3. Configuration file is updated with current user
4. Subsequent commands requiring authentication check current user from config

#### Feed Aggregation Flow

1. agg command starts ticker with specified duration
2. On each tick:
   - Query database for feed with oldest last___fetched___at
   - Fetch RSS content via HTTP
   - Parse XML and extract posts
   - Convert HTML content to Markdown
   - Store new posts (skip duplicates)
   - Update feed's last___fetched___at timestamp

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
- **goose**: For database migrations

### Installation

> **Install directly using Go** <br>
> go install github.com/aidenament/gator@latest

> **Set up configuration** <br>
> echo **'{"db_url": "postgres://user:pass@localhost/gator?sslmode=disable"}' > ~/.gatorconfig.json**