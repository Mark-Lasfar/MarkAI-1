// frontend/components/RecommendationBar.jsx
import useSWR from 'swr';

export default function RecommendationBar({ userId }) {
  const { data: recs, error } = useSWR(`/api/get_recommendations?userId=${userId}`);

  if (!recs) return <div>Loading recommendations...</div>;
  if (error) return <div>Error loading recommendations: {error.message}</div>;

  return (
    <div className="recommendation-bar">
      <h3>مقترحات لك</h3>
      <div className="recommendation-list">
        {recs.recommendations.map((rec, idx) => (
          <button 
            key={idx} 
            className="recommendation-item"
            onClick={() => handleApplyRecommendation(rec)}
          >
            {rec}
          </button>
        ))}
      </div>
    </div>
  );
}