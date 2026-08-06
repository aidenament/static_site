# Goodreads for Friends

[< Back to Projects](/projects)

## A Books and Games Tracking App, Built for a Small Group of Friends

[shutthehellupdaryan.com](https://shutthehellupdaryan.com/) is a media tracker my friends and I use to log books and games, rate them in half stars, and argue about them in the reviews. It is deliberately invite only. There is no signup route anywhere in the application; accounts are created by an admin endpoint or a command line script.

The name comes from the Wall of Slander, a sticky note board where anyone can pin a note. One specific user is blocked from posting by a flag on his account, and the endpoint answers him with a 403 and the message "Nice try, Daryan."

### What It Does

- Tracks books and games behind one mode toggle that swaps the homepage, profile, and detail surfaces
- Searches books through Hardcover's GraphQL API and games through IGDB, marking results already on your shelf
- One review per user per item, enforced by a database constraint, rated in half stars with an optional markdown body
- Autosaves review drafts to local storage per form, so a half written review survives a refresh
- Uploads images into reviews through Cloudinary, and deletes them from Cloudinary when the review is deleted
- Lets users upvote and downvote each other's reviews, but never their own
- Highlights favorites, least favorites, and whatever you are currently reading or playing, chosen from server generated candidate lists

### Architecture

FastAPI serves the API, owns authentication, and renders exactly one Jinja template: a nineteen line shell that embeds a JSON bootstrap payload and the Vite asset tags. A React 19 single page app takes over from there, with all ten page components lazily loaded.

The interesting part is that the shell ships the page's data inline. The homepage HTML already contains the users, items, featured review, and CSRF token, and the client seeds that payload directly into its cache, so the first React render is a cache hit rather than a fetch. The same payload shape is served from an API route for the Vite dev server, where no server rendered script tag exists.

Behind the routers sit fourteen service modules and ten SQLAlchemy models. The homepage and profile feeds are assembled from grouped aggregate subqueries joined in a single pass, rather than counting reviews per row, so the feed does not degrade into an N+1.

### Decisions Worth Explaining

**Cache invalidation by tag, not by key pattern.** Writing a cached value also records its key in a Redis set, so invalidating a topic is one pipelined read and delete instead of a scan. Tag sets carry an extra hour of grace so orphans expire on their own. The process local fallback implements the same semantics with a dictionary of sets.

**Cached payloads are user agnostic.** The item blob and its paginated review list are cached once for everyone, and per user fields like your vote and your permissions are layered on afterward with small queries. One cache entry serves anonymous and signed in traffic alike.

**Passwords are hashed before they are hashed.** bcrypt silently truncates at 72 bytes, so passwords are run through SHA-256 and base64 first. The docstring cites the pyca/bcrypt recommendation that suggests it.

**A circular foreign key is defused by hand.** Users point at their favorite, least favorite, and currently reading book with no cascade behavior, so deleting a book first finds every user pinning it, nulls those columns, flushes to force the ordering, and only then deletes.

**Migrations are safe to re-run.** The startup script runs `alembic upgrade head` on every boot, so the index migrations inspect the live schema and skip indexes that already exist rather than failing against a database that has them.

**Races are handled, not just declared.** Two sticky notes claiming the same slot and a double submitted vote both raise integrity errors, and both are caught, rolled back, and turned into a sensible response instead of a 500.

**Contract tests across the language boundary.** A suite of Python tests encodes the payload shapes the TypeScript validators expect, so a drift between the FastAPI response and the Zod schema fails immediately rather than at runtime in a browser.

### Honest Notes

Worth stating plainly, because a reader looking at the live site will notice:

- **It is not a private app.** The homepage, profiles, and item details are all readable without signing in. Search, the slander wall, and every mutation require a session, but the reviews themselves are public.
- **It runs at friend group scale.** Two users and a couple dozen items. The caching and index work are real, but nothing here has been demonstrated under load.
- **Rate limits are per process and in memory.** Each router builds its own limiter, there is no shared store, and the deployment trusts forwarded client headers, so the limits deter accidents rather than a determined attacker.
- **Caching falls back silently.** Without a cache URL, or if the ping fails, it drops to a per process dictionary and logs a warning.
- **There is no CI.** The test suites run as build phases on Railway, which gates deploys, but nothing runs them on push.
- **Tailwind is installed but effectively unused.** The UI is hand written CSS: a base stylesheet of custom properties plus per component style blocks.

### Scale and Testing

Sixty-one HTTP endpoints, of which twenty-eight change state, and all twenty-eight validate a CSRF token. Ten models, forty-three Pydantic schemas, eighteen migrations in a single linear chain, and twelve rate limited endpoints.

The backend has 222 tests passing at 78% line coverage. The frontend has considerably less: fourteen tests over roughly eleven thousand lines of TypeScript, with the two largest components untested and no end-to-end tests at all.

Roughly 8,500 lines of Python and 11,000 lines of TypeScript and CSS, across 232 commits.

### Stack

**Backend:** FastAPI, SQLAlchemy 2.0, Alembic, Pydantic, PostgreSQL in production and SQLite locally, optional Redis, JWT in httpOnly cookies, bcrypt, bleach and markdown2 for review rendering, tenacity for outbound retries.

**Frontend:** React 19, React Router 7, TypeScript, Vite, Zod for response validation, Vitest.

**Deployment:** Railway with Nixpacks, which installs, runs both test suites, builds the frontend, applies migrations, and then starts uvicorn.
