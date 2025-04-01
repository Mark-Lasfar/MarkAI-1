// frontend/src/components/GenerationPanel.jsx
import { useGeneration } from '../hooks/useGeneration'

export default function GenerationPanel() {
  const {
    generateContent,
    generatedOutput,
    isLoading,
    error
  } = useGeneration()

  const handleGenerate = async (type, prompt) => {
    try {
      await generateContent(type, prompt)
    } catch (err) {
      console.error('Generation failed:', err)
    }
  }

  return (
    <div className="generation-panel">
      <GenerationTypeSelector onSelect={handleGenerate} />
      <GenerationOutput output={generatedOutput} />
      {isLoading && <LoadingIndicator />}
      {error && <ErrorMessage message={error} />}
    </div>
  )
}