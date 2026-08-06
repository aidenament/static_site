# Goodreads for Friends

[< Back to Projects](/projects)

## A Website to Host Book and Game Reviews in FastAPI and React

[shutthehellupdaryan.com](https://shutthehellupdaryan.com/) is a media tracker for logging books and games, rating them in half stars, and reviewing them. Accounts are invite only: there is no signup route, and they are created through an admin endpoint or a command line script. The reviews themselves are publicly readable.

The backend is FastAPI over PostgreSQL with an optional Redis cache. The frontend is a React single page application. It is deployed on Railway.

### Architecture

FastAPI owns authentication, data access, the external API integrations, and asset serving. It renders exactly one Jinja template: a nineteen line shell that embeds a JSON bootstrap payload and the Vite manifest tags. React takes over from there, with all ten page components lazily loaded behind Suspense.

The shell ships each page's data inline rather than leaving the client to fetch it after mount. The homepage HTML already contains the user cards, item cards, featured review, and CSRF token, and the client seeds that payload straight into its cache, so the first React render is a cache hit instead of a round trip. The same payload shape is served from an API endpoint for the Vite dev server, where no server rendered script tag exists.

Behind the routers are fourteen service modules and ten SQLAlchemy models. Routers are split by concern rather than by resource: the books router is a ten line aggregator over separate page, API, and mutation modules, which separates read handling from writes without changing any route paths.

### Query Design

The homepage and profile feeds need aggregates per user and per item: review counts, average ratings, items added, and the date of the most recent review. Each aggregate is computed by its own grouped subquery and joined onto the base table in a single pass, rather than being counted per row, so the feed does not turn into an N+1 as the number of users grows.

The startup script runs `alembic upgrade head` on every boot. The performance migrations inspect the live schema and skip any index that is already present, which keeps them from failing against a database where an index was created outside the migration chain or by a partially applied revision.

### Caching

The cache exposes one interface with two implementations, Redis in production and a process local dictionary with matching semantics as a fallback, selected once at first use after a ping.

Invalidation is by tag rather than by key pattern. Writing a cached value also records its key in a set, so invalidating a topic reads that set and deletes its members instead of scanning the keyspace. Tag sets carry an extra hour of expiry so orphaned entries clean themselves up.

Cached payloads are deliberately user agnostic. The item blob and its paginated review list are cached once and shared by every reader; the fields that vary per viewer, their vote and their permissions on the item, are attached afterward with small queries. One cache entry then serves anonymous and signed in traffic alike.

Invalidating the homepage, a profile, or the slander wall also schedules an immediate re-warm of that same view on a background thread, so the next reader does not pay for the miss. A periodic loop started from the application lifespan refreshes the homepage and a sample of recently touched profiles, pushing the blocking database work through a thread pool so the event loop stays free.

### Correctness Details

Several paths required explicit handling.

**Unique constraints are enforced under races.** Two users claiming the same sticky note slot, and a double submitted vote, both raise integrity errors. Each is caught, rolled back, and returned as a meaningful status rather than a 500.

**A circular foreign key is unwound by hand.** Users point at their favorite, least favorite, and current book, and those columns carry no cascade behavior, so deleting a book first finds every user pinning it, clears those columns, flushes to force the ordering, and only then deletes.

**Long passwords are pre-hashed.** bcrypt truncates silently at 72 bytes, so passwords are run through SHA-256 and base64 first, following the recommendation from the bcrypt maintainers.

**Review markdown is rendered through an allowlist.** Bodies are rendered, sanitized against an explicit tag and protocol allowlist, then passed through a filter that replaces any image source not served by the CDN. The rendered HTML is cached keyed on the review's update timestamp, so editing a review invalidates it without an explicit bust.

### The Client Data Layer

The frontend uses no data fetching library. It has a small TTL cache, a hook that reads from it, and Zod schemas that validate the main payloads at the boundary, dispatched by URL pattern as responses come back.

Two details matter for correctness. The bootstrap payload is seeded during render behind a guard, because re-seeding on later renders would reset each entry's stored timestamp, freezing its TTL and overwriting freshly fetched data with the initial snapshot. And every request threads an abort signal that fires on key change or unmount, with the error and loading transitions suppressed once aborted, which is the usual source of state updates on unmounted components in a hand rolled layer.

A suite of backend tests encodes the payload shapes the TypeScript validators expect, written as Python assertions mirroring them rather than by importing them. A response that drifts from that mirror fails in the backend suite instead of surfacing as a validation error in the browser.

### Instrumentation

A small timing context manager wraps named database operations and logs their duration as labelled key and value pairs, and a middleware records request duration, cache backend, and a correlation ID for the handful of hot path prefixes. Logs are JSON in production and human readable in development, with the request ID echoed back as a response header.

### Scale and Testing

Sixty-one HTTP endpoints, twenty-eight of which change state, and every one of those twenty-eight validates a CSRF token. Ten models, forty-one Pydantic schemas, and eighteen migrations in a single linear chain.

The backend suite is 222 tests at 78% line coverage, and the frontend adds fourteen, of which eight render components and the rest cover the validators and bootstrap parsing. Both run as Railway build phases and gate the deploy. The application is roughly 8,600 lines of Python and 11,000 lines of TypeScript and CSS, with a further 5,200 lines of Python tests, across 232 commits.

### Technologies Used

- **Backend**: FastAPI, SQLAlchemy 2.0, Alembic, Pydantic, PostgreSQL, Redis, JWT in httpOnly cookies, bcrypt, bleach and markdown2, tenacity
- **Frontend**: React 19, React Router 7, TypeScript, Vite, Zod, Vitest
- **Integrations**: Hardcover GraphQL API for books, IGDB for games, Cloudinary for image hosting
- **Deployment**: Railway with Nixpacks
