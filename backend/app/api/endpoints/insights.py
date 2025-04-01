# backend/app/api/endpoints/insights.py
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.db import get_analytics_collection
import plotly.express as px
import pandas as pd

router = APIRouter()

@router.get("/dashboard", response_class=HTMLResponse)
async def ml_dashboard():
    """لوحة تحكم لمراقبة أداء النماذج"""
    analytics = get_analytics_collection()
    data = list(analytics.find({}, {"_id": 0}))
    df = pd.DataFrame(data)
    
    # إنشاء رسوم بيانية
    fig1 = px.line(df, x="timestamp", y="accuracy", title="دقة النموذج بمرور الوقت")
    fig2 = px.pie(df, names="model_usage", title="توزيع استخدام النماذج")
    
    return f"""
    <html>
        <head>
            <title>لوحة تحكم التعلم الآلي</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        </head>
        <body>
            <h1>تحليلات التعلم الآلي</h1>
            <div id="chart1">{fig1.to_html(full_html=False)}</div>
            <div id="chart2">{fig2.to_html(full_html=False)}</div>
            
            <h2>أحدث التفاعلات</h2>
            <table border="1">
                <tr>
                    <th>المستخدم</th>
                    <th>النموذج</th>
                    <th>التقييم</th>
                </tr>
                {"".join(
                    f"<tr><td>{row['user_id']}</td><td>{row['model']}</td><td>{row['rating']}</td></tr>"
                    for row in data[-10:]
                )}
            </table>
        </body>
    </html>
    """