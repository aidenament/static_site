# Goodreads for Friends

[< Back to Projects](/projects)

## A Website to Host Book and Game Reviews in FastAPI and React

[shutthehellupdaryan.com](https://shutthehellupdaryan.com/) is a review site I built for my friends and me. It is a great place for us to write and share our reviews for books and games we have strong opinions on.

### Architecture

FastAPI handles authentication, database access, external services, and asset delivery. The React frontend contains ten lazily loaded pages.

The backend renders one 19-line Jinja template. It includes the Vite entry points and a JSON payload containing the data required for the current page. React reads that payload into its client-side cache, so the initial render does not need another request. During development, when the frontend runs on a separate Vite server, the same payload is available through an API endpoint.

Several pages display aggregates such as review counts, average ratings, items added, and the date of each user's latest review. Each aggregate is calculated in a grouped subquery and joined to the main query. The result is returned in one database statement, regardless of how many users are displayed.

### Caching

The cache has two implementations behind the same interface. Production uses Redis. Development falls back to an in-process dictionary when no Redis URL is configured or the connection check fails.

Entries are organized using tags. When a value is cached, its key is added to a Redis set for each relevant topic. Invalidating a topic means reading that set and deleting its members; it never requires scanning the keyspace.

The larger cached payloads are shared between users. An item and its reviews are cached once, while viewer-specific fields such as votes and permissions are fetched separately and attached afterward. The same cache entry can therefore serve both anonymous and signed-in requests.

Invalidating the homepage, a profile, or the slander wall also queues that view to be rebuilt in the background. The next visitor is less likely to encounter a cold cache.

### Data Integrity and Security

Database constraints handle races that request-level checks cannot prevent. If two users claim the same sticky-note position or submit the same vote simultaneously, the database raises an integrity error. The request rolls back and returns an appropriate status code.

Deleting a book requires explicit handling because users can reference books as their favorite, least favorite, or current read. Those references do not cascade. Before deletion, the application clears every affected user field, flushes the changes, and then removes the book.

Passwords are hashed with bcrypt, but bcrypt silently ignores input beyond 72 bytes. Passwords are therefore passed through SHA-256 and Base64 before bcrypt so long passwords are not truncated.

Reviews support Markdown. The rendered HTML is sanitized using explicit tag and protocol allowlists, and image sources are limited to the configured CDN. Rendered reviews are cached using their update timestamps, so an edit automatically produces a new cache key.

Database migrations are safe to run on every deployment. The startup command runs `alembic upgrade head`, and index migrations inspect the current schema before creating anything. A manually added index will not cause a later deployment to fail.

### Client Data

The frontend does not use a data-fetching library. It has a small TTL cache, a React hook for subscribing to entries, and Zod schemas for validating the main API responses.

The initial server payload is inserted into the cache only once. Re-inserting it on every render would refresh its timestamp indefinitely and could overwrite newer data with the original page snapshot.

Requests also receive an `AbortSignal`. Changing a cache key or unmounting the component cancels the request and suppresses any later loading or error update, preventing stale requests from updating components that no longer use their results.

The TypeScript response schemas are mirrored by assertions in the Python test suite. If the backend changes a payload that the frontend expects, the backend tests catch it before deployment.

### Project Size

The backend has 61 endpoints, including 28 that modify state. All 28 require a valid CSRF token. It also contains ten database models, 41 Pydantic schemas, and 18 migrations in one linear chain.

There are 222 backend tests with 78% line coverage and 14 frontend tests. Both suites run during the Railway build and must pass before deployment.

- **Backend**: FastAPI, SQLAlchemy 2.0, Alembic, Pydantic, PostgreSQL, Redis, JWT in HttpOnly cookies, bcrypt, Bleach, markdown2, Tenacity
- **Frontend**: React 19, React Router 7, TypeScript, Vite, Zod, Vitest
- **Integrations**: Hardcover, IGDB, Cloudinary
- **Deployment**: Railway with Nixpacks
