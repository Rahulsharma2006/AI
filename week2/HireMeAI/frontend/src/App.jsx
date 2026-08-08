import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [portfolio, setPortfolio] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/portfolio')
      .then((response) => response.json())
      .then((data) => {
        setPortfolio(data)
        setLoading(false)
      })
      .catch(() => {
        setPortfolio({
          name: 'Your Name',
          headline: 'AI Engineer building thoughtful digital products',
          summary: 'This portfolio is ready to be customized with your own details.',
          location: 'Remote',
          email: 'you@example.com',
          github: 'https://github.com/your-handle',
          linkedin: 'https://linkedin.com/in/your-handle',
          skills: ['Python', 'FastAPI', 'React', 'AI APIs'],
          experience: [],
          education: [],
          projects: [],
          certifications: [],
          chatPrompt: 'Ask me about my journey.',
        })
        setLoading(false)
      })
  }, [])

  if (loading || !portfolio) {
    return <div className="loading-shell">Loading your portfolio...</div>
  }

  return (
    <div className="portfolio-shell">
      <header className="hero-card">
        <div>
          <p className="eyebrow">Personal AI Portfolio</p>
          <h1>{portfolio.name}</h1>
          <p className="headline">{portfolio.headline}</p>
          <p className="summary">{portfolio.summary}</p>
          <div className="hero-actions">
            <a href={`mailto:${portfolio.email}`}>Contact me</a>
            <a href={portfolio.github} target="_blank" rel="noreferrer">
              GitHub
            </a>
            <a href={portfolio.linkedin} target="_blank" rel="noreferrer">
              LinkedIn
            </a>
          </div>
        </div>
      </header>

      <section className="section-card">
        <h2>About</h2>
        <p>{portfolio.summary}</p>
        <div className="info-grid">
          <div>
            <span>Location</span>
            <strong>{portfolio.location}</strong>
          </div>
          <div>
            <span>Email</span>
            <strong>{portfolio.email}</strong>
          </div>
          <div>
            <span>Focus</span>
            <strong>AI + Product Engineering</strong>
          </div>
        </div>
      </section>

      <section className="section-card">
        <h2>Skills</h2>
        <div className="chip-list">
          {portfolio.skills.map((skill) => (
            <span key={skill} className="chip">
              {skill}
            </span>
          ))}
        </div>
      </section>

      <section className="section-card">
        <h2>Experience</h2>
        <div className="stack-list">
          {portfolio.experience.length > 0 ? (
            portfolio.experience.map((item) => (
              <article key={`${item.company}-${item.role}`} className="stack-item">
                <div className="stack-header">
                  <h3>{item.role}</h3>
                  <span>{item.duration}</span>
                </div>
                <p className="company">{item.company}</p>
                <p>{item.description}</p>
                <div className="chip-list small">
                  {item.skills_used.map((skill) => (
                    <span key={skill} className="chip subtle">
                      {skill}
                    </span>
                  ))}
                </div>
              </article>
            ))
          ) : (
            <p className="muted">Add your experience details in the backend payload to populate this section.</p>
          )}
        </div>
      </section>

      <section className="section-card">
        <h2>Projects</h2>
        <ul className="bullet-list">
          {portfolio.projects.map((project) => (
            <li key={project}>{project}</li>
          ))}
        </ul>
      </section>

      <section className="section-card split-grid">
        <div>
          <h2>Education</h2>
          <ul className="bullet-list">
            {portfolio.education.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
        <div>
          <h2>Certifications</h2>
          <ul className="bullet-list">
            {portfolio.certifications.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      </section>

      <section className="section-card">
        <h2>Ask about me</h2>
        <p>{portfolio.chatPrompt}</p>
      </section>
    </div>
  )
}

export default App
