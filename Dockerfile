FROM python:3.10.9-slim

WORKDIR /portfolio_optimization

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY portfolio_optimization/ portfolio_optimization/

COPY ./data/gold/portfolio-optimization/portfolio_optimization.csv /portfolio_optimization/data/gold/portfolio-optimization/portfolio_optimization.csv

CMD [ "python", "-m", "portfolio_optimization.main" ]