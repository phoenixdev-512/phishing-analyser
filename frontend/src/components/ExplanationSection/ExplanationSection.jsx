import React from 'react';

const ExplanationSection = ({ aiAnalysis }) => {
    if (!aiAnalysis) return null;

    return (
        <div style={{
            marginTop: '2rem',
            borderLeft: '4px solid var(--accent-cyber)',
            background: 'rgba(0, 217, 247, 0.05)',
            padding: '1.5rem',
            position: 'relative',
            overflow: 'hidden'
        }}>
            <div style={{
                position: 'absolute',
                top: 0,
                right: 0,
                background: 'var(--accent-cyber)',
                color: 'var(--bg-primary)',
                padding: '0.2rem 0.5rem',
                fontSize: '0.7rem',
                fontWeight: 'bold'
            }}>
                SECURITY ANALYSIS
            </div>

            <h3 style={{ color: 'var(--accent-cyber)', marginTop: 0 }}>INTELLIGENCE SUMMARY</h3>

            <div style={{ lineHeight: '1.6', fontSize: '1.05rem' }}>
                {aiAnalysis.explanation}
            </div>

            {aiAnalysis.score !== undefined && (
                <div style={{ marginTop: '1rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                    Confidence Score: <span style={{ color: 'var(--text-primary)' }}>{aiAnalysis.score}/100</span>
                </div>
            )}
        </div>
    );
};

export default ExplanationSection;
