// frontend/src/pages/api/generate.js
import { GenerationService } from '@/lib/services/generation';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    try {
      const { type, prompt } = req.body;
      const result = await GenerationService.generate(type, prompt);
      res.status(200).json(result);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }
}   