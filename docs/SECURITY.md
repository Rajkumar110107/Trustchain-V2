# 🔒 TrustChain Security Guidelines

## Security Controls Implemented

1. **Environment Separation**: All secrets, RPC credentials, and contract addresses are loaded dynamically from `.env` via `backend/config.py`.
2. **Input Validation**: `/analyze` endpoint restricts file extensions to `.jpg`, `.jpeg`, `.png`, `.webp` and enforces a maximum file upload size limit (default 10MB).
3. **CORS Control**: Middleware restricts requests to authorized origin domains.
4. **Temporary File Background Cleanup**: Background tasks automatically purge temporary uploaded files from disk after processing.
5. **No Private Key Exposure**: Private keys are strictly contained in local `.env` files and never rendered or sent to the React frontend.
