# ⚡ vapor

> AWS cost visibility in your terminal — no console, no browser, just vapor.

```
╭───────────────────────────────╮
│ ⚡ vapor  AWS cost visibility │
╰───────────────────────────────╯

              Cost Summary — March 2026
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Service                        ┃   Cost (USD) ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ Amazon EC2                     │      $12.40  │
│ AWS Fargate                    │       $8.20  │
│ Amazon S3                      │       $0.84  │
│ Amazon DynamoDB                │       $1.10  │
├────────────────────────────────┼──────────────┤
│ Total MTD                      │      $22.54  │
│ Forecasted (EOM)               │      $31.00  │
└────────────────────────────────┴──────────────┘
```

---

## what is this

`vapor` is a lightweight Python CLI tool that pulls your AWS costs directly from the Cost Explorer API and renders them in your terminal. no browser, no AWS console login, no dashboards — just run `vapor` and see where your money is going.

built for developers who live in the terminal and don't want to open a browser just to check their AWS bill.

---

## features

- 📊 month-to-date cost breakdown by service
- 📅 daily cost breakdown with `--days N`
- 🔮 month-end forecast with `--forecast`
- 🎨 color-coded spend levels (green → yellow → red)
- ⚡ animated loading spinner while fetching
- 🔑 multi-account support via `--profile`

---

## stack

| library | purpose |
|---|---|
| [`boto3`](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) | AWS SDK — talks to Cost Explorer API |
| [`rich`](https://github.com/Textualize/rich) | terminal UI — tables, colors, spinner |
| [`click`](https://click.palletsprojects.com/) | CLI framework — flags and commands |

---

## installation

```bash
git clone https://github.com/maneeshaYasinth/vapor.git
cd vapor
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

## prerequisites

### 1. AWS credentials

configure your AWS credentials on your machine:

```bash
aws configure
```

or via environment variables:

```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
```

### 2. enable Cost Explorer

on first use, Cost Explorer must be enabled in your AWS account:

1. log in as your **root account**
2. go to **Billing and Cost Management → Cost Explorer**
3. visit the page — it auto-enables on first visit
4. wait up to 24 hours for data to populate

> **note:** Cost Explorer API charges **$0.01 per request**. negligible for personal use.

### 3. IAM permissions

your IAM user/role needs the following policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ce:GetCostAndUsage",
        "ce:GetCostForecast"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## usage

```bash
# current month costs by service
vapor

# include month-end forecast
vapor --forecast

# show daily breakdown for last N days
vapor --days 7

# use a specific AWS profile (multi-account)
vapor --profile prod

# combine flags
vapor --forecast --days 14 --profile staging
```

---

## roadmap

- [x] project scaffold & CLI entry point
- [x] MTD cost breakdown by service
- [x] color coding by spend level
- [x] loading spinner
- [x] month-end forecast (`--forecast`)
- [x] daily breakdown (`--days N`)
- [x] multi-account support (`--profile`)
- [ ] publish to PyPI (`pip install vapor-cli`)
- [ ] interactive TUI mode
- [ ] budget vs actual comparison
- [ ] `--json` output for piping

---

## project structure

```
vapor/
├── vapor/
│   ├── __init__.py
│   ├── cli.py          # entry point & display logic
│   └── costs.py        # boto3 API calls
├── setup.py
├── requirements.txt
└── README.md
```

---

## license

MIT