## Twitter Test

### Overview
Testing programmatic tweets via oauth2 + pkce. Created native app from the twitter developer portal. Using fastapi and authlib
to create endpoints and handle login.

### Twitter App Config
- type: native (public)
- app permissions: read (minimal since it only applies to oauth1)
- website url: `http://twitter-test-local.{domain}:8000`
- allowed callbacks or redirects:
  - `http://twitter-test-local.{domain}:8000/auth/twitter`
  - `http://twitter-test-local.{domain}:8000/docs/oauth2-redirect`

#### Keys and Tokens
- api key and secret: generated; not used
- bearer token: not generated; not used (for app access only)
- oauth2 client id: generated; used
- oauth2 client secret: generated; not used (since app type is native)

### Need for Authlib
The builtin fastapi security flow for `OAuth2AuthorizationCodeBearer` almost worked. It's able to initiate the login from
the openapi docs and land the user on the twitter consent screen. But after redirecting back to openapi docs, the page would
be blank. The client side console logs showed an issue with `window.opener` being `null`.

So my workaround is to use authlib which happens to integrate well with fastapi:
- https://docs.authlib.org/en/latest/client/fastapi.html

#### Caveat
The openapi docs don't show any authorize button or lock symbols next to the endpoints. As a workaround I customized the
description to include the login link to initiate the auth flow. And I'm storing the token data via `SessionMiddleware`.

### Twitter Free Tier
Unfortunately the free tier for Twitter app development has serious limitations. It seems that only reading the current
user's data and tweeting are supported. Reading users via username and direct messages are not offered in free tier. And
reading the user's profile is rate limited at 25 requests per 24 hours per user.

#### Tier Comparison
- https://developer.twitter.com/en/portal/products

### Potential Future Plans

#### Identity Provider
The goal would be to integrate with services like okta, auth0, or cognito to support login via Twitter. It may be possible
with a custom auth server. It would issue JWT tokens and support OIDC.

#### Backend Token Storage
Storing the access and refresh tokens in the session is useful for webapp testing. But not so much for automated systems.
For example if you want to have the app automatically post a tweet on your behalf, then the token data probably needs to
persisted to a datastore like MongoDB Atlas or Redis. There would need to be another process to refresh the tokens, and
prompt users to reauthenticate if the refresh fails.
