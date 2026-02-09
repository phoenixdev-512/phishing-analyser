  import { useState } from 'react'
import ResultCard from './components/ResultCard/ResultCard'
import ExplanationSection from './components/ExplanationSection/ExplanationSection'
import './index.css'

function App() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const analyzeUrl = async (e) => {
    e.preventDefault()
    if (!url) return

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      // Use env var for base URL if set, otherwise default to relative path (proxied by Vite or Vercel)
      const baseUrl = import.meta.env.VITE_API_BASE_URL || '';
      const apiUrl = `${baseUrl}/api/analyze`;

      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      })

      if (!response.ok) {
        throw new Error('Analysis failed. Server might be down or busy.')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      console.error(err)
      setError(err.message || 'An error occurred during analysis')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="cyber-container">
      <header style={{ marginBottom: '4rem', borderBottom: '1px solid #333', paddingBottom: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 className="glitch-text" style={{ margin: 0, fontSize: '1.5rem', color: 'var(--accent-cyber)' }}>
          PHISHING<span style={{ color: 'white' }}>.ANALYZER</span>
        </h1>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: 'var(--accent-safe)', boxShadow: '0 0 10px var(--accent-safe)' }} />
          <span style={{ fontSize: '0.8rem', color: 'var(--accent-safe)', letterSpacing: '2px' }}>OPERATIONAL</span>
        </div>
      </header>

      <main>
        <section style={{ marginBottom: '4rem' }}>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '0.5rem', fontSize: '0.9rem', letterSpacing: '1px' }}>URL INTELLIGENCE SCANNER</p>
          <form onSubmit={analyzeUrl} style={{ display: 'flex', gap: '1rem' }}>
            <input
              type="text"
              className="cyber-input"
              placeholder="ENTER TARGET URL (e.g. example.com)"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              disabled={loading}
              style={{ flex: 1 }}
            />
            <button type="submit" className="cyber-btn" disabled={loading}>
              {loading ? 'SCANNING...' : 'ANALYZE'}
            </button>
          </form>
          {error && (
            <div style={{ marginTop: '1rem', color: 'var(--accent-malicious)', border: '1px solid var(--accent-malicious)', padding: '0.5rem' }}>
              ERROR: {error}
            </div>
          )}
        </section>

        {loading && (
          <div style={{ textAlign: 'center', padding: '4rem', color: 'var(--accent-cyber)' }}>
            <div className="glitch-text">INITIALIZING HEURISTICS...</div>
            <div style={{ marginTop: '1rem', width: '200px', height: '2px', background: '#333', margin: '1rem auto', position: 'relative', overflow: 'hidden' }}>
              <div style={{
                position: 'absolute',
                top: 0,
                left: 0,
                height: '100%',
                width: '50%',
                background: 'var(--accent-cyber)',
                animation: 'scan 1s infinite linear'
              }}></div>
            </div>
            <style>{`
              @keyframes scan {
                0% { left: -50%; }
                100% { left: 100%; }
              }
            `}</style>
          </div>
        )}

        {result && (
          <div className="fade-in">
            <ResultCard result={result} />
            <ExplanationSection aiAnalysis={result.ai_analysis} />
          </div>
        )}
      </main>

      <footer style={{ marginTop: '4rem', borderTop: '1px solid #333', paddingTop: '1rem', textAlign: 'center', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
        v1.0.0 • HYBRID ML + RULES • 2026
      </footer>
    </div>
  )
}

export default App
