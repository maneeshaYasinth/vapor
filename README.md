# ⚡ vapor

> AWS cost visibility in your terminal — no console, no browser, just vapor.

```
⚡ vapor — AWS cost visibility in your terminal

┌─────────────────────────────────────────┐
│     AWS Cost Summary — March 2026       │
├──────────────────────────┬──────────────┤
│ Service                  │ Cost (USD)   │
├──────────────────────────┼──────────────┤
│ EC2                      │ $12.40       │
│ ECS Fargate              │  $8.20       │
│ S3                       │  $0.84       │
│ DynamoDB                 │  $1.10       │
├──────────────────────────┼──────────────┤
│ Total MTD                │ $22.54       │
│ Forecasted               │ $31.00       │
└──────────────────────────┴──────────────┘
```

---

## what is this

`vapor` is a lightweight CLI tool that pulls your AWS costs directly from the Cost Explorer API and renders them in your terminal. no browser, no AWS console login, no dashboards — just run `vapor` and see where your money is going.

---

## stack

- [`boto3`](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) — AWS SDK for Python
- [`rich`](https://github.com/Textualize/rich) — terminal UI rendering
- [`click`](https://click.palletsprojects.com/) — CLI framework

---

## installation

```bash
git clone https://github.com/yourusername/vapor.git
cd vapor
pip install -e .
```

---

## prerequisites

AWS credentials configured on your machine:

```bash
aws configure
```

or via environment variables:

```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
```

> **note:** Cost Explorer API charges $0.01 per request. negligible for personal use.

---

## usage

```bash
# current month costs by service
vapor

# use a specific AWS profile
vapor --profile prod

# show last N days breakdown
vapor --days 7

# include month-end forecast
vapor --forecast
```

---

## roadmap

- [x] project scaffold & CLI entry point
- [ ] MTD cost by service
- [ ] month-end forecast
- [ ] `--profile` multi-account support
- [ ] `--days N` daily breakdown
- [ ] color coding by spend level
- [ ] loading spinner
- [ ] publish to PyPI

---

## permissions required

your IAM user/role needs the following policy:

```json
{
  "Effect": "Allow",
  "Action": [
    "ce:GetCostAndUsage",
    "ce:GetCostForecast"
  ],
  "Resource": "*"
}
```

---

## license

MIT