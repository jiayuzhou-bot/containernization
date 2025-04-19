# DS5105 Exercise 2 – Causal Inference API

This project implements a **causal inference regression model** using the Rubin Causal Model and exposes it as a **REST API** with Flask. The application is fully **containerized with Docker** and designed to run seamlessly in **GitHub Codespaces** or any other Docker-compatible environment.

---

## 📌 Question 1 — Estimate

This part of the API fits the following **linear regression model**:
Y = α + τ·W + β·X + ε

- `W`: Binary treatment indicator (1 = participated in the carbon offset program, 0 = did not participate)  
- `X`: Annual sustainability spending (in $1,000s)  
- `Y`: Observed stakeholder engagement score  

### ✅ Returns

A JSON object with the estimated regression parameters:

```json
{
  "ATE_tau": -9.11,
  "beta_for_X": 1.51,
  "intercept_alpha": 95.97,
  "p_value_tau": 0.0004,
  "significance_1_percent": "✅ Statistically significant at 1% level"
}
```

#### ⚙️ How to Run
1. Build and Run the Docker Container
```
docker build -t my-api .
docker run -p 5000:5000 my-api
```
2. Access the /estimate Endpoint
You have two options to call the API:

    In your browser, open the following URL:
```
https://special-journey-pjg4q4rv6vpqh7gq7-5000.app.github.dev/estimate?W=1&X=20
```
    
Or, in a new terminal, enter the following command:

```
curl "http://localhost:5000/estimate?W=1&X=20"
```
3. View returned output (JSON)

## Question 2 – Predict

This endpoint uses the trained linear regression model to predict stakeholder engagement based on:

W: whether the company participates in the carbon offset program (1 = yes, 0 = no)

X: the amount of sustainability spending

#### 🛠 How to Run
1: Build and Run the Container
```
docker build -t my-api .
docker run -p 5000:5000 my-api
```
2. Access the /estimate Endpoint
You have two options to call the API:

    In your browser, open the following URL:
```
https://special-journey-pjg4q4rv6vpqh7gq7-5000.app.github.dev/predict?W=1&X=20
```
Or, in a new terminal, enter the following command:

```
curl "http://localhost:5000/predict?W=1&X=20"
```

3. View returned output (JSON)
```
{
  "W": 1.0,
  "X": 20.0,
  "predicted_engagement": 117.16
}
```