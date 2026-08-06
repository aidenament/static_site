# Goodreads for Friends

[< Back to Projects](/projects)

## A Website to Host Book and Game Reviews in FastAPI and React

[shutthehellupdaryan.com](https://shutthehellupdaryan.com/) is where my friends and I log books and games, rate them in half stars, and argue about them.

The name is the point. It's Goodreads for a group of friends and nobody else, which is why there's no signup route and why one of the pages is a wall for slandering each other. Daryan is blocked from posting on it. The endpoint answers him with a 403 and "Nice try, Daryan." Everything below is what it took to make something that small feel fast.

The backend is FastAPI over PostgreSQL with an optional Redis cache, the frontend is React, and it runs on Railway.

### Architecture

FastAPI owns authentication, data access, the external API integrations, and asset serving. It renders exactly one Jinja template: a nineteen line shell holding a JSON bootstrap payload and the Vite manifest tags. React takes over from there, with all ten page components lazily loaded behind Suspense.

The shell ships each page's data inline. The homepage HTML already contains the user cards, item cards, featured review, and CSRF token, and the client seeds that payload straight into its cache. The first React render is a cache hit. The same payload shape comes from an API endpoint for the Vite dev server, where there's no server rendered script tag to read.

Behind the routers sit fourteen service modules and ten SQLAlchemy models. The routers are split by concern: the books router is a ten line aggregator over separate page, API and mutation modules, which keeps reads and writes apart without renaming a single route.

### Query Design

The homepage and profile feeds need aggregates per user and per item: review counts, average ratings, items added, the date of the most recent review. Each one gets its own grouped subquery, joined onto the base table in a single pass. Adding users adds rows to the result and nothing to the query count.

The startup script runs `alembic upgrade head` on every boot. The performance migrations inspect the live schema and skip any index that's already there, which keeps them from failing against a database where an index arrived outside the migration chain.

### Caching

One interface, two implementations: Redis in production, and a process local dictionary with matching semantics when there's no cache URL or the ping fails. The choice happens once, at first use.

Invalidation works by tag. Writing a cached value also records its key in a set. Invalidating a topic reads that set and deletes its members. No keyspace scanning. Tag sets carry an extra hour of expiry so orphans clean themselves up.

Cached payloads are user agnostic. The item blob and its paginated review list are cached once for everybody, and the parts that differ per viewer, their vote and their permissions, get attached afterward with small queries. One cache entry serves anonymous and signed in traffic alike.

Invalidating the homepage, a profile or the slander wall also fires a background re-warm of that same view, so the next reader doesn't eat the miss. A loop started from the application lifespan refreshes the homepage and a sample of recently touched profiles, pushing the blocking database work through a thread pool to keep the event loop free.

### The Parts That Needed Care

**Unique constraints hold under races.** Two people claiming the same sticky note slot, or a double submitted vote, both raise integrity errors. Each one is caught, rolled back, and turned into a status code that means something.

**A circular foreign key gets unwound by hand.** Users point at their favorite, least favorite and current book, and those columns carry no cascade behavior. Deleting a book finds every user pinning it, clears those columns, flushes to force the ordering, then deletes.

**Long passwords are pre-hashed.** bcrypt truncates silently at 72 bytes, so passwords go through SHA-256 and base64 first. The docstring cites the recommendation it came from.

**Review markdown goes through an allowlist.** Bodies are rendered, sanitized against an explicit tag and protocol allowlist, then filtered to replace any image source not served by the CDN. The rendered HTML is cached against the review's update timestamp, so editing a review invalidates it without an explicit bust.

### The Client Data Layer

There's no data fetching library. A small TTL cache, a hook that reads from it, and Zod schemas validating the main payloads as they come back.

Two details matter. The bootstrap payload is seeded during render behind a guard, because re-seeding on later renders would reset each entry's stored timestamp, freeze its TTL, and overwrite freshly fetched data with the initial snapshot. And every request threads an abort signal that fires on key change or unmount. Once aborted, the error and loading transitions are suppressed. That's where a hand rolled data layer usually starts setting state on components that no longer exist.

A suite of backend tests encodes the payload shapes the TypeScript validators expect, written as Python assertions mirroring them. A response that drifts from that mirror fails in the backend suite, not in somebody's browser.

### Instrumentation

A timing context manager wraps named database operations and logs their duration as labelled key and value pairs. A middleware records request duration, cache backend and a correlation ID, but only for the handful of hot path prefixes. Logs are JSON in production and readable in development, with the request ID echoed back as a response header.

### Scale and Testing

Sixty-one HTTP endpoints, twenty-eight of which change state, and every one of those twenty-eight validates a CSRF token. Ten models, forty-one Pydantic schemas, eighteen migrations in a single linear chain.

The backend suite is 222 tests at 78% line coverage. The frontend adds fourteen, of which eight render components and the rest cover the validators and bootstrap parsing. Both run as Railway build phases and gate the deploy. The application is roughly 8,600 lines of Python and 11,000 lines of TypeScript and CSS, with another 5,200 lines of Python tests, across 232 commits.

### Technologies Used

- **Backend**: FastAPI, SQLAlchemy 2.0, Alembic, Pydantic, PostgreSQL, Redis, JWT in httpOnly cookies, bcrypt, bleach and markdown2, tenacity
- **Frontend**: React 19, React Router 7, TypeScript, Vite, Zod, Vitest
- **Integrations**: Hardcover GraphQL API for books, IGDB for games, Cloudinary for image hosting
- **Deployment**: Railway with Nixpacks
