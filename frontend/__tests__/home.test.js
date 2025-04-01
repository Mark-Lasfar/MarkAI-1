// frontend/__tests__/home.test.js
import { render, screen } from '@testing-library/react'
import Home from '../pages/index'

describe('Home', () => {
  it('renders main heading', () => {
    render(<Home />)
    const heading = screen.getByText(/MarkAI/i)
    expect(heading).toBeInTheDocument()
  })
})