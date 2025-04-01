// frontend/src/components/AIAssistant.jsx
import { useEffect, useState } from 'react';
import { useUser } from '../context/UserContext';
import RecommendationEngine from '../lib/recommendation';

export default function AIAssistant() {
  const { user } = useUser();
  const [recommendations, setRecommendations] = useState([]);
  const [learningTip, setLearningTip] = useState('');

  useEffect(() => {
    const loadRecommendations = async () => {
      const recEngine = new RecommendationEngine(user.id);
      const recs = await recEngine.getHybridRecommendations();
      setRecommendations(recs);
      
      // تحليل أنماط التعلم لتقديم نصائح مخصصة
      const tip = await recEngine.getLearningTip();
      setLearningTip(tip);
    };
    
    loadRecommendations();
  }, [user]);

  const handleInteraction = async (interactionData) => {
    // تسجيل التفاعل وتحليل المشاعر
    await trackInteraction('ai_interaction', {
      ...interactionData,
      sentiment: analyzeSentiment(interactionData.userInput)
    });
    
    // تحديث التوصيات فوراً
    loadRecommendations();
  };

  return (
    <div className="ai-assistant-container">
      <div className="recommendation-sidebar">
        <h3>التوصيات المخصصة</h3>
        <ul>
          {recommendations.map((rec, index) => (
            <li key={index}>
              <button onClick={() => applyRecommendation(rec)}>
                {rec}
              </button>
            </li>
          ))}
        </ul>
        
        {learningTip && (
          <div className="learning-tip">
            <h4>نصيحة تعليمية</h4>
            <p>{learningTip}</p>
          </div>
        )}
      </div>
      
      <div className="main-content">
        {/* واجهة المحادثة الرئيسية */}
      </div>
    </div>
  );
}