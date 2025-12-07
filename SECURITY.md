# Security Policy

## Scope
This project is synthetic and educational. No real-world political or personal data should be ingested. All analyses are fictional simulations.

## Reporting
Report security concerns or misuse by opening a confidential issue or contacting the maintainers. Please include reproduction steps and potential impact within the synthetic context.

## Responsible Use
- Do not deploy this project for real-world surveillance or persuasion.
- Ensure deployments are isolated and use sample or synthetic data only.
- Keep dependencies updated via `pip install -r requirements.txt --upgrade`.

## Hardening Tips
- Run behind TLS termination when exposed.
- Enable authentication/authorization in FastAPI if multi-user scenarios are added.
- Restrict file system permissions for `logs/` and `reports/`.
