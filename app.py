
#####################################################################
#### app.py ####

from flask import Flask, request, jsonify
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import statsmodels.api as sm

app = Flask(__name__)

# 原始数据
data = {
    "Engagement_Score": [137, 118, 124, 124, 120, 129, 122, 142, 128, 114,
                         132, 130, 130, 112, 132, 117, 134, 132, 121, 128],
    "Treatment":         [0,   1,   1,   1,   0,   1,   1,   0,   0,   1,
                          1,   0,   0,   1,   0,   1,   0,   0,   1,   1],
    "Sustainability_Spending": [19.8, 23.4, 27.7, 24.6, 21.5, 25.1, 22.4, 29.3, 20.8, 20.2,
                                27.3, 24.5, 22.9, 18.4, 24.2, 21.0, 25.9, 23.2, 21.6, 22.8]
}
df = pd.DataFrame(data)

# 拟合模型
X = df[["Treatment", "Sustainability_Spending"]]
X = sm.add_constant(X)
y = df["Engagement_Score"]
model = sm.OLS(y, X).fit()

@app.route("/estimate")
def estimate():
    try:
        # 获取回归参数
        alpha = round(model.params["const"], 2)
        tau = round(model.params["Treatment"], 2)
        beta = round(model.params["Sustainability_Spending"], 2)
        p_value_tau = round(model.pvalues["Treatment"], 4)
        significance = "✅ Statistically significant at 1% level" if p_value_tau < 0.01 else "❌ Not significant at 1% level"

        return jsonify({
            "intercept_alpha": alpha,
            "ATE_tau": tau,
            "beta_for_X": beta,
            "p_value_tau": p_value_tau,
            "significance_1_percent": significance
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/predict")
def predict():
    try:
        W = float(request.args.get("W", 0))
        X_val = float(request.args.get("X", 0))
        input_df = pd.DataFrame({"const": [1], "Treatment": [W], "Sustainability_Spending": [X_val]})
        y_pred = model.predict(input_df)[0]
        return jsonify({
            "W": W,
            "X": X_val,
            "predicted_engagement_score": round(y_pred, 2)  # 保留两位小数
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    print("✅ Flask app is starting...")
    print(app.url_map)
    app.run(host="0.0.0.0", port=5000)


